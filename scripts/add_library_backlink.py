# -*- coding: utf-8 -*-
"""
MediBalans · återlänk till kunskapsbanken från varje artikel
==============================================================
PROBLEMET
45 artiklar fanns men noll sidor länkade till kunskapsbanken utanför
navigationen. Varje artikel var alltså en återvändsgränd: läsaren som
just läst klart en symtomguide — precis den person som vill läsa nästa —
fick ingen väg vidare.

ÅTGÄRD
Ett litet band sist i artikeln, före footern, som leder till biblioteket
och anger hur många artiklar som finns där. Bandet är avsiktligt
diskret; det ska fånga den som är klar med texten, inte konkurrera med
konsultations-CTA:n.

Endast artikelsidor får bandet — inte startsidan, inte
integritetspolicyn, inte biblioteket självt eller sektionsindexen.
Klassificeringen återanvänds från build_library så att urvalet är
detsamma som det biblioteket faktiskt listar.

Torrkörning:  python3 scripts/add_library_backlink.py --dry
Skarpt:       python3 scripts/add_library_backlink.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_library import samla, ROOT  # noqa: E402

DRY = "--dry" in sys.argv
MARKER = "kb-backlink"
SEKTIONSMARKOR = 'class="kb-back"'

CSS = """<style>/* {m} */
.kb-back{border-top:1px solid var(--border);background:var(--ice-faint);padding:2.2rem 0;margin-top:0}
.kb-back .inner{max-width:1100px;margin:0 auto;padding:0 2rem;display:flex;gap:1.2rem;
  align-items:center;justify-content:space-between;flex-wrap:wrap}
.kb-back .txt{font-family:var(--font-body);color:var(--text-mid);font-size:.95rem;line-height:1.6;margin:0}
.kb-back .txt strong{color:var(--navy)}
.kb-back a.kb-link{display:inline-block;background:var(--navy);color:#fff;text-decoration:none;
  padding:.8rem 1.5rem;border-radius:4px;font-size:.9rem;font-weight:600;white-space:nowrap}
.kb-back a.kb-link:hover{background:var(--navy-light,#1A3A5E)}
@media(max-width:640px){.kb-back .inner{flex-direction:column;align-items:flex-start}}
</style>""".replace("{m}", MARKER)


def band(lang, antal):
    if lang == "sv":
        txt = (f"<strong>Fortsätt läsa.</strong> Samtliga {antal} artiklar — symtomguider, kliniska "
               "noteringar, utredningar och diagnostik — är samlade och sökbara i kunskapsbanken.")
        cta, href = "Till kunskapsbanken", "/kunskapsbank/"
    else:
        txt = (f"<strong>Keep reading.</strong> All {antal} articles — symptom guides, clinical notes, "
               "investigations and diagnostics — are collected and searchable in the knowledge base.")
        cta, href = "Go to the knowledge base", "/en/knowledge-base/"
    return (f'\n<section class="kb-back"><div class="inner">'
            f'<p class="txt">{txt}</p>'
            f'<a class="kb-link" href="{href}">{cta} →</a>'
            f'</div></section>\n')


def main():
    UTESLUT = {"kunskapsbank", "knowledge-base", "teorem", "theorems"}
    sv = {p["slug"] for p in samla("sv")} - UTESLUT
    en = {p["slug"] for p in samla("en")} - UTESLUT
    print(f"artiklar: SV {len(sv)} · EN {len(en)}\n")

    n = 0
    hoppade = []
    for lang, slugs, pre in (("sv", sv, ""), ("en", en, "en/")):
        antal = len(slugs)
        for slug in sorted(slugs):
            rel = os.path.join(pre, slug, "index.html")
            p = os.path.join(ROOT, rel)
            if not os.path.exists(p):
                hoppade.append((rel, "finns ej"))
                continue
            h = open(p, encoding="utf-8").read()
            if SEKTIONSMARKOR in h:
                continue
            m = re.search(r"<footer\b", h)
            if not m:
                hoppade.append((rel, "ingen footer"))
                continue
            ny = h[:m.start()] + band(lang, antal) + h[m.start():]
            # CSS sist i head
            if MARKER in ny:
                pass          # CSS ärvd via skalet
            elif "</head>" in ny:
                ny = ny.replace("</head>", CSS + "\n</head>", 1)
            else:
                hoppade.append((rel, "ingen </head>"))
                continue
            if not DRY:
                open(p, "w", encoding="utf-8").write(ny)
            n += 1

    print("\n" + ("TORRKORNING — inget skrivet" if DRY else "SKRIVET"))
    print(f"  {n} artiklar fick återlänk")
    if hoppade:
        print(f"  {len(hoppade)} hoppade:")
        for r, w in hoppade[:10]:
            print(f"     {r:52} {w}")


if __name__ == "__main__":
    main()
