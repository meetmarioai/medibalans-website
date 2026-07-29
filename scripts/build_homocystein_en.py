# -*- coding: utf-8 -*-
"""
MediBalans · Homocysteine — engelsk version av den kliniska noteringen
=======================================================================
Speglar /homocystein/ i sin helhet, inklusive de två fynd som bär texten
(riboflavin och MTRR), AHCY/SAM:SAH-avsnittet, NAD+-metyldränaget och
demonteringen av HOPE-2 och NORVIT på design.

Samma disciplin som den svenska: det som talar emot står med, och texten
säger uttryckligen att den avgörande studien aldrig har gjorts.

Kör:  python3 scripts/build_homocystein_en.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from build_content_en import page, hero, toc, band, faq_html, faq_schema, BASE, ROOT
from build_homocystein import SOURCES

URL = f"{BASE}/en/homocysteine/"
SV_URL = f"{BASE}/homocystein/"
ORG = {"@id": f"{BASE}/#organization"}
AUTHOR_ID = f"{BASE}/#mario-anthis"

SECTIONS = [
    ("reference", "The laboratory reference range is too permissive", [
        "Most laboratories report homocysteine below roughly 15 µmol/L as normal. That range was built to "
        "catch overt pathology — not to describe optimal function.",
        "The VITACOG trial at Oxford is the most instructive study here. Participants with mild cognitive "
        "impairment were randomised to B vitamins or placebo. Brain atrophy fell by around 30 % in the "
        "treatment group. In those with homocysteine above 13 µmol/L the rate of atrophy was 53 % lower, "
        "and in the medial temporal lobe — the region affected first in Alzheimer's disease — the "
        "difference was close to ninefold. The effect was concentrated in participants above the median "
        "of 11.3 µmol/L.",
        "In other words: values a laboratory reports as normal coincide with measurably accelerated brain "
        "atrophy. A result of 14 is not reassurance. It is a value at which a randomised trial has shown "
        "intervention makes a difference.",
        "We work clinically toward 6–9 µmol/L. That is a functional target, not a threshold drawn from an "
        "outcome trial — and the distinction is important enough to state plainly.",
    ]),
    ("system", "One value, six points", [
        "Homocysteine is a junction. It forms when methionine gives up its methyl group, and it leaves "
        "along three routes. Each route has its own enzyme and its own cofactor. A raised value means the "
        "flow is not balancing — but it does not identify where the restriction sits.",
        "<strong>MTHFR</strong> produces 5-MTHF, the active folate form. The enzyme requires FAD, "
        "that is riboflavin (B2).",
        "<strong>MTR</strong> (methionine synthase) remethylates homocysteine to methionine. It requires "
        "B12 as methyl carrier and 5-MTHF as methyl donor.",
        "<strong>MTRR</strong> restores MTR once its cobalamin has oxidised. Requires SAM and reducing capacity.",
        "<strong>BHMT</strong> is the folate-independent bypass: betaine (TMG) donates a methyl group "
        "directly. Choline is the precursor.",
        "<strong>CBS</strong> opens the drain — transsulfuration, carrying homocysteine onward toward "
        "cysteine and glutathione. Requires B6 in active form.",
        "<strong>AHCY</strong> sits upstream of all of it and is treated separately below. It is the enzyme "
        "that produces homocysteine in the first place.",
        "Six points, one measured value. That is why a homocysteine result alone is an alarm rather than a "
        "diagnosis, and why treating it with a single substance is guesswork made systematic.",
    ]),
    ("ahcy", "AHCY — the upstream step that determines what the number means", [
        "Homocysteine does not appear from nowhere. SAM donates its methyl group and becomes SAH — "
        "S-adenosylhomocysteine. Only then is SAH hydrolysed to homocysteine and adenosine, and the enzyme "
        "that does it is AHCY (S-adenosylhomocysteine hydrolase).",
        "<strong>The reaction is reversible, and equilibrium favours SAH formation.</strong> Net flux toward "
        "homocysteine occurs only while both products — homocysteine and adenosine — are continuously "
        "removed. If they accumulate the reaction runs backwards and SAH builds up. That makes this step "
        "dependent not only on its own enzyme but on the drains downstream working.",
        "<strong>SAH is a potent inhibitor of essentially all SAM-dependent methyltransferases.</strong> "
        "Accumulated SAH therefore brakes methylation broadly — DNA, histones, neurotransmitters, "
        "phospholipids — regardless of how much SAM is available.",
        "The consequence is uncomfortable but important: the real methylation index is the "
        "<strong>SAM:SAH ratio</strong>, not homocysteine. Homocysteine is a downstream shadow of that "
        "ratio. A patient can have a tidy homocysteine value alongside elevated SAH and suppressed "
        "methylation capacity — and a patient with raised homocysteine may have it precisely because the "
        "AHCY step is working well and the drain further down is narrow.",
        "It is the sharpest illustration of the thesis. A single sample of one metabolite in the middle of "
        "a cycle cannot by itself tell you which way the cycle is leaning.",
    ]),
    ("riboflavin", "Riboflavin — the best evidenced and least used", [
        "If one point in this text is worth taking away, it is this one.",
        "The C677T variant does not render the enzyme unusable. It makes it <em>thermolabile</em> — the "
        "enzyme has an increased tendency to dissociate from its FAD cofactor and loses activity as a "
        "result. Riboflavin stabilises that binding.",
        "This is not mechanistic reasoning alone. The Ulster group has run a series of targeted randomised "
        "trials: riboflavin lowers homocysteine specifically in TT genotype individuals (McNulty, 2006), "
        "lowers blood pressure in TT carriers with cardiovascular disease (Horigan, 2010), and lowers blood "
        "pressure in treated hypertensives with the TT genotype in a targeted randomised trial published "
        "in <em>Hypertension</em> (Wilson, 2013), with the effect sustained at four-year follow-up.",
        "Genotype-specific, randomised, replicated. Meanwhile virtually the entire MTHFR conversation "
        "concerns methylfolate, and riboflavin goes unmentioned. It is the most overlooked intervention in "
        "the field.",
    ]),
    ("mtrr", "MTRR — why normal B12 and folate are not enough", [
        "MTR carries its methyl group on the cobalt in cobalamin. Periodically cob(I)alamin oxidises to "
        "cob(II)alamin and the enzyme stalls. This is not a fault but normal wear within the reaction cycle.",
        "Restarting requires MTRR — methionine synthase reductase — which reductively remethylates the "
        "cofactor using SAM as methyl donor. Without functioning MTRR, MTR stands still regardless of how "
        "much B12 or folate is available.",
        "The decisive finding: the homocysteine-raising effect of the MTRR 66AA genotype is "
        "<strong>independent of serum folate, B12 and B6</strong>. A patient can therefore have textbook "
        "values on all three and still have a cycle that repeatedly stalls.",
        "This is the clinical reason an isolated MTHFR test is insufficient. MTHFR is one of several points "
        "at which the system can fail, and the only one the public has heard of.",
    ]),
    ("nad", "NAD⁺ supplements — the methyl drain rarely mentioned", [
        "There is an iatrogenic cause of rising homocysteine that almost never comes up, and it deserves "
        "its own section because it affects precisely the most health-conscious group.",
        "Nicotinamide — the end product when NAD⁺ precursors such as NMN, NR and niacinamide are "
        "metabolised — is not excreted as it is. It must be methylated first. The enzyme NNMT takes a "
        "methyl group from SAM to form 1-methylnicotinamide, leaving SAH behind. Every molecule of "
        "nicotinamide leaving the body costs a methyl group. Dose determines the bill.",
        "The effect is documented in humans. In a pharmacokinetic study, 100 mg of oral nicotinamide — a "
        "modest dose against the 300–900 mg of NMN common in longevity use — produced rising plasma "
        "homocysteine, depletion of the labile methyl pool and measurably impaired COMT activity within "
        "five hours.",
        "Animal work is clearer still. Nicotinamide supplementation in rats produced betaine depletion, a "
        "dose-dependent fall in global hepatic DNA methylation measured by LINE-1, and methylation changes "
        "at the promoters for NNMT, DNMT1, BHMT, methionine synthase and CBS — the genes of the methionine "
        "cycle itself. In NNMT-overexpressing mice the SAM:SAH ratio collapsed below 1.0, a level at which "
        "essentially all methyltransferase reactions are impaired, while BHMT1 expression fell.",
        "That last detail is the awkward one. The load disables the compensation that would have handled "
        "it: the BHMT branch, the body's folate-independent route for remethylating homocysteine, is "
        "suppressed by the same stress that makes it necessary. This is a self-reinforcing process rather "
        "than an equilibrium seeking its way back.",
        "That the deficit is correctable was shown in a growth study: impaired growth in animal pups at "
        "high nicotinamide doses was prevented by methionine supplementation, replenishing the drained "
        "SAM pool.",
    ]),
    ("nad-evidence", "What the clinical NAD⁺ trials actually show", [
        "The human evidence should be reported as it stands, including what argues against.",
        "NR-SAFE, a randomised double-blind placebo-controlled trial, gave nicotinamide riboside at "
        "3,000 mg daily for four weeks. Serum homocysteine rose significantly by 1.66 µmol/L "
        "(p = 5.4 × 10⁻⁴) and betaine fell relative to placebo. <strong>But</strong> — and this belongs in "
        "the record — whole blood homocysteine and whole blood SAM/SAH were unchanged, and the authors "
        "concluded the methyl donor pool remained largely intact at that dose and duration.",
        "An earlier safety trial in 140 overweight adults found no significant homocysteine elevation at "
        "100–1,000 mg NR daily over eight weeks. That trial also measured homocysteine as a specific safety "
        "endpoint, and its authors referred explicitly to 300 mg doses of nicotinamide and nicotinic acid "
        "being known to raise plasma homocysteine.",
        "A comprehensive human study published in 2025 subsequently confirmed across multiple independent "
        "cohorts that sustained intake of NAD⁺ precursors — both NMN and NR — depletes methyl donors and "
        "raises homocysteine.",
        "Taken together: the effect is dose- and duration-dependent, appears earlier in serum than in whole "
        "blood, and is modified by genotype and by how well the diet supplies methyl groups to begin with. "
        "Short trials at moderate doses in well-nourished subjects say little about what several years of "
        "daily intake does in an ageing population where MTHFR variants are common.",
        "The practical conclusion is not to avoid NAD⁺ precursors. It is that they constitute a methyl load "
        "that should be measured and balanced — check homocysteine before starting and during use, and "
        "provide methylation support rather than hoping the system absorbs it.",
    ]),
    ("methylfolate", "Why “just take methylfolate” often fails", [
        "Methylfolate addresses the MTHFR step. If that is where the bottleneck sits, the effect is often "
        "marked.",
        "If it sits elsewhere, little happens. If MTRR is impaired, what is missing is not methyl donors "
        "but reducing capacity. If B12 is insufficient or in the wrong form, the carrier is missing. If B6 "
        "status is low the drain to transsulfuration is narrow and homocysteine remains regardless of how "
        "much is remethylated. If riboflavin is low, bypassing an enzyme that could have been stabilised "
        "helps little.",
        "And in someone without an MTHFR variant there is no bottleneck to bypass. High doses of active "
        "folate can then drive methylation faster than downstream capacity allows and increase the draw on "
        "methyl groups, methionine, B12, B6 and choline.",
        "Betaine (TMG) deserves a specific note. It is an effective folate-independent route and clinically "
        "useful when the BHMT branch is the viable one. In trials, however, high doses have been shown to "
        "raise LDL and total cholesterol. That is an argument for dosing under follow-up rather than for "
        "avoidance — but it belongs in the picture.",
    ]),
    ("trials", "The negative trials — what they actually tested", [
        "The objection always comes, and it deserves a direct answer: the large intervention trials lowered "
        "homocysteine without reducing cardiovascular events. HOPE-2 gave 2.5 mg folic acid, 50 mg B6 and "
        "1 mg B12 for five years to high-risk patients — no effect on vascular events despite lowered "
        "homocysteine. NORVIT randomised patients within seven days of myocardial infarction, found no "
        "benefit, and reported a signal toward increased events in the combination arm.",
        "The conclusion usually drawn is that homocysteine is a marker rather than a cause. For the "
        "question those trials asked, that is a reasonable conclusion.",
        "But the question they asked was narrower than the one they are cited for. Four objections, each "
        "sufficient on its own to pull the result toward null:",
        "<strong>The population.</strong> Patients with established coronary disease, in NORVIT within a "
        "week of infarction. The plaque is already built. That tests reversal of manifest disease, not "
        "prevention across decades.",
        "<strong>The inclusion criteria.</strong> Raised homocysteine was not required to participate. "
        "Treating people who do not have the condition you wish to affect cannot demonstrate benefit — it "
        "dilutes the effect. VITACOG found its signal precisely by looking above the median, and the effect "
        "scaled with baseline.",
        "<strong>The intervention.</strong> High-dose synthetic folic acid, without riboflavin, without "
        "betaine, without genotype stratification. In carriers that generates unmetabolised folic acid. A "
        "trial that may have harmed a genotypic subgroup while treating unstratified patients is not a "
        "clean test of the hypothesis — and NORVIT's harm signal then becomes intelligible rather than "
        "mysterious.",
        "<strong>The endpoint.</strong> Hard cardiovascular events over a few years. VITACOG chose brain "
        "atrophy — a more sensitive and more proximal measure — and found a large effect. The choice of "
        "endpoint largely determined the answer.",
        "The trials therefore tested whether adding high-dose synthetic folic acid to patients with "
        "established vascular disease, regardless of baseline value and genotype, reduces recurrence. The "
        "answer is no. That is not the same question as whether lifelong methylation capacity matters for "
        "vascular and cerebral ageing.",
    ]),
    ("limits", "What we cannot claim", [
        "The decisive trial has not been done. There is no outcome study showing that a healthy "
        "thirty-five-year-old who lowers homocysteine from 10 to 7 using methylfolate, riboflavin and "
        "betaine lives longer or retains cognition better.",
        "Our target of 6–9 µmol/L is therefore a functional benchmark grounded in mechanism, in VITACOG's "
        "dose effect and in clinical experience — not a threshold validated against hard outcomes. Anyone "
        "claiming otherwise is overreading the evidence.",
        "Nor is lower automatically better. Very low values may reflect heavy draw toward transsulfuration "
        "or an altered B6 dependency, and should be interpreted in context rather than celebrated.",
        "What is hard to get around: homocysteine is cheap, widely available, modifiable — and the "
        "reference range in use today reports as normal values at which a randomised trial has demonstrated "
        "accelerated brain atrophy.",
    ]),
]

FAQ = [
    ("What should homocysteine be?",
     "Most laboratories report values below roughly 15 µmol/L as normal, but that range was built to catch "
     "overt pathology. VITACOG showed accelerated brain atrophy above 11 µmol/L and the largest treatment "
     "effect above 13. We work clinically toward 6–9 µmol/L. That is a functional benchmark grounded in "
     "mechanism and trial effect, not a threshold validated against hard outcomes."),
    ("Is methylfolate enough if homocysteine is high?",
     "Rarely. Homocysteine is formed and cleared through six points, each of which can be the bottleneck: "
     "AHCY which hydrolyses SAH to homocysteine, MTHFR which requires riboflavin, MTR which requires B12, "
     "MTRR which restores oxidised cobalamin using SAM, BHMT which runs on betaine and choline, and CBS "
     "which carries homocysteine toward glutathione and requires B6. Methylfolate addresses only the MTHFR "
     "step."),
    ("Why does riboflavin (B2) matter in MTHFR variants?",
     "The MTHFR enzyme requires FAD, formed from riboflavin. The C677T variant makes the enzyme "
     "thermolabile through an increased tendency to dissociate from FAD. Riboflavin stabilises that "
     "binding. Targeted randomised trials have shown riboflavin lowers homocysteine and blood pressure "
     "specifically in TT genotype individuals, with the effect sustained at four-year follow-up. It is the "
     "best evidenced genotype-specific intervention in the field and is still rarely used."),
    ("Can homocysteine be high despite normal B12 and folate?",
     "Yes. Methionine synthase stalls when its cobalamin oxidises, and MTRR is required to restore it. The "
     "homocysteine-raising effect of the MTRR 66AA genotype is independent of serum folate, B12 and B6 — so "
     "all three can be normal while the cycle still stalls. This is the clinical reason an isolated MTHFR "
     "test is insufficient."),
    ("Can methylation be impaired despite normal homocysteine?",
     "Yes. SAM donates its methyl group and becomes SAH, which is then hydrolysed to homocysteine and "
     "adenosine by AHCY. That reaction is reversible and equilibrium favours SAH formation, so net flux "
     "requires both products to be cleared continuously. SAH is also a potent inhibitor of essentially all "
     "SAM-dependent methyltransferases. The real methylation index is therefore the SAM:SAH ratio — "
     "homocysteine is a downstream shadow of it."),
    ("Can NMN or NR raise homocysteine?",
     "Yes, and the mechanism is well described. Nicotinamide must be methylated by NNMT to be excreted. "
     "Each molecule costs a methyl group from SAM and leaves SAH behind, so the load is dose-dependent. In "
     "humans, 100 mg of oral nicotinamide produced rising homocysteine and impaired COMT activity within "
     "five hours, and in a randomised trial 3,000 mg of nicotinamide riboside daily raised serum "
     "homocysteine by 1.66 µmol/L while betaine fell. A 2025 human study confirmed methyl donor depletion "
     "with sustained intake of both NMN and NR. The conclusion is not to avoid them, but to measure "
     "homocysteine before and during use and balance the methyl load."),
    ("Do the negative cardiac trials mean homocysteine does not matter?",
     "They show that adding high-dose synthetic folic acid to patients with established coronary disease, "
     "without requiring raised baseline values and without genotype stratification, does not reduce "
     "recurrence. That is a narrower question than the one usually cited. The population already had "
     "manifest disease, raised homocysteine was not required for entry, the intervention lacked riboflavin "
     "and betaine, and the endpoint was hard events over a few years. The trials do not refute the "
     "hypothesis — but the decisive trial has not been done either."),
    ("Is low homocysteine always good?",
     "No. Very low values may reflect heavy draw toward transsulfuration or an altered B6 dependency. The "
     "value is interpreted in context alongside B12, folate, B6, riboflavin status and genotype."),
]


def build():
    anchors = [(a, t.split("—")[0].strip()[:30]) for a, t, _ in SECTIONS] + [("faq", "FAQ")]
    body = "".join(
        f'<section id="{a}"><h2>{t}</h2>' + "".join(f"<p>{p}</p>" for p in ps) + "</section>"
        for a, t, ps in SECTIONS)
    srcs = "".join(f"<li>{s}</li>" for s in SOURCES)

    title = ("What should homocysteine be? One-carbon metabolism is a system, not a snapshot | MediBalans")
    desc = ("Laboratories report below 15 µmol/L as normal, but brain atrophy accelerates above 11. "
            "Homocysteine is formed via AHCY and cleared via MTHFR, MTR, MTRR, BHMT and CBS — with "
            "riboflavin, B12, SAM, betaine and B6 as cofactors. The real methylation index is the SAM:SAH ratio.")

    schema = [
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@graph": [
                {"@type": "MedicalWebPage", "@id": URL + "#page", "url": URL, "name": title,
                 "inLanguage": "en-GB", "datePublished": "2026-07-29", "dateModified": "2026-07-29",
                 "audience": {"@type": "Patient"}, "author": {"@id": AUTHOR_ID},
                 "provider": ORG, "publisher": ORG,
                 "about": {"@type": "MedicalTest", "name": "Homocysteine and methylation capacity"}}]},
            ensure_ascii=False) + "</script>",
        faq_schema(URL, FAQ),
    ]

    content = f"""
{hero("Clinical note · Methylation", "Homocysteine ", "A system, not a snapshot.",
      "A homocysteine value tells you one-carbon metabolism is not balancing. It tells you nothing about "
      "which of six points is restricting — and that is why treatment with a single substance so often fails.",
      '<a class="btn-p" href="/en/#booking">Book a consultation</a>'
      '<a class="btn-s" href="/en/methylation-test/">MethylDetox — 38 genes</a>',
      "Clinical note. Functional benchmarks are stated as such, not as validated thresholds.",
      [("6–9", "µmol/L, our target"), ("15", "Laboratory limit"),
       ("6", "Points in the system"), ("38", "Genes in the panel")])}
{toc(anchors)}
<div class="container sec-body">
<section><p class="lead-p"><strong>In short:</strong> the laboratory reference range is too permissive. Brain
atrophy accelerates at values reported as normal. We work toward 6–9 µmol/L. But the more important answer is
that the number alone does not tell you what to correct — homocysteine is formed and cleared through six points,
each with its own cofactor, and treatment is determined by which of them is the bottleneck.</p></section>
{body}
<section id="faq"><h2>Frequently asked <em>questions</em></h2>{faq_html(FAQ)}</section>
<section id="sources"><h2>Sources</h2><ol class="src">{srcs}</ol>
<p style="margin-top:1.5rem"><a href="/en/methylation-test/">MethylDetox — 38 genes →</a> · <a href="/en/baby-balans/">Baby Balans — preconception</a> · <a href="/en/cellular-nutrient-analysis/">CMA — cellular nutrient status</a> · <a href="{SV_URL}">Svenska</a></p></section>
</div>
{band("Measure the whole system,", "not one point",
      "A homocysteine value is the starting point, not the answer. Which point is restricting is determined "
      "by genotype and intracellular status — and that in turn determines which form and which dose is right for you.")}
"""
    html = page(title, desc, URL, SV_URL, schema, content)
    return html.replace("</style>", "\n.src{font-size:.87rem;color:var(--text-mid)}.src li{margin-bottom:.6rem}\n</style>", 1)


if __name__ == "__main__":
    p = os.path.join(ROOT, "en", "homocysteine", "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(build())
    print("   en/homocysteine/index.html")
