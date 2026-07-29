# -*- coding: utf-8 -*-
"""
MediBalans · Baby Balans — engelsk sida
========================================
/en/baby-balans/ var en KOPIA av den engelska startsidan: 96 % identisk,
noll förekomster av "Baby Balans", och canonical pekade på /en/ vilket
gjorde att sidan avindexerade sig själv. Den ersätts här av en riktig
sida — inte en översättning av en kopia.

Innehållet speglar den svenska sidan efter omskrivningen, med samma
kliniska hållning:

  · Folat ska tas. Frågan är formen, och den avgörs av genotyp.
  · Skadan knyts till HÖGA doser, inte till 400 µg perikonceptionellt.
  · C677T-bärare omvandlar långsamt och ofullständigt — inte "inte alls".
  · Explicit säkerhetsrad: sluta aldrig med folattillskott.
  · Methylfolat är inte heller rätt för alla — utan variant finns ingen
    flaskhals att kringgå, och höga doser kan driva metylering snabbare
    än nedströms kapacitet medger.
  · NIPT beskrivs korrekt som screening från vecka 10, inte diagnostik.

Kör:  python3 scripts/build_baby_balans_en.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from build_content_en import page, hero, toc, band, faq_html, faq_schema, BASE, ROOT

URL = f"{BASE}/en/baby-balans/"
SV_URL = f"{BASE}/baby-balans/"
ORG = {"@id": f"{BASE}/#organization"}
AUTHOR_ID = f"{BASE}/#mario-anthis"

SECTIONS = [
    ("why", "Healthy children begin before conception", [
        "Antenatal care starts at a positive pregnancy test. By then the most consequential window has "
        "already closed: the neural tube closes around day 28, egg maturation takes roughly 90 days, and "
        "spermatogenesis takes about 74. The biochemistry that shapes those processes is set months before "
        "anyone knows there is a pregnancy.",
        "Preconception assessment moves the starting point. Instead of optimising a pregnancy already "
        "underway, it establishes what the parents' biology can supply before conception — and corrects "
        "what is correctable while there is still time for correction to matter.",
        "This applies to both parents. Half the child's genome comes from the father, and paternal folate "
        "status, methylation capacity and DNA fragmentation are as relevant as the mother's. In practice "
        "they are almost never examined.",
    ]),
    ("folate", "Folic acid is the wrong form for many — test before you dose", [
        "Nearly every clinician gives the same advice: take folic acid when planning pregnancy. The "
        "principle is correct. Folate is critical for neural tube closure and DNA synthesis. "
        "<strong>You should take folate.</strong>",
        "But the advice assumes something that does not hold for everyone — that the body efficiently "
        "converts synthetic folic acid into the active form. In <strong>MTHFR C677T homozygotes</strong> "
        "the enzyme operates at 30–40 % of normal capacity. Conversion happens, but slowly and "
        "incompletely. At least 40 % of the population carries one or more MTHFR variants, and standard "
        "screening does not test for it.",
        "The consequence is not that folate is wrong. It is that the <em>form</em> and the <em>dose</em> "
        "are set blind, and that a normal serum folate can conceal insufficient availability inside the cell.",
    ]),
    ("answer", "Should I take folic acid if I carry an MTHFR variant?", [
        "<strong>Yes — never stop folate supplementation. But choose the right form.</strong> Synthetic "
        "folic acid requires the MTHFR enzyme to become 5-MTHF, the form the cell actually uses. At C677T "
        "homozygosity the enzyme runs at 30–40 % of normal capacity. At <em>high</em> intakes the "
        "conversion saturates and unmetabolised folic acid accumulates in blood — linked in the literature "
        "to masked B12 deficiency and adverse pregnancy outcomes. The clinically reasonable form for "
        "carriers is active <strong>methylfolate (5-MTHF)</strong>, dosed according to genotype and "
        "verified intracellular folate status.",
        "<strong>Important:</strong> periconceptional folate supplementation reduces the risk of neural "
        "tube defects by roughly 70 %, and the neural tube closes around day 28 — often before pregnancy "
        "is known. <strong>Never stop folate.</strong> Discuss the form with your midwife or doctor.",
        "<strong>But methylfolate is not right for everyone either.</strong> In someone with normal MTHFR "
        "function there is no bottleneck to bypass. High doses of active methylfolate can then drive "
        "methylation faster than downstream capacity allows — clinically seen as restlessness, "
        "irritability, headache and disturbed sleep — and increase the draw on methyl groups, and therefore "
        "the requirement for methionine, B12, B6 and choline. This is a clinical observation rather than a "
        "well-established dose–response relationship, but the pattern recurs often enough not to ignore.",
        "The conclusion runs both ways, and that is the point: <strong>the wrong form can harm whichever "
        "one you choose blindly.</strong> Carriers need active folate. Non-carriers rarely need it at high "
        "dose. Which one you are is settled by a test done once that holds for life — not by whichever "
        "bottle was nearest on the shelf.",
    ]),
    ("test", "Our clear recommendation: test methylation before you try to conceive — both of you", [
        "Folate, B12, choline and betaine all run through the same methylation machinery. Which form and "
        "which dose is right for you is determined by your genotype, not by a generic instruction on a "
        "label. It is a single measurement that holds for the rest of your life, and it costs a fraction "
        "of what a failed pregnancy does.",
        "<strong>Test both partners.</strong> Sperm quality and DNA fragmentation are affected by the same "
        "methylation pathways. Half the child's genome comes from the father, and his folate status is as "
        "relevant as the mother's — something that in practice is never investigated.",
    ]),
    ("nipt", "During pregnancy: NIPT", [
        "NIPT (non-invasive prenatal testing) analyses cell-free fetal DNA in maternal blood from around "
        "week 10 and screens for the most common chromosomal conditions — trisomy 21, 18 and 13. It is a "
        "blood test with no miscarriage risk, unlike amniocentesis or chorionic villus sampling.",
        "NIPT is a <strong>screening test, not a diagnostic answer</strong>. A positive finding must always "
        "be confirmed by CVS or amniocentesis before any conclusions are drawn. Nor does it replace "
        "preconception assessment — it measures something entirely different, at an entirely different time.",
        "<strong>We offer NIPT.</strong> Our view is that everyone who can should have it, and the "
        "advantage of doing it with us is that the result is read alongside your methylation profile and "
        "other findings rather than as an isolated verdict.",
    ]),
]

FAQ = [
    ("Should I take folic acid if I have an MTHFR variant?",
     "Yes — never stop folate supplementation, but choose the right form. Synthetic folic acid requires the "
     "MTHFR enzyme to be converted to 5-MTHF, the form cells actually use. At C677T homozygosity the enzyme "
     "runs at 30–40 % of normal capacity, and at high intakes unmetabolised folic acid accumulates. Active "
     "methylfolate bypasses that step. Periconceptional folate reduces neural tube defect risk by roughly "
     "70 % and the neural tube closes around day 28, often before pregnancy is known — so the answer is to "
     "change form, not to stop."),
    ("Is methylfolate better for everyone?",
     "No. Without an MTHFR variant there is no bottleneck to bypass, and high doses of active methylfolate "
     "can drive methylation faster than downstream capacity allows, increasing the requirement for "
     "methionine, B12, B6 and choline. The wrong form can cause problems whichever one you choose blindly. "
     "Which applies to you is determined by genotype."),
    ("Why should both partners be tested?",
     "Half the child's genome comes from the father. Spermatogenesis takes about 74 days and is affected by "
     "the same methylation pathways as egg maturation, including DNA fragmentation. Paternal folate status "
     "is as relevant as maternal status, and in practice it is almost never examined."),
    ("What is NIPT and do you offer it?",
     "NIPT analyses cell-free fetal DNA in maternal blood from around week 10 and screens for trisomy 21, "
     "18 and 13. It carries no miscarriage risk. It is a screening test, not a diagnosis — positive findings "
     "must be confirmed by CVS or amniocentesis. We offer NIPT, and read the result alongside your "
     "methylation profile rather than in isolation."),
    ("When should preconception assessment be done?",
     "Ideally three to six months before you start trying. Egg maturation takes roughly 90 days and "
     "spermatogenesis about 74, so corrections need that much time to reach the cells that matter. Testing "
     "earlier is better than testing later; testing at all is better than either."),
]


def build():
    anchors = [(a, t.split("—")[0].split(":")[0].strip()[:34]) for a, t, _ in SECTIONS]
    anchors.append(("faq", "FAQ"))
    body = "".join(
        f'<section id="{a}"><h2>{t}</h2>' + "".join(f"<p>{p}</p>" for p in ps) + "</section>"
        for a, t, ps in SECTIONS)

    title = "Baby Balans — preconception methylation, folate and NIPT | MediBalans Stockholm"
    desc = ("Healthy children begin before conception. We map methylation, MTHFR genotype and cellular "
            "nutrient status in both parents before pregnancy — and offer NIPT during it. The right form "
            "of folate, dosed to your genetics.")

    schema = [
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@graph": [
                {"@type": "MedicalWebPage", "@id": URL + "#page", "url": URL, "name": title,
                 "inLanguage": "en-GB", "datePublished": "2026-07-29", "dateModified": "2026-07-29",
                 "audience": {"@type": "Patient"}, "author": {"@id": AUTHOR_ID},
                 "provider": ORG, "publisher": ORG,
                 "about": {"@type": "MedicalTest",
                           "name": "Preconception methylation and nutrient assessment"}}]},
            ensure_ascii=False) + "</script>",
        faq_schema(URL, FAQ),
    ]

    content = f"""
{hero("Preconception · Baby Balans", "Healthy children begin ", "before conception.",
      "Antenatal care starts at a positive test. The most consequential window has closed by then — "
      "the neural tube closes around day 28, and the biochemistry that shapes it is set months earlier.",
      '<a class="btn-p" href="/en/#booking">Book a consultation</a>'
      '<a class="btn-s" href="/en/methylation-test/">MethylDetox — 38 genes</a>',
      "Clinical assessment by a licensed physician. Patients across Sweden and internationally.",
      [("90", "Days, egg maturation"), ("74", "Days, spermatogenesis"),
       ("28", "Day of neural tube closure"), ("38", "Genes in the panel")])}
{toc(anchors)}
<div class="container sec-body">
<section><p class="lead-p"><strong>In short:</strong> folate is not optional — but the right form depends on
your genotype, and so does the right dose. Carriers of MTHFR variants convert synthetic folic acid slowly and
incompletely; non-carriers rarely need active folate at high dose. One test settles which you are, and it holds
for life. We assess both parents before conception, and offer NIPT during pregnancy.</p></section>
{body}
<section id="faq"><h2>Frequently asked <em>questions</em></h2>{faq_html(FAQ)}</section>
<section id="related">
<p><a href="/en/methylation-test/">MethylDetox — 38 genes →</a> · <a href="/en/cellular-nutrient-analysis/">CMA — cellular nutrient status</a> · <a href="{SV_URL}">Svenska</a></p>
</section>
</div>
{band("Measure", "before you dose",
      "Which form of folate is right for you is a question with an answer. A preconception consultation "
      "establishes what your biology can actually supply — and what needs correcting while there is still "
      "time for it to matter.")}
"""
    return page(title, desc, URL, SV_URL, schema, content)


if __name__ == "__main__":
    p = os.path.join(ROOT, "en", "baby-balans", "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(build())
    print("   en/baby-balans/index.html — riktig sida, ersätter startsidekopian")
