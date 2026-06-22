#!/usr/bin/env python3
"""
v2 — Inject Kroppsskanning / Body Composition (InBody) links into the
medibalans-website nav, anchoring STRUCTURALLY instead of on exact strings.

WHY v2
------
v1 used one exact sibling line per copy. The hand-maintained navs vary in
label and subset across pages, so v1 covered desktop fully (71) but missed
most mobile/footer copies. v2 locates each block by its container and inserts
before the closing tag, so it does not care which items a given copy lists:

  desktop : the <div class="dropdown-menu"> that contains the diagnostics
            marker (methyldetox / methylation-test) -> insert before </div>
  mobile  : the "— Diagnostik/Diagnostics —" section -> insert before the
            next section header (<a ...>— …)
  footer  : the <h4>Diagnostik/Diagnostics</h4> + <ul> -> insert before </ul>

Idempotent (skips a block that already has the new link), fail-closed
(a block it cannot locate is skipped and counted, never half-edited),
dry-run by default.

USAGE
    python3 inject_nav_v2.py            # dry run + report
    python3 inject_nav_v2.py --apply     # write
"""

import sys, pathlib, re

APPLY = "--apply" in sys.argv
ROOT = pathlib.Path(".").resolve()
SKIP = {".git", "node_modules", ".vercel", ".next"}
files = [p for p in ROOT.rglob("*.html") if not any(s in p.parts for s in SKIP)]

LOCALES = {
    "SV": {
        "href": "/kroppsskanning/",
        "marker": "/methyldetox/",
        "section": "— Diagnostik —", "label": "Diagnostik",
        "h4": "Diagnostik",
        "desktop_link": '\n          <a href="/kroppsskanning/">Kroppsskanning — InBody</a>',
        "mobile_link":  '\n  <a href="/kroppsskanning/" onclick="closeMobile()" class="sub">Kroppsskanning — InBody</a>',
        "footer_link":  '\n          <li><a href="/kroppsskanning/">Kroppsskanning</a></li>',
    },
    "EN": {
        "href": "/en/body-composition-analysis/",
        "marker": "/en/methylation-test/",
        "section": "— Diagnostics —", "label": "Diagnostics",
        "h4": "Diagnostics",
        "desktop_link": '\n          <a href="/en/body-composition-analysis/">Body Composition — InBody</a>',
        "mobile_link":  '\n  <a href="/en/body-composition-analysis/" onclick="closeMobile()" class="sub">Body Composition — InBody</a>',
        "footer_link":  '\n          <li><a href="/en/body-composition-analysis/">Body Composition</a></li>',
    },
}

# tallies[(LOC, copy)] = [present, injected, already, skipped]
tallies = {(loc, c): [0, 0, 0, 0]
           for loc in LOCALES for c in ("desktop", "mobile", "footer")}

def inject_desktop(text, L):
    marker = re.escape(L["marker"])
    pat = re.compile(r'<div class="dropdown-menu">(?:(?!</div>).)*?' + marker +
                     r'(?:(?!</div>).)*?</div>', re.S)
    return _apply(text, L, "desktop", pat, L["desktop_link"])

def inject_mobile(text, L):
    # Mobile section header may be <a style=...>— Label —</a> (SV template)
    # or <div class="mob-section-label">— Label —</div> (EN template).
    # Capture from that header up to the next section header (<a|<div ...>— ).
    label = re.escape(L["label"])
    pat = re.compile(r'>—\s*' + label + r'\s*—\s*</(?:a|div)>.*?(?=<(?:a|div)[^>]*>—\s)', re.S)
    return _apply(text, L, "mobile", pat, L["mobile_link"], before_close=False)

def inject_footer(text, L):
    pat = re.compile(r'<h4>\s*' + re.escape(L["h4"]) + r'\s*</h4>\s*<ul>(?:(?!</ul>).)*?</ul>', re.S)
    return _apply(text, L, "footer", pat, L["footer_link"])

def _apply(text, L, copy, pat, link, before_close=True):
    m = pat.search(text)
    key = (L["EN_or_SV"], copy)
    if not m:
        # block not present at all -> not a miss, just absent on this page
        return text
    tallies[key][0] += 1  # present
    blk = m.group(0)
    if L["href"] in blk:
        tallies[key][2] += 1  # already
        return text
    if before_close:
        # insert link just before the final closing tag of the block
        close = "</div>" if copy == "desktop" else "</ul>"
        idx = blk.rfind(close)
        new_blk = blk[:idx] + link + "\n        " + blk[idx:]
    else:
        # mobile: append link at the end of the captured section
        new_blk = blk.rstrip() + link + "\n  "
    text = text[:m.start()] + new_blk + text[m.end():]
    tallies[key][1] += 1  # injected
    return text

changed = 0
for path in files:
    text = path.read_text(encoding="utf-8")
    original = text
    for name, L in LOCALES.items():
        L["EN_or_SV"] = name
        text = inject_desktop(text, L)
        text = inject_mobile(text, L)
        text = inject_footer(text, L)
    if text != original:
        changed += 1
        if APPLY:
            path.write_text(text, encoding="utf-8")

mode = "APPLIED" if APPLY else "DRY RUN (no files written — use --apply)"
print(f"\n=== Nav injection v3 · {mode} ===")
print(f"HTML files scanned : {len(files)}")
print(f"Files changed      : {changed}\n")
print(f"{'copy':<12}{'present':>9}{'injected':>10}{'already':>9}")
for (loc, copy), (present, inj, alr, _sk) in tallies.items():
    print(f"{loc+' '+copy:<12}{present:>9}{inj:>10}{alr:>9}")
print("\nFor each copy: present = pages that actually contain that block.")
print("injected + already should equal present. If present is lower than")
print("the desktop count for the same locale, those pages simply have no")
print("mobile/footer block — expected, not an error.")
