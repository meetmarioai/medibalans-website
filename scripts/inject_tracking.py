#!/usr/bin/env python3
"""
Inject the analytics and chat-widget blocks into every page that is missing them.

Why this exists
---------------
The site has no build step and no template engine: every page is hand-written
HTML, and the GA4, Meta Pixel and Meet Mario blocks are pasted in by hand. Over
111 pages that has drifted badly.

    GA4      absent from 27 pages - including ALL FIVE symptom guides, /cma/,
             and both knowledge-base hubs. Those are the highest-intent pages on
             the site and they have been invisible in analytics.
    Pixel    absent from 7 - including /cma/ and /en/alcat-test/. Ad spend
             against pages that cannot report a conversion.
    Widget   absent from 14 - the entire long-form editorial cluster, which is
             exactly the content that earns answer-engine traffic. Those readers
             arrive, read, and have nothing to click.

This follows the same pattern as scripts/apply_canonical_nav.py: one source of
truth, applied mechanically to every file, rather than remembering to paste
three blocks into each new page.

Usage
-----
    python3 scripts/inject_tracking.py --dry     # report only, writes nothing
    python3 scripts/inject_tracking.py           # apply

Blocks are lifted verbatim from index.html at run time, so this cannot drift
from the canonical copy. Files that already carry a block are never touched.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "index.html"

# Files that must never get tracking or a chat widget.
#   redirect stubs   - meta-refresh only, nothing to measure
#   the GSC file     - Google's own verification file
#   privacy policy   - a page about data handling should not itself set
#                      marketing cookies before the visitor has read it
SKIP = {
    "en-clinical-notes/index.html",
    "utredningsprotokol.html",
    "google7dc4d048aac517b5.html",
    "integritetspolicy/index.html",
    "en/privacy-policy/index.html",
}


def extract(text, start_pat, end_pat, name):
    """Pull a block out of index.html, from start_pat through end_pat inclusive."""
    s = re.search(start_pat, text)
    if not s:
        sys.exit(f"could not locate the start of the {name} block in index.html")
    e = re.search(end_pat, text[s.start():])
    if not e:
        sys.exit(f"could not locate the end of the {name} block in index.html")
    return text[s.start(): s.start() + e.end()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="report without writing")
    args = ap.parse_args()

    src = SOURCE.read_text(encoding="utf-8")

    ga4 = extract(
        src,
        r'<script async src="https://www\.googletagmanager\.com/gtag/js',
        r"</script>\s*\n\s*</script>|</script>[\s\S]{0,200}?</script>",
        "GA4",
    )
    # Tighter: GA4 is two adjacent script tags.
    m = re.search(
        r'<script async src="https://www\.googletagmanager\.com/gtag/js[\s\S]*?</script>\s*<script>[\s\S]*?</script>',
        src,
    )
    ga4 = m.group() if m else ga4

    pixel = extract(
        src,
        r"<script>\s*\n!function\(f,b,e,v,n,t,s\)",
        r"</noscript>",
        "Meta Pixel",
    )

    widget = extract(
        src,
        r"<style>#__mb_bubble",
        r"\}\)\(\);</script>",
        "Meet Mario widget",
    )

    print(f"blocks lifted from index.html — ga4 {len(ga4)}B  pixel {len(pixel)}B  widget {len(widget)}B\n")

    pages = sorted(
        p for p in ROOT.rglob("*.html")
        if "node_modules" not in p.parts and str(p.relative_to(ROOT)) not in SKIP
    )

    counts = {"ga4": 0, "pixel": 0, "widget": 0}
    touched = []

    for page in pages:
        rel = str(page.relative_to(ROOT))
        html = page.read_text(encoding="utf-8")
        original = html
        added = []

        # Redirect stubs have no head/body worth touching.
        if "</head>" not in html or "</body>" not in html:
            continue

        if "googletagmanager" not in html and "gtag(" not in html:
            html = html.replace("</head>", ga4 + "\n</head>", 1)
            added.append("ga4")
            counts["ga4"] += 1

        if "fbq(" not in html:
            html = html.replace("</head>", pixel + "\n</head>", 1)
            added.append("pixel")
            counts["pixel"] += 1

        # The widget goes last in the body so it never blocks content paint.
        if "__mb_bubble" not in html:
            html = html.replace("</body>", widget + "\n</body>", 1)
            added.append("widget")
            counts["widget"] += 1

        if html != original:
            touched.append((rel, added))
            if not args.dry:
                page.write_text(html, encoding="utf-8")

    for rel, added in touched:
        print(f"  {'+'.join(added):20} {rel}")

    print(
        f"\n{len(touched)} file(s) {'would change' if args.dry else 'changed'} — "
        f"ga4 {counts['ga4']}, pixel {counts['pixel']}, widget {counts['widget']}"
    )
    if args.dry:
        print("dry run — nothing written")


if __name__ == "__main__":
    main()
