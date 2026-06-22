#!/usr/bin/env python3
"""
Add the Kroppsskanning (SV) and Body Composition (EN) pages to sitemap.xml,
each with full hreflang alternates.

The current sitemap is a flat <urlset> with no language alternates. For a
bilingual pair, the highest-value SEO addition is xhtml:link alternates so
Google pairs the two URLs and never reads them as duplicate content.

This script:
  - adds xmlns:xhtml to <urlset> if missing (required for xhtml:link)
  - inserts the two <url> blocks before </urlset> if not already present
  - is idempotent (re-running changes nothing) and dry-run by default

USAGE
    cd ~/path/to/medibalans-website
    python3 inject_sitemap_kroppsskanning.py            # dry run
    python3 inject_sitemap_kroppsskanning.py --apply     # write
"""

import sys, pathlib, datetime

APPLY = "--apply" in sys.argv
SITEMAP = pathlib.Path("sitemap.xml")
TODAY = datetime.date.today().isoformat()

SV = "https://www.medibalans.com/kroppsskanning/"
EN = "https://www.medibalans.com/en/body-composition-analysis/"

ALTS = (
    f'    <xhtml:link rel="alternate" hreflang="sv" href="{SV}"/>\n'
    f'    <xhtml:link rel="alternate" hreflang="en" href="{EN}"/>\n'
    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SV}"/>\n'
)

def block(loc):
    return (
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        "    <priority>0.8</priority>\n"
        f"{ALTS}"
        "  </url>\n\n"
    )

if not SITEMAP.exists():
    sys.exit("sitemap.xml not found — run from the repo root.")

xml = SITEMAP.read_text(encoding="utf-8")
original = xml
actions = []

# 1) ensure xhtml namespace on <urlset>
if "xmlns:xhtml" not in xml:
    xml = xml.replace(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        1,
    )
    actions.append("added xmlns:xhtml namespace")
else:
    actions.append("xmlns:xhtml already present")

# 2) insert the two url blocks before </urlset>
to_add = ""
if f"<loc>{SV}</loc>" not in xml:
    to_add += block(SV); actions.append("queued SV url block")
else:
    actions.append("SV url already in sitemap")
if f"<loc>{EN}</loc>" not in xml:
    to_add += block(EN); actions.append("queued EN url block")
else:
    actions.append("EN url already in sitemap")

if to_add:
    xml = xml.replace("</urlset>", to_add + "</urlset>", 1)

mode = "APPLIED" if APPLY else "DRY RUN (no file written — use --apply)"
print(f"=== sitemap injection · {mode} ===")
for a in actions:
    print("  -", a)
print(f"  url count before: {original.count('<url>')}  after: {xml.count('<url>')}")

if xml != original and APPLY:
    SITEMAP.write_text(xml, encoding="utf-8")
    print("  sitemap.xml written.")
elif xml == original:
    print("  nothing to change.")
