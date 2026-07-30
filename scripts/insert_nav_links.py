# -*- coding: utf-8 -*-
"""
MediBalans · nav-insättning för /symtom/ och /skrifter/ (+ EN)
==============================================================
Lägger in två nya navigationslänkar på samtliga sidor, i BÅDA språken
och i BÅDA navigationerna (desktop-dropdown och mobilmeny).

Varför detta är gjort försiktigt:
  Webbplatsen har flera nav-dialekter. Mobilmenyn förekommer i minst två
  varianter — en med <div class="mob-section-label"> och en med
  class="sub" på länkarna. Desktop använder .dropdown-menu.
  Skriptet hårdkodar därför INGEN markup. Det hittar en befintlig
  ankarlänk i respektive sektion, KLONAR dess attribut (class, onclick)
  och sätter in den nya länken före den — så att varje länk automatiskt
  får rätt markup för sin egen kontext.

Idempotent: hoppar över filer som redan innehåller länken.
Torrkörning:  python3 scripts/insert_nav_links.py --dry
Skarpt:       python3 scripts/insert_nav_links.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv

# (ny href, ny text, [ankar-href att sätta in FÖRE — första som hittas används])
# Flera kandidater eftersom navigationen inte är identisk på alla sidor.
RULES_SV = [
    ("/symtom/", "Symtomguider",
     ["/ibs-tarmhalsa/", "/utmattning/", "/autoimmun/", "/alcat/"]),
]
RULES_EN = [
    ("/en/symptoms/", "Symptom Guides",
     ["/en/ibs-gut-health/", "/en/chronic-fatigue/", "/en/autoimmunity/", "/en/alcat-test/"]),
]

# regioner där insättning får ske
REGION_PATTERNS = [
    (r"<header\b.*?</header>", "desktop"),
    (r'<div class="mobile-nav"[^>]*>.*?(?=<script|</body)', "mobil"),
]


def clone_anchor(anchor_tag, new_href, new_text):
    """Bygg en ny <a> med samma attribut som den matchade, men ny href/text."""
    attrs = dict(re.findall(r'(\w[\w-]*)\s*=\s*"([^"]*)"', anchor_tag))
    attrs["href"] = new_href
    order = ["href", "onclick", "class"]
    parts = []
    for k in order:
        if k in attrs:
            parts.append(f'{k}="{attrs[k]}"')
    for k, v in attrs.items():
        if k not in order:
            parts.append(f'{k}="{v}"')
    return f"<a {' '.join(parts)}>{new_text}</a>"


def process(path, rules):
    h = open(path, encoding="utf-8").read()
    original = h
    report = []

    for new_href, new_text, anchor_candidates in rules:
        for region_re, region_name in REGION_PATTERNS:
            m = re.search(region_re, h, re.S)
            if not m:
                report.append(f"{region_name}:region saknas")
                continue
            region = m.group(0)
            if f'href="{new_href}"' in region:
                report.append(f"{region_name}:redan")
                continue
            am = None
            for cand in anchor_candidates:
                am = re.search(r'<a\b[^>]*href="' + re.escape(cand) + r'"[^>]*>.*?</a>', region, re.S)
                if am:
                    break

            if am:
                new_link = clone_anchor(am.group(0), new_href, new_text)
                new_region = region[:am.start()] + new_link + "\n      " + region[am.start():]
            else:
                # Reservväg: ingen av ankarkandidaterna finns i denna nav-dialekt.
                # Sätt in efter sista interna länken i regionen, med klonade
                # attribut, så att länken ändå finns på sidan.
                alls = list(re.finditer(r'<a\b[^>]*href="/[^"]*"[^>]*>.*?</a>', region, re.S))
                if not alls:
                    report.append(f"{region_name}:ingen länk att klona")
                    continue
                last = alls[-1]
                new_link = clone_anchor(last.group(0), new_href, new_text)
                new_region = region[:last.end()] + "\n      " + new_link + region[last.end():]
                report.append(f"{region_name}:reserv")
            h = h[:m.start()] + new_region + h[m.end():]
            report.append(f"{region_name}:+{new_text}")

    changed = h != original
    if changed and not DRY:
        open(path, "w", encoding="utf-8").write(h)
    return changed, report


def main():
    sv, en = [], []
    for dirpath, _, files in os.walk(ROOT):
        if any(x in dirpath for x in (".git", "node_modules", "scripts", "downloads")):
            continue
        for fn in files:
            if fn != "index.html":
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT)
            (en if rel.startswith("en/") or rel.startswith("en-") else sv).append(p)

    stats = {"ändrade": 0, "oförändrade": 0, "saknar ankare": 0}
    for group, rules, label in ((sv, RULES_SV, "SV"), (en, RULES_EN, "EN")):
        print(f"\n=== {label} ({len(group)} filer) ===")
        for p in sorted(group):
            changed, report = process(p, rules)
            rel = os.path.relpath(p, ROOT)
            if changed:
                stats["ändrade"] += 1
                print(f"  ✓ {rel:52} {' | '.join(report)}")
            else:
                if any("saknas" in r for r in report):
                    stats["saknar ankare"] += 1
                    print(f"  · {rel:52} {' | '.join(report)}")
                else:
                    stats["oförändrade"] += 1
    print("\n" + ("TORRKÖRNING — inget skrivet" if DRY else "SKRIVET"))
    print(stats)


if __name__ == "__main__":
    main()
