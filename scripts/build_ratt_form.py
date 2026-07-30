# -*- coding: utf-8 -*-
"""
MediBalans · Rätt form av tillskott — tvåspråkig klinisk notering
==================================================================
Praktisk följeslagare till /homocystein/. Där handlar det om VAR
flaskhalsen sitter; här om VILKEN FORM varje nod kräver och vad
fullständig kompensation innebär.

═══ IP-GRÄNS — LÄS INNAN NÅGOT ÄNDRAS ═══
Detta är den text som ligger närmast patentansökan 2451139-6 (NMN+5).
Ansökan hävdar att följande är ICKE-UPPENBART, och det får därför INTE
beskrivas här:

  · den specifika kombinationen NMN + metionin + TMG + 5-MTHF +
    hydroxokobalamin/adenosylkobalamin + P5P
  · trevägsarkitekturen BHMT + MTR + transsulfurering som konstruktion
  · resonemanget att methylkobalamin väljs BORT därför att exogena
    metylgrupper belastar COMT hos långsamma varianter
  · doser, kvoter, sekvens

Det som DÄREMOT är fri lärobokskemi och tryggt att publicera:
  · att 5-MTHF är den aktiva folatformen
  · att P5P är aktiv B6 och R5P aktiv B2
  · att B12 finns som cyano-, hydroxo-, metyl- och adenosylkobalamin
  · att BHMT och MTR är zinkberoende, MAT magnesiumberoende
  · att AHCY har hårt bundet NAD+ som kofaktor
  · principen att partiell kompensation flyttar flaskhalsen

Artikeln stannar vid princip och enskilda noder. Den beskriver aldrig en
sammansättning.

Kör:  python3 scripts/build_ratt_form.py
"""
import html as H
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from build_new_sections import page as sv_page, hero as sv_hero, toc as sv_toc, band as sv_band, ROOT, BASE
from build_content_en import page as en_page, hero as en_hero, toc as en_toc, band as en_band

SV_URL = f"{BASE}/ratt-form-av-tillskott/"
EN_URL = f"{BASE}/en/supplement-forms/"
ORG = {"@id": f"{BASE}/#organization"}
AUTHOR_ID = f"{BASE}/#mario-anthis"

# ───────────────────────────────────────────────────────── noder
NODER = [
    dict(
        nod="MTHFR", uppg_sv="Producerar aktivt folat", uppg_en="Produces active folate",
        form_sv="5-MTHF (metylfolat)", form_en="5-MTHF (methylfolate)",
        kofakt_sv="Riboflavin som FAD, NADPH", kofakt_en="Riboflavin as FAD, NADPH",
        obs_sv="Syntetisk folsyra kräver omvandling. Riboflavin stabiliserar det termolabila C677T-enzymet.",
        obs_en="Synthetic folic acid requires conversion. Riboflavin stabilises the thermolabile C677T enzyme.",
    ),
    dict(
        nod="MTR", uppg_sv="Återmetylerar homocystein", uppg_en="Remethylates homocysteine",
        form_sv="B12 — flera former finns", form_en="B12 — several forms exist",
        kofakt_sv="Zink, 5-MTHF som metyldonator", kofakt_en="Zinc, 5-MTHF as methyl donor",
        obs_sv="B12 förekommer som cyano-, hydroxo-, metyl- och adenosylkobalamin. De skiljer sig i "
               "stabilitet, halveringstid och hur de tas in i cellens kobalaminmetabolism.",
        obs_en="B12 occurs as cyano-, hydroxo-, methyl- and adenosylcobalamin. They differ in stability, "
               "half-life and how they enter cellular cobalamin metabolism.",
    ),
    dict(
        nod="MTRR", uppg_sv="Återställer oxiderat kobalamin", uppg_en="Restores oxidised cobalamin",
        form_sv="Ingen egen substans — kräver SAM", form_en="No substance of its own — requires SAM",
        kofakt_sv="SAM, NADPH, riboflavin (FAD/FMN)", kofakt_en="SAM, NADPH, riboflavin (FAD/FMN)",
        obs_sv="Noden går inte att supplementera direkt. Den försörjs indirekt genom att SAM-poolen och "
               "reduktionskapaciteten hålls uppe — vilket är skälet till att B12 ensamt ofta inte räcker.",
        obs_en="This node cannot be supplemented directly. It is supported indirectly by maintaining the SAM "
               "pool and reducing capacity — which is why B12 alone is often insufficient.",
    ),
    dict(
        nod="BHMT", uppg_sv="Folatoberoende återmetylering", uppg_en="Folate-independent remethylation",
        form_sv="Betain (TMG); cholin som förstadium", form_en="Betaine (TMG); choline as precursor",
        kofakt_sv="Zink", kofakt_en="Zinc",
        obs_sv="Höga betaindoser har i studier höjt LDL och totalkolesterol. Dosering under uppföljning.",
        obs_en="High betaine doses have raised LDL and total cholesterol in trials. Dose under follow-up.",
    ),
    dict(
        nod="CBS", uppg_sv="Inleder transsulfurering", uppg_en="Initiates transsulfuration",
        form_sv="P5P (pyridoxal-5-fosfat)", form_en="P5P (pyridoxal-5-phosphate)",
        kofakt_sv="Hem, serin", kofakt_en="Haem, serine",
        obs_sv="Pyridoxin-HCl måste fosforyleras till P5P, ett steg som kan vara nedsatt. P5P är den form "
               "enzymet faktiskt använder.",
        obs_en="Pyridoxine HCl must be phosphorylated to P5P, a step that can be impaired. P5P is the form "
               "the enzyme actually uses.",
    ),
    dict(
        nod="AHCY", uppg_sv="Producerar homocystein ur SAH", uppg_en="Produces homocysteine from SAH",
        form_sv="Ingen substans — kräver NAD⁺", form_en="No substance — requires NAD⁺",
        kofakt_sv="Hårt bundet NAD⁺", kofakt_en="Tightly bound NAD⁺",
        obs_sv="Enzymet bär NAD⁺ som fast kofaktor. Samtidigt dränerar NAD⁺-prekursorer metylgrupper via "
               "NNMT. Sambandet går alltså åt båda hållen och gör noden särskilt olämplig att ignorera.",
        obs_en="The enzyme carries NAD⁺ as a fixed cofactor. At the same time NAD⁺ precursors drain methyl "
               "groups via NNMT. The relationship runs both ways, which makes this node particularly "
               "unwise to ignore.",
    ),
    dict(
        nod="MAT", uppg_sv="Bildar SAM ur metionin", uppg_en="Forms SAM from methionine",
        form_sv="Metionin; magnesium", form_en="Methionine; magnesium",
        kofakt_sv="ATP, magnesium", kofakt_en="ATP, magnesium",
        obs_sv="Utan tillräcklig SAM-produktion stannar både metylering och MTRR-återställningen.",
        obs_en="Without sufficient SAM production, both methylation and MTRR restoration stall.",
    ),
    dict(
        nod="SHMT", uppg_sv="Försörjer folatcykeln med enkolsenheter",
        uppg_en="Supplies the folate cycle with one-carbon units",
        form_sv="Serin, glycin", form_en="Serine, glycine",
        kofakt_sv="P5P", kofakt_en="P5P",
        obs_sv="Ofta förbisedd. Utan enkolsenheter finns inget att metylera folatet med.",
        obs_en="Frequently overlooked. Without one-carbon units there is nothing to methylate the folate with.",
    ),
]


def tabell(lang):
    sv = lang == "sv"
    head = ("<tr><th>Nod</th><th>Uppgift</th><th>Form som används</th><th>Kofaktorer</th></tr>" if sv
            else "<tr><th>Node</th><th>Function</th><th>Form used</th><th>Cofactors</th></tr>")
    rows = ""
    for n in NODER:
        rows += (f"<tr><td><strong>{n['nod']}</strong></td>"
                 f"<td>{H.escape(n['uppg_sv'] if sv else n['uppg_en'])}</td>"
                 f"<td>{H.escape(n['form_sv'] if sv else n['form_en'])}</td>"
                 f"<td>{H.escape(n['kofakt_sv'] if sv else n['kofakt_en'])}</td></tr>")
    noter = "".join(
        f"<p><strong>{n['nod']}.</strong> {n['obs_sv'] if sv else n['obs_en']}</p>" for n in NODER)
    return f"<table><thead>{head}</thead><tbody>{rows}</tbody></table>{noter}"


SV_SECTIONS = [
    ("varfor-form", "Varför formen avgör", [
        "Ett näringsämne på en förpackning är inte samma sak som ett näringsämne i ett enzym. Mellan burken "
        "och reaktionen ligger upptag, transport och i många fall ett eller flera omvandlingssteg — och det "
        "är i omvandlingsstegen individuella skillnader uppstår.",
        "Syntetisk folsyra måste reduceras och metyleras innan cellen kan använda den. Pyridoxin måste "
        "fosforyleras till P5P. Riboflavin måste omvandlas till FAD. Varje sådant steg är ett enzym, och "
        "varje enzym kan vara nedsatt av genetik, av bristande kofaktorer eller av belastning.",
        "Att välja en form som redan är aktiv innebär att kringgå ett steg som annars kan vara flaskhalsen. "
        "Det är hela poängen, och det är också gränsen för vad formvalet kan åstadkomma: det löser "
        "omvandlingsproblemet, inte alla andra problem.",
    ]),
    ("noderna", "Nod för nod", None),
    ("full-kompensation", "Partiell kompensation flyttar bara flaskhalsen", [
        "Här ligger textens egentliga innehåll, och det följer direkt av T1: i ett "
        "system av icke-substituerbara steg bestäms funktionen av det mest begränsande steget.",
        "Om folat är flaskhalsen och du tillför aktivt folat, stiger flödet — tills nästa steg blir "
        "begränsande. Har du samtidigt låg B12-status blir MTR den nya flaskhalsen. Är B6 lågt blir "
        "avloppet mot transsulfurering trångt och homocystein stannar kvar trots att återmetyleringen nu "
        "fungerar. Är riboflavin lågt arbetar MTHFR fortfarande under sin kapacitet även med tillfört folat.",
        "Konsekvensen är att partiell kompensation ofta ger en initial förbättring som planar ut. Patienten "
        "beskriver det som att tillskottet slutade fungera. Det gjorde det inte — flaskhalsen flyttade sig.",
        "Fullständig kompensation innebär att varje nod har det den kräver, i en form den kan använda, "
        "samtidigt. Vilka noder som faktiskt behöver stöd hos en enskild person avgörs av genotyp och av "
        "uppmätt intracellulär status — inte av att fylla på allt.",
    ]),
    ("mer-ar-inte-battre", "Mer är inte bättre, och åt båda hållen", [
        "Aktiv form är inte automatiskt rätt val. Utan MTHFR-variant finns ingen flaskhals att kringgå, och "
        "höga doser aktivt folat kan då driva metyleringen fortare än nedströms kapacitet medger — med ökat "
        "uttag av metylgrupper, metionin, B12, B6 och cholin som följd.",
        "Samma logik gäller metyldonatorer generellt. Den som redan har ett välförsörjt system får inget "
        "tillskott av mer; den som har ett belastat system kan få symtom av att belastningen ökar utan att "
        "avloppen samtidigt öppnas.",
        "Det är därför frågan aldrig är <em>vilket tillskott är bäst</em> utan <em>vad begränsar just den "
        "här personen</em>.",
    ]),
    ("uppfoljning", "Vad som ska mätas, och när", [
        "Homocystein är den billigaste och mest tillgängliga avläsningen av om kompensationen fungerar. Den "
        "är trubbig — den säger inte vilken nod som klämmer — men den svarar på om flödet förbättrats.",
        "Omvärdera efter åtta till tolv veckor. Faller homocystein men symtomen kvarstår, ligger "
        "förklaringen sannolikt någon annanstans än i metyleringen. Faller det inte alls trots adekvat "
        "form och dos, är antagandet om vilken nod som var bindande sannolikt fel.",
        "Intracellulär status komplettera bilden där serum är otillräckligt, och genotyp förklarar varför "
        "en viss form fungerar bättre för en person än för en annan.",
    ]),
    ("granser", "Vad denna text inte gör anspråk på", [
        "Den anger inga doser. Rätt dos beror på genotyp, utgångsstatus, kost, läkemedel och samtidiga "
        "tillstånd, och kan inte generaliseras i en artikel.",
        "Den beskriver inte någon sammansättning. Vilka noder som ska stödjas samtidigt hos en enskild "
        "patient är en klinisk bedömning, och den bedömningen görs efter mätning.",
        "Och den påstår inte att formvalet ensamt avgör utfallet. Formen löser omvandlingssteget. Om "
        "problemet sitter i reduktionskapacitet, i belastning eller i något helt annat system, hjälper "
        "ingen form i världen.",
    ]),
]

EN_SECTIONS = [
    ("why-form", "Why the form determines the outcome", [
        "A nutrient on a label is not the same as a nutrient in an enzyme. Between the bottle and the "
        "reaction lie absorption, transport and in many cases one or more conversion steps — and it is in "
        "the conversion steps that individual differences arise.",
        "Synthetic folic acid must be reduced and methylated before the cell can use it. Pyridoxine must be "
        "phosphorylated to P5P. Riboflavin must be converted to FAD. Each such step is an enzyme, and every "
        "enzyme can be impaired by genetics, by missing cofactors or by load.",
        "Choosing a form that is already active means bypassing a step that might otherwise be the "
        "bottleneck. That is the entire point — and also the limit of what form selection can achieve: it "
        "solves the conversion problem, not every other problem.",
    ]),
    ("nodes", "Node by node", None),
    ("full-compensation", "Partial compensation only moves the bottleneck", [
        "This is the real content of the text, and it follows directly from "
        "T1: in a system of non-substitutable steps, function is determined "
        "by the most limiting step.",
        "If folate is the bottleneck and you supply active folate, flux rises — until the next step becomes "
        "limiting. If B12 status is low, MTR becomes the new bottleneck. If B6 is low, the drain toward "
        "transsulfuration is narrow and homocysteine remains despite remethylation now working. If "
        "riboflavin is low, MTHFR still operates below capacity even with folate supplied.",
        "The consequence is that partial compensation often produces an initial improvement that plateaus. "
        "The patient describes it as the supplement having stopped working. It did not — the bottleneck moved.",
        "Full compensation means every node has what it requires, in a form it can use, simultaneously. "
        "Which nodes actually need support in a given person is determined by genotype and measured "
        "intracellular status — not by supplying everything.",
    ]),
    ("more-is-not-better", "More is not better, and it runs both ways", [
        "An active form is not automatically the right choice. Without an MTHFR variant there is no "
        "bottleneck to bypass, and high doses of active folate can then drive methylation faster than "
        "downstream capacity allows — increasing the draw on methyl groups, methionine, B12, B6 and choline.",
        "The same logic applies to methyl donors generally. Someone with a well-supplied system gains "
        "nothing from more; someone with a loaded system can develop symptoms from increasing the load "
        "without opening the drains at the same time.",
        "This is why the question is never <em>which supplement is best</em> but <em>what is limiting this "
        "particular person</em>.",
    ]),
    ("follow-up", "What to measure, and when", [
        "Homocysteine is the cheapest and most accessible readout of whether compensation is working. It is "
        "blunt — it does not identify which node is restricting — but it answers whether flux has improved.",
        "Reassess after eight to twelve weeks. If homocysteine falls but symptoms persist, the explanation "
        "probably lies somewhere other than methylation. If it does not fall at all despite adequate form "
        "and dose, the assumption about which node was binding is probably wrong.",
        "Intracellular status completes the picture where serum is insufficient, and genotype explains why "
        "a given form works better for one person than another.",
    ]),
    ("limits", "What this text does not claim", [
        "It gives no doses. The right dose depends on genotype, baseline status, diet, medication and "
        "concurrent conditions, and cannot be generalised in an article.",
        "It describes no composition. Which nodes should be supported simultaneously in an individual "
        "patient is a clinical judgement, and that judgement follows measurement.",
        "And it does not claim that form selection alone determines the outcome. Form solves the conversion "
        "step. If the problem lies in reducing capacity, in load, or in an entirely different system, no "
        "form in the world will help.",
    ]),
]

SV_FAQ = [
    ("Vilken form av folat ska jag ta?",
     "5-MTHF (metylfolat) är den form cellen använder direkt och kringgår MTHFR-steget. Det är särskilt "
     "relevant vid MTHFR-variant, där omvandlingen av syntetisk folsyra sker långsamt och ofullständigt. "
     "Men aktivt folat är inte automatiskt rätt för alla: utan variant finns ingen flaskhals att kringgå, "
     "och höga doser kan då driva metyleringen fortare än nedströms kapacitet medger."),
    ("Vilken form av B6 och B12 är rätt?",
     "B6 bör ges som P5P, pyridoxal-5-fosfat, eftersom det är den form enzymet använder — pyridoxin-HCl "
     "måste först fosforyleras, ett steg som kan vara nedsatt. B12 förekommer som cyano-, hydroxo-, metyl- "
     "och adenosylkobalamin, och formerna skiljer sig i stabilitet, halveringstid och hur de tas in i "
     "cellens kobalaminmetabolism. Vilken som är lämplig avgörs individuellt."),
    ("Varför slutade mitt tillskott fungera efter ett tag?",
     "Sannolikt gjorde det inte det — flaskhalsen flyttade sig. När det mest begränsande steget korrigeras "
     "stiger flödet tills nästa steg blir begränsande. Partiell kompensation ger därför ofta en initial "
     "förbättring som planar ut. Fullständig kompensation innebär att varje nod som behöver stöd får det "
     "samtidigt, i en form den kan använda."),
    ("Räcker det med en bra multivitamin?",
     "Sällan, av två skäl. Den innehåller ofta inaktiva former som förutsätter att omvandlingsstegen "
     "fungerar, och den doserar efter genomsnitt snarare än efter vad som begränsar just dig. Den kan "
     "dessutom tillföra rikligt av det du inte behöver."),
    ("Hur vet jag om kompensationen fungerar?",
     "Mät homocystein före start och efter åtta till tolv veckor. Det är en trubbig men billig avläsning av "
     "om flödet förbättrats. Faller värdet inte alls trots adekvat form och dos är antagandet om vilken nod "
     "som var bindande sannolikt fel."),
]

EN_FAQ = [
    ("Which form of folate should I take?",
     "5-MTHF (methylfolate) is the form the cell uses directly and bypasses the MTHFR step. That is "
     "particularly relevant with an MTHFR variant, where conversion of synthetic folic acid is slow and "
     "incomplete. But active folate is not automatically right for everyone: without a variant there is no "
     "bottleneck to bypass, and high doses can then drive methylation faster than downstream capacity allows."),
    ("Which form of B6 and B12 is correct?",
     "B6 should be given as P5P, pyridoxal-5-phosphate, because that is the form the enzyme uses — "
     "pyridoxine HCl must first be phosphorylated, a step that can be impaired. B12 occurs as cyano-, "
     "hydroxo-, methyl- and adenosylcobalamin, and the forms differ in stability, half-life and how they "
     "enter cellular cobalamin metabolism. Which is appropriate is determined individually."),
    ("Why did my supplement stop working after a while?",
     "It probably did not — the bottleneck moved. When the most limiting step is corrected, flux rises "
     "until the next step becomes limiting. Partial compensation therefore often produces an initial "
     "improvement that plateaus. Full compensation means every node needing support receives it "
     "simultaneously, in a form it can use."),
    ("Is a good multivitamin enough?",
     "Rarely, for two reasons. It often contains inactive forms that assume the conversion steps work, and "
     "it doses to an average rather than to what limits you specifically. It may also supply plenty of what "
     "you do not need."),
    ("How do I know whether compensation is working?",
     "Measure homocysteine before starting and after eight to twelve weeks. It is a blunt but inexpensive "
     "readout of whether flux has improved. If it does not fall at all despite adequate form and dose, the "
     "assumption about which node was binding is probably wrong."),
]


def bygg(lang):
    sv = lang == "sv"
    url, other = (SV_URL, EN_URL) if sv else (EN_URL, SV_URL)
    secs = SV_SECTIONS if sv else EN_SECTIONS
    faq = SV_FAQ if sv else EN_FAQ

    anchors = [(a, t.split("—")[0].split(",")[0].strip()[:30]) for a, t, _ in secs]
    anchors.append(("faq", "Vanliga frågor" if sv else "FAQ"))

    body = ""
    for a, t, ps in secs:
        inner = tabell(lang) if ps is None else "".join(f"<p>{p}</p>" for p in ps)
        body += f'<section id="{a}"><h2>{t}</h2>{inner}</section>'

    from build_new_sections import faq_html as sv_faq_html, faq_schema as sv_faq_schema
    from build_content_en import faq_html as en_faq_html, faq_schema as en_faq_schema
    faq_html = sv_faq_html if sv else en_faq_html
    faq_schema = sv_faq_schema if sv else en_faq_schema
    hero_f, band_f, toc_f = (sv_hero, sv_band, sv_toc) if sv else (en_hero, en_band, en_toc)

    if sv:
        titel = "Rätt form av tillskott — och full kompensation av homocysteincykeln | MediBalans"
        desc = ("5-MTHF, P5P, riboflavin, betain, zink och magnesium — varje nod i metioninscykeln kräver sin "
                "form och sina kofaktorer. Partiell kompensation flyttar bara flaskhalsen. Vad fullständig "
                "kompensation innebär, och vad som ska mätas.")
        h1, h1em = "Rätt form — och ", "full kompensation."
        lead = ("Ett näringsämne på en förpackning är inte samma sak som ett näringsämne i ett enzym. Mellan "
                "burken och reaktionen ligger omvandlingssteg, och det är där individuella skillnader uppstår.")
        kort = ("<strong>Kort svar:</strong> välj den form som redan är aktiv där ett omvandlingssteg kan "
                "vara nedsatt — 5-MTHF för folat, P5P för B6, riboflavin för MTHFR. Men formvalet räcker inte. "
                "Korrigerar du en nod stiger flödet tills nästa nod blir begränsande, och patienten upplever "
                "att tillskottet slutade fungera. Fullständig kompensation innebär att varje nod som behöver "
                "stöd får det samtidigt — och vilka de är avgörs av genotyp och mätning, inte av att fylla på allt.")
        eyebrow = "Klinisk notering · Metylering"
        band_a, band_b = "Rätt form", "börjar med rätt fråga"
        band_p = ("Vilken form och vilken nod som är relevant för dig avgörs av genotyp och intracellulär "
                  "status. Det är en mätning, inte en gissning.")
        src_head, lbl_other = "Vidare läsning", "English"
    else:
        titel = "Correct supplement forms — and full compensation of the homocysteine cycle | MediBalans"
        desc = ("5-MTHF, P5P, riboflavin, betaine, zinc and magnesium — every node in the methionine cycle "
                "requires its own form and cofactors. Partial compensation only moves the bottleneck. What "
                "full compensation means, and what to measure.")
        h1, h1em = "Correct form — and ", "full compensation."
        lead = ("A nutrient on a label is not the same as a nutrient in an enzyme. Between the bottle and the "
                "reaction lie conversion steps, and that is where individual differences arise.")
        kort = ("<strong>In short:</strong> choose the already-active form wherever a conversion step may be "
                "impaired — 5-MTHF for folate, P5P for B6, riboflavin for MTHFR. But form alone is not enough. "
                "Correct one node and flux rises until the next node becomes limiting, and the patient "
                "experiences the supplement as having stopped working. Full compensation means every node "
                "needing support receives it simultaneously — and which those are is determined by genotype "
                "and measurement, not by supplying everything.")
        eyebrow = "Clinical note · Methylation"
        band_a, band_b = "The right form", "begins with the right question"
        band_p = ("Which form and which node is relevant for you is determined by genotype and intracellular "
                  "status. That is a measurement, not a guess.")
        src_head, lbl_other = "Further reading", "Svenska"

    schema = [
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@graph": [
                {"@type": "MedicalWebPage", "@id": url + "#page", "url": url, "name": titel,
                 "inLanguage": "sv-SE" if sv else "en-GB",
                 "datePublished": "2026-07-29", "dateModified": "2026-07-29",
                 "audience": {"@type": "Patient"}, "author": {"@id": AUTHOR_ID},
                 "provider": ORG, "publisher": ORG}]}, ensure_ascii=False) + "</script>",
        faq_schema(url, faq),
    ]

    booking = "/#booking" if sv else "/en/#booking"
    hcy = "/homocystein/" if sv else "/en/homocysteine/"
    methyl = "/methyldetox/" if sv else "/en/methylation-test/"
    cma = "/cma/" if sv else "/en/cellular-nutrient-analysis/"

    innehall = f"""
{hero_f(eyebrow, h1, h1em, lead,
        f'<a class="btn-p" href="{booking}">' + ("Boka konsultation" if sv else "Book a consultation") + '</a>'
        f'<a class="btn-s" href="{methyl}">MethylDetox</a>',
        ("Klinisk notering. Inga doser anges — de avgörs individuellt efter mätning." if sv
         else "Clinical note. No doses are given — they are determined individually after measurement."),
        [("8", "Noder" if sv else "Nodes"), ("5-MTHF", "Aktivt folat" if sv else "Active folate"),
         ("P5P", "Aktivt B6" if sv else "Active B6"), ("8–12", "Veckor till omtest" if sv else "Weeks to retest")])}
{toc_f(anchors)}
<div class="container sec-body">
<section><p class="lead-p">{kort}</p></section>
{body}
<section id="faq"><h2>{"Vanliga" if sv else "Frequently asked"} <em>{"frågor" if sv else "questions"}</em></h2>{faq_html(faq)}</section>
<section id="vidare"><h2>{src_head}</h2>
<p><a href="{hcy}">{"Homocystein — ett system, inte ett stickprov" if sv else "Homocysteine — a system, not a snapshot"} →</a> · <a href="{cma}">CMA</a> · <a href="{other}">{lbl_other}</a></p></section>
</div>
{band_f(band_a, band_b, band_p)}
"""
    if sv:
        html = sv_page(titel, desc, url, schema, innehall)
        m = re.search(r'<link rel="alternate" hreflang="sv" href="[^"]+">', html)
        if m:
            html = html.replace(m.group(0), m.group(0) + f'\n<link rel="alternate" hreflang="en" href="{other}">', 1)
        return html
    return en_page(titel, desc, url, other, schema, innehall)


if __name__ == "__main__":
    for lang, rel in (("sv", "ratt-form-av-tillskott/index.html"),
                      ("en", "en/supplement-forms/index.html")):
        p = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(bygg(lang))
        print(f"   {rel}")
