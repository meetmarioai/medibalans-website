# -*- coding: utf-8 -*-
"""
MediBalans · Teorem / Theorems — tvåspråkig sektion
====================================================
Satserna definieras EN gång i TEOREM nedan, med fält för båda språken.
Svenska och engelska sidor genereras ur samma datastruktur, vilket gör
det omöjligt för dem att glida isär — samma princip som canonical_nav.

RAMVERK (beslutat med Dr Mario)
  · Satserna presenteras som FALSIFIERBARA PROPOSITIONER, inte som
    bevisade teorem. Det står uttryckligen i ingressen, vilket avväpnar
    den självklara invändningen innan den hinner göras.
  · Varje sats MÅSTE ha en falsifieringsklausul. En sats som inte kan
    motbevisas publiceras inte här.
  · Satserna versioneras och revideringar redovisas öppet.
  · IP-spärr: satserna anger PRINCIP, aldrig PROCEDUR. Tröskelvärden,
    viktningar, sekvenser och poängsättning hör inte hemma på sidan.
    Den stående raden om patentansökningar gör spärren till en
    trovärdighetssignal i stället för en lucka.

Nya satser läggs till som en post i TEOREM. Kör om skriptet.

Kör:  python3 scripts/build_teorem.py
"""
import html as H
import re
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from build_new_sections import page as sv_page, hero as sv_hero, band as sv_band, ROOT, BASE
from build_content_en import page as en_page, hero as en_hero, band as en_band

SV_URL = f"{BASE}/teorem/"
EN_URL = f"{BASE}/en/theorems/"
ORG = {"@id": f"{BASE}/#organization"}
AUTHOR_ID = f"{BASE}/#mario-anthis"

# ─────────────────────────────────────────────────────────────── satserna
TEOREM = [
    dict(
        nr="T1", version="1", datum="2026-07",
        status_sv="Under prövning", status_en="Under test",
        namn_sv="Den bindande restriktionen",
        namn_en="The binding constraint",
        sats_sv="I ett biologiskt system med flera samtidiga brister bestäms funktionsnivån av "
                "den mest begränsande faktorn, inte av summan av faktorerna.",
        sats_en="In a biological system with several simultaneous deficits, the level of function "
                "is determined by the most limiting factor, not by the sum of the factors.",
        def_sv=[
            ("Bindande restriktion", "den faktor vars korrigering ensam höjer funktionsnivån."),
            ("Icke-substituerbar", "att ingen annan tillgänglig väg kan utföra samma uppgift."),
            ("Funktionsnivå", "systemets faktiska kapacitet, inte enskilda mätvärden."),
        ],
        def_en=[
            ("Binding constraint", "the factor whose correction alone raises the level of function."),
            ("Non-substitutable", "no other available pathway can perform the same task."),
            ("Level of function", "the system's actual capacity, not individual measured values."),
        ],
        rackvidd_sv="Gäller när de involverade faktorerna är icke-substituerbara. Gäller inte där "
                    "redundanta vägar kan kompensera för bortfallet — då fördelas begränsningen i "
                    "stället över flera faktorer och satsen förlorar sin skärpa.",
        rackvidd_en="Applies where the factors involved are non-substitutable. Does not apply where "
                    "redundant pathways can compensate for the loss — the constraint is then "
                    "distributed across several factors and the proposition loses its force.",
        grunder_sv=[
            "Enzymatiska kedjor är sekventiella. Ett steg som saknar sin kofaktor sätter takten för "
            "hela kedjan oavsett hur väl försörjda de övriga stegen är.",
            "Kliniskt återkommer mönstret att bred supplementering ger begränsad effekt medan "
            "korrigering av en enskild faktor ger oproportionerligt utslag — vilket är vad satsen "
            "förutsäger och vad en additiv modell inte förklarar.",
        ],
        grunder_en=[
            "Enzymatic chains are sequential. A step lacking its cofactor sets the pace for the "
            "entire chain regardless of how well supplied the remaining steps are.",
            "Clinically, the recurring pattern is that broad supplementation produces limited effect "
            "while correcting a single factor produces disproportionate response — which is what the "
            "proposition predicts and what an additive model does not explain.",
        ],
        falsifiering_sv="Att korrigering av en icke-bindande faktor ger samma funktionsvinst som "
                        "korrigering av den bindande faktorn. Ett sådant fynd skulle innebära att "
                        "faktorerna är additiva och att satsen är falsk.",
        falsifiering_en="That correcting a non-binding factor produces the same functional gain as "
                        "correcting the binding one. Such a finding would mean the factors are "
                        "additive and the proposition is false.",
    ),
]

CSS = """
.tm{border:1px solid var(--border);background:#fff;padding:2rem;margin-bottom:1.6rem}
.tm-head{display:flex;gap:1rem;align-items:baseline;flex-wrap:wrap;margin-bottom:1.2rem;
  border-bottom:1px solid var(--border);padding-bottom:1rem}
.tm-nr{font-family:var(--font-mono);font-size:1.4rem;color:var(--blue);font-weight:600}
.tm-namn{font-family:var(--font-display);font-size:1.5rem;color:var(--navy);line-height:1.2}
.tm-badge{margin-left:auto;font-family:var(--font-mono);font-size:.62rem;letter-spacing:.13em;
  text-transform:uppercase;color:var(--text-light);border:1px solid var(--border);
  padding:.3rem .7rem;border-radius:3px;white-space:nowrap}
.tm-sats{font-family:var(--font-display);font-size:1.22rem;line-height:1.5;color:var(--navy);
  border-left:3px solid var(--blue);padding-left:1.3rem;margin:0 0 1.6rem}
.tm-lbl{font-family:var(--font-mono);font-size:.63rem;letter-spacing:.15em;text-transform:uppercase;
  color:var(--text-light);margin:1.4rem 0 .5rem}
.tm dl{margin:0}
.tm dt{font-weight:600;color:var(--navy);font-size:.92rem;margin-top:.6rem}
.tm dd{margin:0 0 .2rem;color:var(--text-mid);font-size:.92rem}
.tm p{color:var(--text-mid);margin:0 0 .8rem;line-height:1.7}
.tm ul{margin:0;padding-left:1.15rem;color:var(--text-mid)}
.tm li{margin-bottom:.5rem;line-height:1.7}
.tm-fals{background:var(--bg-warm);border-left:3px solid var(--warm);padding:1.1rem 1.3rem;margin-top:1.2rem}
.tm-fals p{margin:0;color:var(--text)}
.tm-cite{font-family:var(--font-mono);font-size:.65rem;color:var(--text-light);margin-top:1.2rem;
  border-top:1px solid var(--border);padding-top:.8rem}
.tm-regler{background:var(--ice-faint);border-left:3px solid var(--blue);padding:1.5rem 1.7rem;margin:2rem 0}
.tm-regler p{margin:0 0 .7rem}
.tm-regler p:last-child{margin-bottom:0}
"""


def render(t, lang):
    sv = lang == "sv"
    namn = t["namn_sv"] if sv else t["namn_en"]
    sats = t["sats_sv"] if sv else t["sats_en"]
    defs = t["def_sv"] if sv else t["def_en"]
    rack = t["rackvidd_sv"] if sv else t["rackvidd_en"]
    grund = t["grunder_sv"] if sv else t["grunder_en"]
    fals = t["falsifiering_sv"] if sv else t["falsifiering_en"]
    status = t["status_sv"] if sv else t["status_en"]
    L = dict(
        sats="Sats" if sv else "Proposition",
        defi="Definitioner" if sv else "Definitions",
        rack="Räckvidd" if sv else "Scope",
        grund="Grunder" if sv else "Grounds",
        fals="Vad som skulle falsifiera satsen" if sv else "What would falsify this",
        cite="Citeras som" if sv else "Cite as",
    )
    url = SV_URL if sv else EN_URL
    dl = "".join(f"<dt>{H.escape(a)}</dt><dd>{H.escape(b)}</dd>" for a, b in defs)
    gl = "".join(f"<li>{H.escape(g)}</li>" for g in grund)
    return f"""<div class="tm" id="{t['nr'].lower()}">
<div class="tm-head">
  <span class="tm-nr">{t['nr']}</span>
  <span class="tm-namn">{H.escape(namn)}</span>
  <span class="tm-badge">{H.escape(status)} · v{t['version']} · {t['datum']}</span>
</div>
<div class="tm-lbl">{L['sats']}</div>
<p class="tm-sats">{H.escape(sats)}</p>
<div class="tm-lbl">{L['defi']}</div><dl>{dl}</dl>
<div class="tm-lbl">{L['rack']}</div><p>{H.escape(rack)}</p>
<div class="tm-lbl">{L['grund']}</div><ul>{gl}</ul>
<div class="tm-fals"><div class="tm-lbl" style="margin-top:0">{L['fals']}</div><p>{H.escape(fals)}</p></div>
<div class="tm-cite">{L['cite']}: MediBalans {t['nr']} v{t['version']} — {H.escape(namn)}. {url}#{t['nr'].lower()}</div>
</div>"""


def bygg(lang):
    sv = lang == "sv"
    url, other = (SV_URL, EN_URL) if sv else (EN_URL, SV_URL)
    kort = "".join(render(t, lang) for t in TEOREM)

    if sv:
        titel = "Teorem — falsifierbara satser om biologisk funktion | MediBalans"
        desc = ("Numrerade, versionerade satser om biologisk funktion. Varje sats anger räckvidd, "
                "grunder och vad som skulle falsifiera den. Principer, inte metod.")
        h1, h1em = "Teorem ", "Satser som går att motbevisa."
        lead = ("Detta är den formella delen av vårt arbete. Satserna nedan är propositioner, inte bevis — "
                "de är formulerade så att de går att pröva och motbevisa, och de revideras öppet när "
                "underlaget ändras.")
        regler = ("<p><strong>Tre regler för den här sidan.</strong></p>"
                  "<p>En sats publiceras här endast om den går att falsifiera. Kan ingen observation "
                  "tänkas motbevisa den hör den hemma någon annanstans.</p>"
                  "<p>Satserna versioneras. När en sats revideras redovisas ändringen och skälet öppet "
                  "i stället för att texten tyst skrivs om.</p>"
                  "<p>Satserna anger <em>princip</em>, aldrig <em>procedur</em>. Tröskelvärden, viktningar "
                  "och beräkningssteg omfattas av patentansökningar och beskrivs inte här.</p>")
        band_a, band_b = "Från princip", "till mätning"
        band_p = ("Satserna är den formella grunden. Den kliniska tillämpningen börjar med att mäta vad "
                  "som faktiskt begränsar just din biologi.")
        lbl_other = "English"
        eyebrow = "Forskning · Formella satser"
    else:
        titel = "Theorems — falsifiable propositions on biological function | MediBalans"
        desc = ("Numbered, versioned propositions on biological function. Each states its scope, its "
                "grounds, and what would falsify it. Principles, not method.")
        h1, h1em = "Theorems ", "Propositions that can be refuted."
        lead = ("This is the formal part of our work. The propositions below are conjectures, not proofs — "
                "they are stated so that they can be tested and refuted, and they are revised openly when "
                "the evidence changes.")
        regler = ("<p><strong>Three rules for this page.</strong></p>"
                  "<p>A proposition is published here only if it can be falsified. If no observation could "
                  "refute it, it belongs elsewhere.</p>"
                  "<p>Propositions are versioned. When one is revised, the change and the reason are shown "
                  "openly rather than the text being quietly rewritten.</p>"
                  "<p>Propositions state <em>principle</em>, never <em>procedure</em>. Thresholds, weightings "
                  "and computational steps are covered by patent applications and are not described here.</p>")
        band_a, band_b = "From principle", "to measurement"
        band_p = ("The propositions are the formal basis. Clinical application begins by measuring what "
                  "actually constrains your biology.")
        lbl_other = "Svenska"
        eyebrow = "Research · Formal propositions"

    schema = ['<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "@id": url + "#page", "url": url, "name": titel,
             "inLanguage": "sv-SE" if sv else "en-GB", "description": desc,
             "author": {"@id": AUTHOR_ID}, "publisher": ORG},
            {"@type": "ItemList", "@id": url + "#list", "numberOfItems": len(TEOREM),
             "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "url": f"{url}#{t['nr'].lower()}",
                  "name": f"{t['nr']} — " + (t["namn_sv"] if sv else t["namn_en"])}
                 for i, t in enumerate(TEOREM)]}]}, ensure_ascii=False) + "</script>"]

    booking = "/#booking" if sv else "/en/#booking"
    skrifter = "/skrifter/" if sv else "/en/writings/"
    gcr = "/global-constraint-rule/" if sv else "/en/global-constraint-rule/"
    hero_f = sv_hero if sv else en_hero
    band_f = sv_band if sv else en_band

    innehall = f"""
{hero_f(eyebrow, h1, h1em, lead,
        f'<a class="btn-p" href="{booking}">' + ("Boka konsultation" if sv else "Book a consultation") + '</a>'
        f'<a class="btn-s" href="{gcr}">Global Constraint Rule</a>',
        ("Propositioner under prövning. Inte etablerad evidens." if sv
         else "Propositions under test. Not established evidence."),
        [(str(len(TEOREM)), "Satser" if sv else "Propositions"),
         ("Anthis", "Författare" if sv else "Author"),
         ("v1", "Version"), ("2026", "Publicerad" if sv else "Published")])}
<div class="container sec-body">
<section><div class="tm-regler">{regler}</div></section>
<section>{kort}</section>
<section>
<p style="margin-top:1rem"><a href="{gcr}">Global Constraint Rule →</a> · <a href="{skrifter}">{'Skrifter' if sv else 'Writings'}</a> · <a href="{other}">{lbl_other}</a></p>
</section>
</div>
{band_f(band_a, band_b, band_p)}
"""
    if sv:
        html = sv_page(titel, desc, url, schema, innehall).replace("</style>", CSS + "\n</style>", 1)
        # sv_page saknar hreflang mot engelska — sätt in den reciproka länken
        m = re.search(r'<link rel="alternate" hreflang="sv" href="[^"]+">', html)
        if m:
            html = html.replace(m.group(0),
                                m.group(0) + f'\n<link rel="alternate" hreflang="en" href="{other}">', 1)
        return html
    return en_page(titel, desc, url, other, schema, innehall).replace("</style>", CSS + "\n</style>", 1)


if __name__ == "__main__":
    # RETIRERAD 2026-07-30. Teorem-sidorna (/teorem/, /en/theorems/) är
    # permanent borttagna från webbplatsen och returnerar 410 Gone via
    # vercel.json. Denna generator får INTE köras — den skulle återskapa
    # sidorna och (via canonical_nav) återinföra menyposterna på alla sidor.
    # Filen är kvar enbart som historik och kan tas bort med `git rm`.
    raise SystemExit(
        "build_teorem.py är retirerad: /teorem/ och /en/theorems/ är "
        "borttagna (410 Gone). Kör inte denna generator."
    )
