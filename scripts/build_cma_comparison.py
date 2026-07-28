# -*- coding: utf-8 -*-
"""
MediBalans · CMA vs SpectraCell — jämförande klinisk notering (SV + EN)
=======================================================================
RAMVERK (beslutat med Dr Mario):
  Artikeln vinner på metodologi och upplösning, och medger öppet den
  delade evidensposition som båda testerna har. Skälet är dubbelt.

  1. Molinas policy namnger ordagrant "SpectraCell, Cell Science Systems
     cell micronutrient assay, and ExaTest" som icke ersättningsbara.
     Blue Cross-policyerna behandlar intracellulär mikronäringsanalys som
     KATEGORI. CMA ligger inom den kategorin. Ett påstående om att CMA
     är validerat där SpectraCell är experimentellt vore falskt och
     kontrollerbart på nittio sekunder.

  2. Jämförande reklam som namnger konkurrent omfattas av
     marknadsföringslagen. Varje påstående måste kunna substantieras.

  Det som DÄREMOT är sant och substantierbart:
    · SpectraCell: depletionsdesign i optimerat medium, 31 analyter
    · CMA: repletionsdesign i patientens EGET serum, 55 analyter
  Skillnaden i frågeställning är reell och kliniskt relevant.

Kör från repo-roten:  python3 scripts/build_cma_comparison.py
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_new_sections import page, hero, toc, band, faq_html, faq_schema, ROOT, BASE

ORG = {"@id": f"{BASE}/#organization"}
AUTHOR_ID = f"{BASE}/#mario-anthis"

SV_URL = f"{BASE}/mikronaringstest-jamforelse/"
EN_URL = f"{BASE}/en/micronutrient-test-comparison/"

# ─────────────────────────────────────────────────────────── SVENSKA
SV_SECTIONS = [
    ("fragan", "Två test, två olika frågor", [
        "Både Cellular Micronutrient Assay (CMA) från Cell Science Systems och SpectraCells Micronutrient Test bygger på samma grundidé: att mäta näringsstatus i vita blodkroppar i stället för i serum. Rationalen är god. Serumkoncentrationen speglar transport, inte funktion — en patient kan ha normalt magnesium, B12 eller zink i blodet och samtidigt ha otillräcklig tillgång inne i cellen, där de enzymatiska processerna faktiskt äger rum.",
        "Där likheten slutar är i hur mätningen görs. De två analyserna ställer olika frågor till cellen, och det avgör vad svaret kan användas till.",
    ]),
    ("depletion", "SpectraCell: depletion i optimerat medium", [
        "SpectraCells metod är en lymfocytproliferationsanalys av depletionstyp. Patientens lymfocyter placeras i ett odlingsmedium som innehåller optimala nivåer av samtliga näringsämnen. Ett enskilt näringsämne avlägsnas därefter ur mediet, och celltillväxten mäts och jämförs mot tillväxten vid fullständigt medium. Uteblir tillväxten tolkas det som otillräcklig funktionell status för det ämnet. Panelen omfattar 31 analyter.",
        "Designen är logiskt konsekvent, men den ställer frågan: hur reagerar dessa celler när ett ämne saknas i en i övrigt idealisk miljö? Det är inte samma sak som att fråga hur cellerna fungerar i patientens egen miljö.",
    ]),
    ("repletion", "CMA: repletion i patientens eget serum", [
        "CMA vänder på designen. Lymfocyter separeras ur patientens helblod och patientens <em>eget serum</em> tillsätts tillbaka till cellerna. Cellerna stimuleras med ett mitogen och en baslinje för proliferation registreras — alltså hur patientens celler faktiskt presterar i patientens egen biokemiska miljö. Därefter tillsätts mikronäringsämnen och proliferationen jämförs mot den individuella baslinjen. Panelen omfattar 55 analyter.",
        "Två saker skiljer detta från depletionsdesignen. Mätningen sker i autologt serum, vilket innebär att patientens faktiska miljö — inklusive det som är otillräckligt i den — ingår i testförhållandet i stället för att korrigeras bort. Och frågan som ställs är den kliniskt operativa: förbättras cellens funktion om detta ämne tillförs?",
        "Den frågan översätts direkt till ett behandlingsbeslut. Ett svar som visar att proliferationen stiger när ett ämne tillförs är ett argument för att tillföra det ämnet. Ett depletionssvar besvarar en angränsande men annan fråga.",
    ]),
    ("skillnaderna", "Vad skillnaderna innebär praktiskt", [
        "Analytantalet — 55 mot 31 — är den enklaste skillnaden och den minst intressanta. Den avgörande skillnaden är referensramen. När baslinjen utgörs av patientens egna celler i patientens eget serum blir varje resultat individuellt kalibrerat. Jämförelsen sker inte mot ett populationsmedelvärde utan mot personen själv.",
        "Det har betydelse vid just de tillstånd där testet är aktuellt: långvarig trötthet, nedsatt återhämtning, misstänkt metabol flaskhals. I dessa fall är frågan sällan om patienten avviker från befolkningen, utan om det finns ett åtgärdbart underskott i just den här personens cellulära förutsättningar.",
    ]),
    ("evidens", "Var båda testerna står — utan omskrivningar", [
        "Här bör man vara rak, och det tjänar ingenting på att undvika det: <strong>ingen av dessa analyser är etablerad standarddiagnostik, och båda bedöms likartat av amerikanska betalare.</strong>",
        "Molinas policy för intracellulär mikronäringsanalys namnger uttryckligen SpectraCell, Cell Science Systems cellulära mikronäringsanalys och ExaTest som analyser som inte uppfyller kriterierna för ersättning. Blue Cross Blue Shields policyer behandlar intracellulär mikronäringsanalys som en kategori och bedömer den som experimentell. Ingen av analyserna är FDA-godkänd; båda är laboratorieutvecklade tester.",
        "Att hävda att CMA skulle stå utanför den bedömningen vore felaktigt. Det som skiljer analyserna är metodologisk design och upplösning — inte evidensstatus. Den som säljer intracellulär mikronäringsanalys som validerad rutindiagnostik tar sig friheter med underlaget.",
        "Vad betyder det då kliniskt? Att analysen är ett underlag bland flera, inte ett facit. Den används hos oss när den kliniska frågan är formulerad först, och den läses tillsammans med anamnes, konventionella prover och övriga fynd. Den ersätter inte serumprover — den besvarar en annan fråga än de gör.",
    ]),
    ("val", "När respektive analys är motiverad", [
        "Om frågan är om ett näringsämne saknas i kroppen i grov mening är konventionella serumprover billigare, snabbare och tillräckliga. De ska göras först. Ferritin, B12, folat, D-vitamin och kalcium besvarar de flesta frågor som ställs i klinisk vardag.",
        "Om frågan är varför en patient med normala serumvärden ändå inte återhämtar sig, tillför en funktionell analys någonting som serum inte kan ge. Där är CMA:s repletionsdesign i autologt serum enligt vår bedömning den mer användbara konstruktionen, därför att den svarar på om tillförsel gör skillnad för just den patienten.",
        "Det är också skälet till att vi arbetar med CMA och inte med SpectraCell. Det är ett metodval, inte ett påstående om att den ena analysen är validerad och den andra inte.",
    ]),
]

SV_FAQ = [
    ("Vad är skillnaden mellan CMA och SpectraCells mikronäringstest?",
     "Båda mäter näringsstatus i vita blodkroppar i stället för i serum, men de använder motsatt design. SpectraCell använder depletion: cellerna odlas i ett optimerat medium, ett näringsämne avlägsnas och minskad tillväxt tolkas som otillräcklig status. Panelen omfattar 31 analyter. CMA använder repletion i patientens eget serum: en individuell baslinje för celltillväxt registreras, därefter tillsätts näringsämnen och förbättringen mäts mot den baslinjen. Panelen omfattar 55 analyter."),
    ("Varför spelar det roll att CMA använder patientens eget serum?",
     "Därför att referensramen blir individuell. När cellerna mäts i patientens egen biokemiska miljö ingår patientens faktiska förutsättningar i testförhållandet i stället för att korrigeras bort av ett optimerat medium. Frågan som besvaras blir då den kliniskt operativa: förbättras cellens funktion om detta ämne tillförs? Det svaret översätts direkt till ett behandlingsbeslut."),
    ("Är CMA vetenskapligt validerat och godkänt?",
     "Nej, inte som etablerad standarddiagnostik, och det gäller båda analyserna. Molinas policy namnger uttryckligen både SpectraCell och Cell Science Systems cellulära mikronäringsanalys som analyser som inte uppfyller kriterierna för ersättning, och Blue Cross Blue Shield bedömer intracellulär mikronäringsanalys som kategori som experimentell. Ingen av analyserna är FDA-godkänd; båda är laboratorieutvecklade tester. Analysen används därför som ett underlag i en klinisk helhetsbedömning, aldrig som ensamt beslutsunderlag."),
    ("Ersätter CMA vanliga blodprover?",
     "Nej. Konventionella serumprover är billigare, snabbare och besvarar de flesta frågor som ställs i klinisk vardag. De ska göras först. En funktionell analys tillför något först när serumvärdena är normala men patienten ändå inte återhämtar sig — då besvarar den en annan fråga än serumprovet gör."),
    ("Varför använder MediBalans CMA och inte SpectraCell?",
     "Det är ett metodval. Repletionsdesignen i autologt serum svarar på om tillförsel av ett ämne förbättrar funktionen hos just den patienten, vilket är den fråga ett behandlingsbeslut vilar på. Panelen är dessutom bredare, 55 analyter mot 31. Det är inte ett påstående om att den ena analysen är validerad och den andra inte — båda befinner sig i samma evidensposition."),
]

SV_SOURCES = [
    "Molina Healthcare. Clinical Policy: Intracellular Micronutrient Analysis (G2099) — namnger SpectraCell, Cell Science Systems cellular micronutrient assay och ExaTest.",
    "Blue Cross Blue Shield, FEP Medical Policy 2.04.73 — Intracellular Micronutrient Analysis. Bedöms som investigational.",
    "Cell Science Systems. Cellular Nutrition Assays — metodbeskrivning: lymfocyter i autologt serum, mitogenstimulering, baslinjeproliferation och repletion.",
    "SpectraCell Laboratories. Micronutrient Test — metodbeskrivning: lymfocytproliferationsanalys med depletion ur optimerat medium.",
]

# ─────────────────────────────────────────────────────────── ENGELSKA
EN_SECTIONS = [
    ("question", "Two tests, two different questions", [
        "Both the Cellular Micronutrient Assay (CMA) from Cell Science Systems and SpectraCell's Micronutrient Test rest on the same premise: measuring nutrient status inside white blood cells rather than in serum. The rationale is sound. Serum concentration reflects transport, not function — a patient can have normal magnesium, B12 or zinc in blood while having insufficient availability inside the cell, where the enzymatic processes actually occur.",
        "The similarity ends at how the measurement is made. The two assays ask the cell different questions, and that determines what the answer can be used for.",
    ]),
    ("depletion", "SpectraCell: depletion in an optimised medium", [
        "SpectraCell's method is a lymphocyte proliferation assay of depletion type. The patient's lymphocytes are placed in a culture medium containing optimal levels of all nutrients. A single nutrient is then removed from the medium, and cell growth is measured against growth in the complete medium. Failure to grow is interpreted as insufficient functional status for that nutrient. The panel covers 31 analytes.",
        "The design is internally consistent, but the question it asks is: how do these cells respond when one substance is absent from an otherwise ideal environment? That is not the same as asking how the cells perform in the patient's own environment.",
    ]),
    ("repletion", "CMA: repletion in the patient's own serum", [
        "CMA inverts the design. Lymphocytes are separated from the patient's whole blood and the patient's <em>own serum</em> is added back to the cells. The cells are stimulated with a mitogen and a baseline proliferation rate is recorded — how the patient's cells actually perform in the patient's own biochemical environment. Micronutrients are then added and proliferation is compared against that individual baseline. The panel covers 55 analytes.",
        "Two things separate this from the depletion design. Measurement occurs in autologous serum, meaning the patient's actual milieu — including whatever is insufficient in it — forms part of the test condition rather than being corrected away. And the question asked is the clinically operative one: does cellular function improve if this substance is supplied?",
        "That question translates directly into a treatment decision. A result showing proliferation rising when a nutrient is added is an argument for supplying that nutrient. A depletion result answers an adjacent but different question.",
    ]),
    ("implications", "What the differences mean in practice", [
        "The analyte count — 55 against 31 — is the simplest difference and the least interesting. The decisive difference is the frame of reference. When the baseline consists of the patient's own cells in the patient's own serum, every result is individually calibrated. The comparison is not against a population mean but against the person themselves.",
        "This matters in precisely the conditions where the test is considered: prolonged fatigue, impaired recovery, suspected metabolic bottleneck. In those cases the question is rarely whether the patient deviates from the population, but whether there is a correctable deficit in this particular person's cellular conditions.",
    ]),
    ("evidence", "Where both tests stand — without euphemism", [
        "This deserves plain statement, and there is nothing to gain by avoiding it: <strong>neither assay is established standard diagnostics, and both are assessed similarly by US payers.</strong>",
        "Molina's policy on intracellular micronutrient analysis explicitly names SpectraCell, the Cell Science Systems cellular micronutrient assay and ExaTest as not meeting coverage criteria. Blue Cross Blue Shield policies treat intracellular micronutrient analysis as a category and consider it investigational. Neither assay is FDA-approved; both are laboratory-developed tests.",
        "Claiming that CMA falls outside that assessment would be false. What separates the assays is methodological design and resolution — not evidentiary status. Anyone selling intracellular micronutrient analysis as validated routine diagnostics is taking liberties with the evidence.",
        "What does that mean clinically? That the assay is one input among several, not a verdict. We use it when the clinical question has been formulated first, and we read it alongside history, conventional tests and other findings. It does not replace serum testing — it answers a different question than serum testing does.",
    ]),
    ("choice", "When each assay is warranted", [
        "If the question is whether a nutrient is missing in gross terms, conventional serum testing is cheaper, faster and sufficient. It should be done first. Ferritin, B12, folate, vitamin D and calcium answer most questions that arise in everyday practice.",
        "If the question is why a patient with normal serum values still fails to recover, a functional assay adds something serum cannot provide. There, in our assessment, CMA's repletion design in autologous serum is the more useful construction, because it answers whether supplementation makes a difference for that particular patient.",
        "That is also why we work with CMA rather than SpectraCell. It is a methodological choice, not a claim that one assay is validated and the other is not.",
    ]),
]

EN_FAQ = [
    ("What is the difference between CMA and SpectraCell's micronutrient test?",
     "Both measure nutrient status inside white blood cells rather than in serum, but they use opposite designs. SpectraCell uses depletion: cells are cultured in an optimised medium, one nutrient is removed, and reduced growth is interpreted as insufficient status. The panel covers 31 analytes. CMA uses repletion in the patient's own serum: an individual baseline for cell growth is recorded, then nutrients are added and improvement is measured against that baseline. The panel covers 55 analytes."),
    ("Why does it matter that CMA uses the patient's own serum?",
     "Because the frame of reference becomes individual. When cells are measured in the patient's own biochemical environment, the patient's actual conditions form part of the test rather than being corrected away by an optimised medium. The question answered is then the clinically operative one: does cellular function improve if this substance is supplied? That answer translates directly into a treatment decision."),
    ("Is CMA scientifically validated and approved?",
     "No, not as established standard diagnostics, and this applies to both assays. Molina's policy explicitly names both SpectraCell and the Cell Science Systems cellular micronutrient assay as not meeting coverage criteria, and Blue Cross Blue Shield considers intracellular micronutrient analysis as a category investigational. Neither assay is FDA-approved; both are laboratory-developed tests. The assay is therefore used as one input in an overall clinical assessment, never as a sole basis for decisions."),
    ("Does CMA replace ordinary blood tests?",
     "No. Conventional serum tests are cheaper, faster and answer most questions arising in everyday practice. They should be done first. A functional assay adds something only when serum values are normal but the patient still fails to recover — it then answers a different question than the serum test does."),
    ("Why does MediBalans use CMA rather than SpectraCell?",
     "It is a methodological choice. The repletion design in autologous serum answers whether supplying a substance improves function in that specific patient, which is the question a treatment decision rests on. The panel is also broader, 55 analytes against 31. This is not a claim that one assay is validated and the other is not — both occupy the same evidentiary position."),
]


def build(lang):
    is_sv = lang == "sv"
    url, other = (SV_URL, EN_URL) if is_sv else (EN_URL, SV_URL)
    secs = SV_SECTIONS if is_sv else EN_SECTIONS
    faq = SV_FAQ if is_sv else EN_FAQ

    anchors = [(a, t.split(":")[0].split("—")[0].strip()) for a, t, _ in secs]
    anchors.append(("faq", "Vanliga frågor" if is_sv else "FAQ"))

    body = "".join(
        f'<section id="{a}"><h2>{t}</h2>' + "".join(f"<p>{p}</p>" for p in ps) + "</section>"
        for a, t, ps in secs)

    if is_sv:
        title = "CMA eller SpectraCell? Två intracellulära mikronäringstest jämförda | MediBalans"
        desc = ("CMA och SpectraCell mäter båda näringsstatus i vita blodkroppar men använder motsatt design — "
                "repletion i patientens eget serum mot depletion i optimerat medium, 55 analyter mot 31. "
                "En metodologisk jämförelse med öppen redovisning av evidensläget.")
        h1, h1em = "CMA eller SpectraCell? ", "Två test, två olika frågor."
        lead = ("Båda mäter näringsstatus inuti cellen i stället för i serum. Skillnaden ligger inte i ambitionen "
                "utan i konstruktionen — och den avgör vad svaret kan användas till.")
        kicker = "Klinisk notering · Mikronäringsdiagnostik"
        sources = SV_SOURCES
        src_head = "Källor"
        note = ("<strong>Om denna text.</strong> Detta är en metodologisk jämförelse av två laboratorieanalyser. "
                "Den redovisar öppet att ingen av analyserna är etablerad standarddiagnostik och att båda bedöms "
                "likartat av amerikanska betalare. Jämförelsen avser konstruktion och upplösning, inte evidensstatus.")
        band_a, band_b = "Mätning", "före tolkning"
        band_p = ("Vilken analys som är motiverad avgörs av den kliniska frågan — och konventionella prover ska "
                  "vara gjorda först. En inledande konsultation avgör vad som faktiskt tillför något.")
    else:
        title = "CMA or SpectraCell? Two intracellular micronutrient tests compared | MediBalans"
        desc = ("CMA and SpectraCell both measure nutrient status inside white blood cells but use opposite designs — "
                "repletion in the patient's own serum versus depletion in an optimised medium, 55 analytes against 31. "
                "A methodological comparison with the evidence position stated openly.")
        h1, h1em = "CMA or SpectraCell? ", "Two tests, two different questions."
        lead = ("Both measure nutrient status inside the cell rather than in serum. The difference lies not in the "
                "ambition but in the construction — and that determines what the answer can be used for.")
        kicker = "Clinical note · Micronutrient diagnostics"
        sources = SV_SOURCES
        src_head = "Sources"
        note = ("<strong>About this text.</strong> This is a methodological comparison of two laboratory assays. "
                "It states openly that neither assay is established standard diagnostics and that both are assessed "
                "similarly by US payers. The comparison concerns construction and resolution, not evidentiary status.")
        band_a, band_b = "Measurement", "before interpretation"
        band_p = ("Which assay is warranted depends on the clinical question — and conventional tests should be done "
                  "first. An initial consultation determines what actually adds something.")

    schema = [
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@graph": [
                {"@type": "MedicalWebPage", "@id": url + "#page", "url": url, "name": title,
                 "inLanguage": "sv-SE" if is_sv else "en-GB",
                 "datePublished": "2026-07-28", "dateModified": "2026-07-28",
                 "audience": {"@type": "Patient"},
                 "author": {"@id": AUTHOR_ID}, "provider": ORG, "publisher": ORG},
            ]}, ensure_ascii=False) + "</script>",
        faq_schema(url, faq),
    ]

    booking = "/#booking" if is_sv else "/en/#booking"
    cma_link = "/cma/" if is_sv else "/en/cellular-nutrient-analysis/"
    other_lbl = "English" if is_sv else "Svenska"

    content = f"""
{hero(kicker, h1, h1em, lead,
      f'<a class="btn-p" href="{booking}">{"Boka konsultation" if is_sv else "Book a consultation"}</a>'
      f'<a class="btn-s" href="{cma_link}">{"Om CMA" if is_sv else "About CMA"}</a>',
      "Klinisk notering — metodologisk jämförelse, inte marknadsföringspåstående." if is_sv
      else "Clinical note — methodological comparison, not a marketing claim.",
      [("55", "CMA-analyter"), ("31", "SpectraCell-analyter"),
       ("Autologt", "CMA-serum" if is_sv else "CMA serum"),
       ("2026", "Publicerad" if is_sv else "Published")])}
{toc(anchors)}
<div class="container sec-body">
<section><div class="box"><p>{note}</p></div></section>
{body}
<section id="faq"><h2>{"Vanliga" if is_sv else "Frequently asked"} <em>{"frågor" if is_sv else "questions"}</em></h2>{faq_html(faq)}</section>
<section id="kallor"><h2>{src_head}</h2><ol class="src">{"".join(f"<li>{s}</li>" for s in sources)}</ol>
<p style="margin-top:1.5rem"><a href="{cma_link}">{"Läs mer om CMA" if is_sv else "Read more about CMA"} →</a> · <a href="{other}">{other_lbl}</a></p></section>
</div>
{band(band_a, band_b, band_p)}
"""
    extra = "\n.src{font-size:.87rem;color:var(--text-mid)}.src li{margin-bottom:.6rem}"
    return page(title, desc, url, schema, content).replace("</style>", extra + "\n</style>", 1) \
        if is_sv else page(title, desc, url, schema, content).replace("</style>", extra + "\n</style>", 1)


def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)
    print("  ", rel, f"({len(content):,})")


if __name__ == "__main__":
    write("mikronaringstest-jamforelse/index.html", build("sv"))
    print("SV klar. EN byggs ur engelska skalet separat (se build_cma_comparison_en).")
