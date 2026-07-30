# -*- coding: utf-8 -*-
"""
MediBalans · engelska versioner av /symtom/ och /skrifter/
==========================================================
Bygger /en/symptoms/ och /en/writings/ ur det ENGELSKA sidskalet
(en/gi-effects-test/index.html) så att engelsk nav, footer och språk
följer med automatiskt.

hreflang paras åt båda håll mot de svenska originalen.

Kör från repo-roten:  python3 scripts/build_content_en.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.medibalans.com"
TEMPLATE = os.path.join(ROOT, "en", "gi-effects-test", "index.html")

ORG = {"@id": f"{BASE}/#organization"}
AUTHOR_ID = f"{BASE}/#mario-anthis"
AUTHOR_NODE = {
    "@type": "Physician", "@id": AUTHOR_ID, "name": "Mario Anthis",
    "givenName": "Mario", "familyName": "Anthis",
    "jobTitle": "Founder & Medical Director",
    "worksFor": ORG, "medicalSpecialty": "PrimaryCare",
    "url": f"{BASE}/en/writings/",
}

EN_PANEL = {
    "gi-effects-test": ("GI Effects®", "SEK 8,500"),
    "nutreval-test": ("NutrEval® FMV", "SEK 12,200"),
    "metabolomics": ("Metabolomix+", "SEK 8,100"),
    "sibo-test": ("SIBO Breath Test", "SEK 3,700"),
    "womens-health": ("Women's Health+", "SEK 6,200"),
    "organix": ("Organix®", "SEK 5,600"),
    "fatty-acids": ("Fatty Acid Analysis", "SEK 3,900"),
    "adrenal-stress": ("Adrenocortex Stress Profile", "SEK 2,100"),
    "essential-estrogens": ("Essential Estrogens", None),
    "menopause-plus": ("Menopause Plus", None),
    "alcat-test": ("ALCAT immune reactivity", None),
}


def extract_shell():
    h = open(TEMPLATE, encoding="utf-8").read()
    body_i = h.index("<body")
    styles = "".join(m.group(0) for m in re.finditer(r"<style[^>]*>.*?</style>", h[:body_i], re.S))
    fonts = "".join(re.findall(r'<link[^>]*fonts\.(?:googleapis|gstatic)[^>]*>', h[:body_i]))
    m = re.search(r"<script>!function\(f,b,e,v,n,t,s\).*?</script>", h, re.S)
    pixel = m.group(0) if m else ""
    body_open = re.search(r"<body[^>]*>", h).group(0)
    # mobilmenyn ligger utanför </header> — måste tas med, annars blir
    # hamburgarknappen död på nya sidor
    h_start = h.index("<header")
    h_end = h.index("</header>") + len("</header>")
    mn = h.find('id="mobileNav"', h_end)
    if mn != -1:
        m = re.search(r"</div>\s*(?=<(?!a\b)[a-zA-Z])", h[mn:])
        header = h[h_start: mn + m.end()] if m else h[h_start:h_end]
    else:
        header = h[h_start:h_end]
    assert 'id="mobileNav"' in header, "mobilnav saknas i extraherat skal"
    footer = h[h.index("<footer"): h.index("</footer>") + len("</footer>")]
    tail = h[h.index("</footer>") + len("</footer>"):]
    return dict(styles=styles, fonts=fonts, pixel=pixel, body_open=body_open,
                header=header, footer=footer, tail=tail)


S = extract_shell()

_src = open(os.path.join(ROOT, "scripts", "build_new_sections.py"), encoding="utf-8").read()
_start = _src.index("/* ---- sektionsspecifikt")
_end = _src.index("</style>", _start)          # sök EFTER startpunkten
EXTRA_CSS = _src[_start:_end].replace("{{", "{").replace("}}", "}")
assert ".sec-hero{" in EXTRA_CSS and ".reco-badge{" in EXTRA_CSS, "CSS-extraktion misslyckades"


def page(title, desc, canonical, sv_url, schema_blocks, content):
    schema = "\n".join(schema_blocks)
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js" style="overflow-x:hidden;">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{canonical}">
<link rel="alternate" hreflang="sv" href="{sv_url}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_GB">
<meta property="og:locale:alternate" content="sv_SE">
<meta property="og:image" content="{BASE}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
{schema}
{S['pixel']}
{S['fonts']}
{S['styles']}
<style>
{EXTRA_CSS}
</style>
</head>
{S['body_open']}
{S['header']}
{content}
{S['footer']}
{S['tail']}"""


def reco():
    return """<a class="reco-badge" href="https://www.reco.se/medibalans-christina-biri-ab" rel="noopener">
<span class="score">4.87</span>
<span>
  <span class="stars">★★★★★</span>
  <span class="lbl">Highest rated in Sweden</span>
  <span class="sub">Verified patient reviews · Reco.se</span>
</span>
<span class="ver">Reco.se<b>Verified</b></span>
</a>"""


def hero(eyebrow, h1, h1em, lead, buttons, fine="", stats=None):
    s = ""
    if stats:
        s = '<div class="sec-stats">' + "".join(
            f'<div><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in stats) + "</div>"
    return f"""<section class="sec-hero"><div class="container">
<p class="eyebrow">{eyebrow}</p>
<h1>{h1}<em>{h1em}</em></h1>
<p class="lead">{lead}</p>
<div class="btn-row">{buttons}</div>
{f'<p class="fine">{fine}</p>' if fine else ''}
{reco()}
{s}
</div></section>"""


def toc(items):
    return ('<div class="sec-toc"><div class="container"><div class="inner">'
            '<span class="lbl">On this page</span>'
            + "".join(f'<a href="#{a}">{t}</a>' for a, t in items) + "</div></div></div>")


def band(h2, h2em, p):
    return f"""<section class="sec-band"><div class="container">
<h2>{h2}<em> {h2em}</em></h2><p>{p}</p>
<div class="btn-row">
<a class="btn-p" href="/en/#booking">Book a consultation</a>
<a class="btn-s" href="tel:+46723195070">+46 72 319 50 70</a>
</div></div></section>"""


def faq_html(items):
    return "".join(f'<div class="faq-i"><p class="q">{q}</p><p class="a">{a}</p></div>' for q, a in items)


def faq_schema(url, items):
    return ('<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage", "@id": url + "#faq",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]
    }, ensure_ascii=False) + "</script>")


# ═══════════════════════════════════════════════════ GUIDES (EN)
GUIDES = [
    dict(
        slug="bloating", sv="uppblast-mage",
        kicker="Symptom guide · Digestive health",
        title="Constantly bloated — causes and what can actually be measured | MediBalans",
        desc="Daily bloating rarely has a single cause. The most common explanations, when to seek medical care, and which causes can be measured objectively.",
        h1="Bloated all the time — ", h1em="what it can mean",
        lead="Being bloated after a large meal is normal. Being bloated every day, regardless of what you eat, is not. The difference is not how much it swells but how predictable it is.",
        svar="Short answer: chronic bloating usually comes down to one of four things — incomplete breakdown of food, bacterial fermentation in the wrong part of the gut, immune reactivity to certain foods, or altered gut motility. They produce similar symptoms but require different action, which is why general dietary advice so often fails.",
        orsaker=[
            ("Incomplete breakdown of food", "If the pancreas produces too few enzymes, or stomach acid is insufficient, incompletely digested food travels further down the gut than it should. There it ferments. Typical pattern: bloating regardless of what you eat, strong-smelling gas, loose or greasy stools."),
            ("Bacterial fermentation in the wrong place", "Bacteria belong in the colon. If they colonise the small intestine they ferment food before it can be absorbed. Typical pattern: swelling within 30–90 minutes of eating, often worse with fibre-rich or sugary food — the opposite of what general dietary advice recommends."),
            ("Immune reactivity to foods", "Delayed immune reactions to foods can drive low-grade inflammation in the gut lining. Because the reaction appears hours to days after the meal, it is difficult to link to the right food on your own."),
            ("Altered gut motility", "If the gut's wave-like movements are too slow, contents remain and ferment. Common in constipation-predominant presentations and aggravated by stress, thyroid dysfunction and certain medicines."),
            ("Hormonal and cycle-related causes", "Many women experience swelling that follows the menstrual cycle. If bloating is cyclical rather than daily, the explanation often lies in hormonal fluid regulation rather than the gut."),
        ],
        roda=["Blood in the stool or black stools", "Unintentional weight loss", "Anaemia",
              "Fever, night sweats or symptoms that wake you",
              "Swelling that is persistent and does not vary through the day",
              "New symptoms after the age of 50",
              "Family history of bowel cancer, coeliac disease or inflammatory bowel disease"],
        matbart=[("Incomplete breakdown", "Pancreatic elastase-1, faecal fat, muscle fibres", "gi-effects-test"),
                 ("Bacterial fermentation in the small intestine", "Hydrogen and methane in breath over time", "sibo-test"),
                 ("Gut flora composition", "Microbiome by PCR, short-chain fatty acids", "gi-effects-test"),
                 ("Inflammation in the gut lining", "Calprotectin, EPX, secretory IgA", "gi-effects-test"),
                 ("Cyclical, hormonally driven swelling", "Sex hormones and metabolites over time", "womens-health")],
        sjalv=[("Start with primary care if you have not already", "Faecal calprotectin and blood counts are free, fast and rule out serious disease. Any further investigation is more meaningful once that is done."),
               ("Keep a diary for two weeks — but the right way", "Record the time of the meal and the time of the swelling, not just what you ate. The delay is often more informative than the content."),
               ("Be careful about eliminating foods on your own", "Prolonged self-imposed elimination diets narrow the diet, reduce gut flora diversity and make later investigation harder to interpret."),
               ("Note whether it follows your cycle", "If swelling is predictably worse on certain days of the month, that is a different investigation from daily bloating.")],
        faq=[("Why am I bloated all the time even though I eat healthily?",
              "Healthy food is not the same as easily digestible food. Fibre-rich vegetables, legumes and wholegrains ferment strongly if they reach bacteria in the wrong part of the gut or if breakdown is incomplete. The problem is not the food itself but where and how it is broken down."),
             ("My tests were normal — why am I still bloated?",
              "Standard primary-care tests are designed to detect or exclude inflammatory bowel disease and bleeding. They do not measure digestion, pancreatic enzyme production, gut flora composition or its metabolic output. Normal tests exclude disease — not dysfunction."),
             ("Can the cause of bloating be measured?",
              "Several of the causes can be measured objectively. Enzyme production is assessed via pancreatic elastase-1 in stool, bacterial fermentation in the small intestine via hydrogen and methane breath testing, and gut flora composition via a comprehensive stool profile. Which measurement is warranted depends on the symptom pattern."),
             ("What does an investigation for bloating cost?",
              "GI Effects Comprehensive costs SEK 8,500 and the SIBO breath test SEK 3,700 through MediBalans, including the kit, analysis at Genova Diagnostics and clinical interpretation by a licensed physician. Which analysis is warranted is decided at the initial consultation.")],
        rel=[("gi-effects-test", "Comprehensive stool profile: digestion, microbiome, inflammation and metabolic output."),
             ("sibo-test", "Hydrogen and methane breath test for bacterial overgrowth in the small intestine.")],
    ),
    dict(
        slug="tired-all-the-time", sv="trott-hela-tiden",
        kicker="Symptom guide · Energy &amp; fatigue",
        title="Tired all the time despite sleeping — what fatigue can be caused by | MediBalans",
        desc="Fatigue despite normal blood tests is common and usually has a measurable explanation. Common causes, when to seek care, and what can be measured beyond routine tests.",
        h1="Tired all the time despite sleeping — ", h1em="and the tests are normal",
        lead="The sentence we hear most often is that everything looked fine on the tests. That is usually true — and at the same time insufficient. Routine tests are built to detect disease, not to explain why energy production is failing.",
        svar="Short answer: fatigue with normal routine tests rarely has a single cause. The most common explanations are insufficient cofactors for cellular energy production, a disrupted circadian rhythm in the stress system, low-grade inflammation, borderline thyroid dysfunction, or sleep that is long enough but not restorative.",
        orsaker=[
            ("Cellular energy production lacks cofactors", "Mitochondria need B vitamins, magnesium, iron, CoQ10 and carnitine to convert food into energy. A normal blood level does not mean the process inside the cell is working — serum reflects transport, not function."),
            ("Disrupted circadian rhythm in the stress system", "Cortisol should be high in the morning and low in the evening. After prolonged strain the curve flattens or shifts. Typical pattern: difficulty getting going, a dip mid-afternoon, paradoxically alert late at night."),
            ("Low-grade inflammation", "Chronic immune activation consumes energy and affects the brain directly. It need not show as elevated CRP."),
            ("Borderline thyroid function", "A TSH within the reference range does not exclude a thyroid contribution, particularly if antibodies are present or conversion from T4 to T3 is insufficient."),
            ("Sleep that is long but not restorative", "Eight hours in bed is not eight hours of recovery. Sleep apnoea and nocturnal stress activation produce normal sleep duration with absent recovery."),
            ("Borderline iron and B12 status", "Ferritin in the lower part of the reference range often produces symptoms long before haemoglobin is affected, particularly in menstruating women."),
        ],
        roda=["Unintentional weight loss", "Fever or night sweats",
              "Breathlessness or chest pain on exertion",
              "New neurological symptoms — numbness, visual changes, weakness",
              "Fatigue that has worsened rapidly over weeks",
              "Low mood, hopelessness or thoughts of not wanting to live",
              "Unexplained anaemia"],
        matbart=[("Cellular energy production", "Organic acids, amino acids, mitochondrial markers", "nutreval-test"),
                 ("Metabolic bottleneck without a blood draw", "Organic acids via a urine sample at home", "metabolomics"),
                 ("The stress system's daily curve", "Cortisol at several time points plus DHEA", "adrenal-stress"),
                 ("Inflammatory baseline", "Omega-3 index and omega-6/omega-3 ratio", "fatty-acids"),
                 ("Hormonal cause in women", "Sex hormones, cortisol and melatonin over time", "womens-health")],
        sjalv=[("Make sure the basic work-up has actually been done", "Full blood count, ferritin, B12, folate, TSH, glucose and CRP. It is free, fast and necessary before anything more advanced is meaningful. Ask to see the actual numbers, not just the message that everything was normal."),
               ("Track fatigue across the day for two weeks", "Rate your energy three times daily. The pattern is diagnostic: uniformly low energy points somewhere different from energy that is low in the morning and rises at night."),
               ("Rule out sleep apnoea if you snore", "It is common, underdiagnosed and treatable. No nutritional analysis compensates for fragmented sleep."),
               ("Be sceptical of adding supplements at random", "Without measurement it is guesswork, and some supplements at high doses can shift other systems.")],
        faq=[("Why am I tired when all my tests are normal?",
              "Routine tests are constructed to detect disease, not to describe function. They measure the concentration of a handful of substances in blood, not whether the biochemical processes requiring them are working inside the cell. A normal serum level can therefore coexist with a bottleneck in cellular energy production."),
             ("Which tests can show why I am tired?",
              "Beyond the basic work-up, cellular energy production can be assessed via organic acids and amino acids, the stress system's daily curve via cortisol at several time points, and fatty acid status. NutrEval FMV costs SEK 12,200, Metabolomix+ SEK 8,100 and the Adrenocortex Stress Profile SEK 2,100 through MediBalans."),
             ("What is the difference between ordinary tiredness and burnout?",
              "Ordinary tiredness improves with rest and sleep. In burnout, rest does not produce the same recovery, and fatigue is often accompanied by cognitive symptoms, disturbed sleep and reduced stress tolerance. If rest does not help, that is a reason to investigate further."),
             ("Can fatigue originate in the gut?",
              "It can. Impaired nutrient absorption, low-grade gut inflammation and immune reactivity to foods can all contribute. If you have both digestive symptoms and fatigue, investigating the gut first is often reasonable.")],
        rel=[("nutreval-test", "125+ biomarkers: organic acids, amino acids, fatty acids, vitamins and minerals."),
             ("adrenal-stress", "Cortisol at timed points across the day plus DHEA.")],
    ),
    dict(
        slug="food-reactions", sv="reagerar-pa-maten",
        kicker="Symptom guide · Food &amp; immune reactivity",
        title="I react to almost everything I eat — what it can mean | MediBalans",
        desc="When more and more foods cause symptoms, the explanation is rarely that you have become allergic to everything. What is actually happening, the risks of eliminating on your own, and what can be measured.",
        h1="I react to almost everything I eat — ", h1em="what does it mean?",
        lead="The list of foods you cannot tolerate grows longer every month. This is often read as becoming allergic to more and more things. More often something else is going on — and the growing list is a symptom of it, not the explanation.",
        svar="Short answer: when tolerance to food gradually narrows, true allergy is rarely the mechanism. The most common explanations are reduced digestive capacity, a gut lining with ongoing low-grade inflammation, delayed immune reactions to common foods, and a gut flora that has become less robust — often as a consequence of repeated elimination diets.",
        orsaker=[
            ("True allergy is uncommon in this picture", "IgE-mediated allergy produces rapid, predictable and often dramatic reactions to a small number of specific substances. That rarely matches a picture of gradually worsening tolerance to more and more foods."),
            ("Delayed immune reactions", "Cellular immune reactions to foods appear hours to days after a meal. The delay makes them nearly impossible to identify with a food diary."),
            ("Reduced digestive capacity", "If enzyme or acid production is insufficient, more foods become difficult to handle — not because they are harmful, but because they are not broken down sufficiently."),
            ("The gut lining is affected", "With ongoing low-grade inflammation the lining becomes more easily irritated. Ordinary foods then produce symptoms, much as salt stings more in a wound than on intact skin."),
            ("The diet has narrowed", "Each elimination reduces gut flora diversity, and a less diverse flora handles variation less well. This creates a self-reinforcing spiral."),
        ],
        roda=["Swelling of the lips, tongue or throat — seek emergency care",
              "Breathing difficulty or hives with a meal — seek emergency care",
              "Unintentional weight loss or nutritional deficiency", "Blood in the stool",
              "Vomiting or difficulty swallowing",
              "Severely restricted diet over a long period",
              "Anxiety around meals or growing need to control food"],
        matbart=[("Delayed immune reactivity to foods", "Cellular reactivity to up to 250 or 483 foods, additives and chemicals", "alcat-test"),
                 ("Inflammation in the gut lining", "Calprotectin, EPX, secretory IgA", "gi-effects-test"),
                 ("Digestive capacity", "Pancreatic elastase-1, faecal fat", "gi-effects-test"),
                 ("Gut flora diversity", "Microbiome by PCR and short-chain fatty acids", "gi-effects-test"),
                 ("Bacterial fermentation in the small intestine", "Hydrogen and methane in breath", "sibo-test")],
        sjalv=[("Stop expanding the elimination until you know why", "Each new elimination without evidence narrows the diet and makes later investigation harder to interpret. A growing list is a reason to investigate, not to keep removing."),
               ("Rule out coeliac disease before removing gluten", "Coeliac testing becomes unreliable once you have stopped eating gluten. The order matters — test first, eliminate after."),
               ("Record the delay, not only what you ate", "Reactions within minutes, within hours and after a day point to entirely different mechanisms."),
               ("Pay attention to how you feel around food", "If meals have become anxious or the need to control food is growing, that deserves help in itself, whatever the investigation shows.")],
        faq=[("Can you become intolerant to more and more foods?",
              "What you experience is real, but the explanation is rarely that the immune system has become allergic to more and more substances. More often digestive capacity is reduced or the gut lining is easily irritated, so more foods produce symptoms. The threshold has fallen, rather than the number of allergies having risen."),
             ("What is the difference between allergy and intolerance?",
              "Allergy is an IgE-mediated immune reaction that appears rapidly and can be life-threatening. Intolerance usually concerns failing breakdown, for example lactose intolerance. In addition there are delayed cellular immune reactions to foods, appearing hours to days after a meal, which neither standard allergy testing nor a food diary captures well."),
             ("Why does a food diary not help?",
              "Because a delayed reaction can appear up to a day after the meal. What you note as the cause is then usually the wrong meal. This is also why many end up eliminating more and more foods without improving."),
             ("Should I cut out gluten and dairy to be safe?",
              "Not without first testing for coeliac disease, since that test becomes unreliable once you stop eating gluten. Prolonged eliminations without evidence narrow the diet and reduce gut flora diversity, which can worsen the picture over time.")],
        rel=[("gi-effects-test", "Comprehensive stool profile: inflammation, digestion, microbiome and barrier."),
             ("sibo-test", "Hydrogen and methane breath test for bacterial overgrowth.")],
        essay_link=True,
    ),
    dict(
        slug="brain-fog", sv="hjarndimma",
        kicker="Symptom guide · Cognition",
        title="Brain fog — why thinking feels slow and what can be measured | MediBalans",
        desc="Brain fog is a real symptom with several possible explanations. Common causes, when to seek care, and which factors can be measured objectively.",
        h1="Brain fog — when thinking ", h1em="moves through syrup",
        lead="You cannot find the words. You read the same paragraph three times. You walk into a room and forget why. Brain fog is not a diagnostic term, but it describes something real — and it almost always has a physiological component that can be investigated.",
        svar="Short answer: the brain is metabolically demanding and sensitive to disturbances in energy supply, inflammation and circadian rhythm. The most common explanations for brain fog are insufficient cellular energy production, low-grade inflammation, disrupted circadian rhythm, hormonal change and nutritional cofactor deficiency.",
        orsaker=[
            ("The brain is not getting enough energy", "The brain uses around a fifth of the body's energy. When mitochondrial energy production has a bottleneck it often shows cognitively first, before it registers as physical fatigue."),
            ("Low-grade inflammation", "Inflammatory signalling affects the brain directly, producing reduced concentration and slower thinking. This can occur without elevated CRP."),
            ("Disrupted circadian rhythm", "Cognitive sharpness follows the circadian rhythm closely. With a flattened cortisol curve the usual morning sharpness fails to appear."),
            ("Hormonal change", "Oestrogen affects the brain's energy metabolism and neurotransmitters. Cognitive symptoms during perimenopause are common, real and under-reported."),
            ("Missing cofactors for neurotransmitters", "Synthesis of dopamine, serotonin and noradrenaline requires B vitamins, iron and magnesium. Insufficient availability produces cognitive symptoms before it appears in standard tests."),
            ("Sleep, blood sugar and medication", "Fragmented sleep, large blood sugar swings and certain medicines are common and frequently overlooked contributors."),
        ],
        roda=["Sudden confusion or difficulty speaking — seek emergency care",
              "One-sided weakness or numbness — seek emergency care",
              "Memory loss that others around you notice",
              "Difficulty managing everyday tasks you previously handled",
              "New cognitive symptoms after a head injury",
              "Visual changes or persistent headache",
              "Symptoms worsening rapidly over weeks"],
        matbart=[("Mitochondrial energy production", "Organic acids and Krebs cycle intermediates", "organix"),
                 ("Neurotransmitter metabolism", "Breakdown products of dopamine and serotonin", "organix"),
                 ("Nutritional cofactors", "B vitamins, magnesium, amino acids, antioxidant status", "nutreval-test"),
                 ("Fatty acid status in the brain", "Omega-3 index, particularly DHA", "fatty-acids"),
                 ("Circadian rhythm and stress system", "Cortisol curve across the day", "adrenal-stress"),
                 ("Hormonal cause in perimenopause", "Oestrogens, progesterone and melatonin across several days", "menopause-plus")],
        sjalv=[("Rule out the simple things first", "Full blood count, ferritin, B12, folate, TSH and glucose. Iron deficiency and thyroid dysfunction are common, treatable causes of cognitive symptoms."),
               ("Map when in the day the fog is worst", "Worst in the morning points to circadian rhythm. Worst after meals points to blood sugar. Even across the day points to something more fundamental."),
               ("Address sleep before anything else", "No analysis compensates for fragmented sleep, and sleep apnoea is both common and treatable."),
               ("Note whether it follows your cycle", "Cognitive symptoms that arrived alongside changes in periods, sleep or hot flushes often have a hormonal component.")],
        faq=[("What is brain fog?",
              "Brain fog is not a medical diagnosis but a description of reduced cognitive sharpness — poorer concentration, word-finding difficulty, slower thinking and reduced working memory. The symptom is real and almost always has a physiological component, usually linked to energy supply, inflammation, circadian rhythm or hormonal change."),
             ("Is brain fog a sign of dementia?",
              "In the great majority of cases no, particularly in younger people and when symptoms vary through the day or track sleep and stress. Memory loss that others around you notice, or difficulty managing everyday tasks you previously handled, is however a reason to seek medical assessment."),
             ("What can be measured in brain fog?",
              "Beyond the basic work-up, mitochondrial energy production and neurotransmitter metabolism can be assessed via organic acids in urine. Organix costs SEK 5,600, NutrEval FMV SEK 12,200, fatty acid analysis SEK 3,900 and the Adrenocortex Stress Profile SEK 2,100 through MediBalans."),
             ("Can brain fog originate in the gut?",
              "Indirectly, yes. Impaired nutrient absorption, low-grade gut inflammation and immune activation affect the brain's energy supply and inflammatory environment. If you have both digestive and cognitive symptoms, investigating the gut as part of the picture is often reasonable.")],
        rel=[("organix", "Organic acids in urine: mitochondrial function, neurotransmitters, detoxification."),
             ("nutreval-test", "Broad metabolic and nutritional mapping, 125+ biomarkers.")],
    ),
    dict(
        slug="hormonal-fatigue-after-40", sv="trott-efter-40-hormoner",
        kicker="Symptom guide · Hormones after 40",
        title="Tired, sleeping badly and not yourself after 40 — hormonal causes | MediBalans",
        desc="Perimenopause often begins years before periods change, producing fatigue, disturbed sleep and mood swings. Why blood tests are often normal, and what can be measured instead.",
        h1="Tired, sleeping badly and not yourself after 40 — ", h1em="it may be hormonal",
        lead="It rarely begins with hot flushes. It begins with sleep getting worse, patience running out faster, and not quite recognising yourself. Perimenopause can begin up to a decade before periods change noticeably.",
        svar="Short answer: in perimenopause hormones fluctuate sharply from day to day before they decline. A blood test taken on a single day therefore often falls within the reference range despite marked symptoms — not because hormones are stable, but because the test captured one point on a curve that is swinging.",
        orsaker=[
            ("Progesterone falls first", "Progesterone often declines several years before oestrogen. Because progesterone has calming, sleep-promoting effects, the decline is usually first noticed as worse sleep and a shorter fuse — long before classic menopausal symptoms."),
            ("Oestrogen fluctuates before it falls", "In perimenopause oestrogen swings sharply up and down. It is the swings themselves, rather than low levels, that produce many of the symptoms — and they make single blood tests hard to interpret."),
            ("Sleep becomes less restorative", "Hormonal change affects sleep architecture. You may sleep the same number of hours but obtain less deep sleep."),
            ("The stress system becomes more sensitive", "Hormonal change and the HPA axis influence each other. Many describe the same workload that previously worked as now unmanageable."),
            ("Thyroid and iron change at the same time", "Thyroid disease often presents in the same age range, and heavy bleeding can deplete iron stores. Both produce similar symptoms and must be excluded."),
            ("Metabolism and body composition shift", "Altered insulin sensitivity and muscle mass mean the same diet and training produce different results than before."),
        ],
        roda=["Bleeding that is very heavy or prolonged",
              "Bleeding between periods or after intercourse",
              "Bleeding after periods have stopped for more than a year — seek care",
              "Unintentional weight loss", "New severe low mood or anxiety",
              "Breast changes or a lump", "Symptoms worsening rapidly"],
        matbart=[("Hormonal fluctuation across several days", "Oestrogens, progesterone, P/E2 ratio, testosterone, DHEA, cortisol, melatonin", "menopause-plus"),
                 ("Hormones in their daily context", "Sex hormones with cortisol curve and oestrogen metabolism", "womens-health"),
                 ("Oestrogen breakdown pathways", "2-OH, 4-OH and 16α-OH metabolites and methylation", "essential-estrogens"),
                 ("The stress system's daily curve", "Cortisol at several time points plus DHEA", "adrenal-stress"),
                 ("Nutritional status and energy production", "Organic acids, amino acids, vitamins and minerals", "nutreval-test")],
        sjalv=[("Ask for the basic tests and see the numbers", "TSH, ferritin, full blood count, B12 and glucose. Thyroid disease and iron deficiency are common at this age and produce symptoms easily attributed to hormones."),
               ("Track symptoms against your cycle for three months", "Record sleep, energy and mood alongside where you are in the cycle. Patterns over time are more informative than single values."),
               ("Take symptoms seriously even if tests are normal", "Normal tests in perimenopause do not exclude a hormonal cause. They reflect one day on a curve that is swinging."),
               ("Protect sleep and muscle mass", "Strength training and a regular sleep rhythm are two of the most effective measures at this stage, whatever the investigation later shows.")],
        faq=[("Why are my hormone tests normal despite clear symptoms?",
              "In perimenopause hormone levels fluctuate sharply from day to day. A blood test taken on a single day can therefore fall within the reference range despite marked symptoms. Samples collected at several points across several days show the pattern and the fluctuation rather than a single point."),
             ("When does perimenopause begin?",
              "It can begin up to ten years before periods stop, often in the forties and sometimes earlier. The first signs are rarely hot flushes but instead worse sleep, reduced stress tolerance, mood swings and fatigue."),
             ("Can fatigue after 40 have causes other than hormones?",
              "Yes, and those should be excluded first. Thyroid disease, iron deficiency, sleep apnoea and depression are common in the same age range and produce similar symptoms. A hormonal investigation is most meaningful once the basic work-up is done."),
             ("What can be measured in perimenopausal symptoms?",
              "Hormones can be measured at several points across several days to capture the fluctuation, together with the cortisol curve and melatonin. Women's Health+ costs SEK 6,200 and the Adrenocortex Stress Profile SEK 2,100 through MediBalans. Menopause Plus and Essential Estrogens are priced at consultation.")],
        rel=[("womens-health", "Sex hormones, cortisol curve and oestrogen metabolism in one context."),
             ("menopause-plus", "Saliva samples across several days capturing hormonal fluctuation.")],
    ),
]


def pcard(slug, desc):
    name, price = EN_PANEL[slug]
    p = f'<div class="p">{price}</div>' if price else '<div class="p">Priced at consultation</div>'
    return (f'<a class="mb-card" href="/en/{slug}/"><span class="k">Analysis</span>'
            f'<div class="t">{name}</div><p class="d">{desc}</p>{p}</a>')


def build_guide(g):
    url = f"{BASE}/en/symptoms/{g['slug']}/"
    sv_url = f"{BASE}/symtom/{g['sv']}/"
    anchors = [("causes", "Common causes"), ("seek-care", "When to seek care"),
               ("measurable", "What can be measured"), ("yourself", "What you can do first"),
               ("faq", "FAQ")]
    orsaker = "".join(f"<h3>{t}</h3><p>{d}</p>" for t, d in g["orsaker"])
    roda = "".join(f"<li>{x}</li>" for x in g["roda"])
    sjalv = "".join(f"<h3>{t}</h3><p>{d}</p>" for t, d in g["sjalv"])
    rows = ""
    for cause, meas, slug in g["matbart"]:
        name, _ = EN_PANEL[slug]
        rows += (f'<tr><td><strong>{cause}</strong></td><td>{meas}</td>'
                 f'<td><a href="/en/{slug}/">{name}</a></td></tr>')
    cards = "".join(pcard(s, d) for s, d in g["rel"])
    if g.get("essay_link"):
        cards += ('<a class="mb-card" href="/en/clinical-notes/#cn-011">'
                  '<span class="k">Writings</span><div class="t">Evolutionary mismatch — what the test actually measures</div>'
                  '<p class="d">Essay by Mario Anthis on reactivity as recognition rather than disease.</p></a>')

    schema = [
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "MedicalWebPage", "@id": url + "#page",
            "url": url, "name": g["title"], "inLanguage": "en-GB",
            "datePublished": "2026-07-28", "dateModified": "2026-07-28",
            "audience": {"@type": "Patient"}, "provider": ORG, "publisher": ORG,
        }, ensure_ascii=False) + "</script>",
        faq_schema(url, g["faq"]),
    ]

    content = f"""
{hero(g['kicker'], g['h1'], g['h1em'], g['lead'],
      '<a class="btn-p" href="/en/#booking">Book a consultation</a>'
      '<a class="btn-s" href="#measurable">What can be measured</a>',
      'Clinical assessment by a licensed physician. Patients across Sweden and internationally.',
      [(str(len(g['orsaker'])), 'Possible causes'), (str(len(g['matbart'])), 'Measurable factors'),
       ('Home kit', 'Sampling'), ('2–3 wks', 'Turnaround')])}
{toc(anchors)}
<div class="container sec-body">
<section><p class="lead-p">{g['svar']}</p></section>
<section id="causes"><h2>Common <em>causes</em></h2>{orsaker}</section>
<section id="seek-care"><h2>When to <em>seek care</em></h2>
<p>The following should be assessed within conventional healthcare before any extended investigation. They are best excluded early and cost nothing to check.</p>
<div class="box-warn"><ul>{roda}</ul></div>
<p>No functional analysis replaces conventional medical assessment for these symptoms.</p></section>
<section id="measurable"><h2>What can actually be <em>measured</em></h2>
<p>Several of the causes above can be investigated objectively. The table shows which measurement answers which question — which is warranted in your case depends on the symptom pattern, not on how comprehensive the panel is.</p>
<table><thead><tr><th>Possible cause</th><th>What is measured</th><th>Analysis</th></tr></thead><tbody>{rows}</tbody></table>
<div class="box"><p>MediBalans is the official Swedish distributor for Genova Diagnostics. Analyses are ordered after clinical assessment, sampling is usually done at home, and results are interpreted by a licensed physician alongside your history.</p></div></section>
<section id="yourself"><h2>What you can do <em>first</em></h2>{sjalv}</section>
<section id="related"><h2>Read <em>further</em></h2><div class="card-grid">{cards}</div>
<p style="margin-top:1.5rem"><a href="/en/symptoms/">All symptom guides →</a> · <a href="/en/genova-diagnostics/">All analyses</a> · <a href="{sv_url}">Svenska</a></p></section>
<section id="faq"><h2>Frequently asked <em>questions</em></h2>{faq_html(g['faq'])}</section>
</div>
{band('Find out', 'why', 'An initial consultation gives a clinical assessment of your situation and a clear next step — which investigation is warranted, and which is not.')}
"""
    return page(g["title"], g["desc"], url, sv_url, schema, content)


def build_index():
    url = f"{BASE}/en/symptoms/"
    sv_url = f"{BASE}/symtom/"
    cards = "".join(
        f'<a class="mb-card" href="/en/symptoms/{g["slug"]}/"><span class="k">{g["kicker"].split("·")[-1].strip()}</span>'
        f'<div class="t">{g["h1"].rstrip(" —")}</div><p class="d">{g["lead"][:140]}…</p>'
        f'<div class="p">Read the guide →</div></a>' for g in GUIDES)
    schema = ['<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage", "@id": url + "#collection",
        "url": url, "name": "Symptom guides — MediBalans", "inLanguage": "en-GB", "publisher": ORG,
        "hasPart": [{"@type": "MedicalWebPage", "url": f"{BASE}/en/symptoms/{g['slug']}/", "name": g["title"]}
                    for g in GUIDES]}, ensure_ascii=False) + "</script>"]
    content = f"""
{hero('Symptom guide · MediBalans Stockholm', 'Symptom guides ', 'Start with how you feel.',
      'Guides written around symptoms rather than diagnoses. Each one covers the most common causes, when to seek conventional care instead, what can actually be measured objectively — and what you can do yourself first.',
      '<a class="btn-p" href="/en/#booking">Book a consultation</a><a class="btn-s" href="/en/genova-diagnostics/">Diagnostics</a>',
      'These guides do not replace medical assessment. For red-flag symptoms, conventional care applies.',
      [(str(len(GUIDES)), 'Published guides'), ('Home kit', 'Sampling'), ('2–3 wks', 'Turnaround'), ('Physician', 'Interpretation')])}
<div class="container sec-body" style="max-width:1100px">
<section id="guides"><h2>Choose what <em>sounds like you</em></h2><div class="card-grid">{cards}</div></section>
</div>
<div class="container sec-body">
<section id="principle"><h2>The same <em>principle</em> in every guide</h2>
<p>Each guide follows the same order, and that order is deliberate. First what the symptom usually stems from. Then the signs that should take you to conventional care rather than to an investigation with us. Then what can actually be measured objectively. Last, what you can do yourself — including the free steps within the healthcare system that should be completed before anything more advanced is meaningful.</p>
<div class="box"><p>The right investigation is the smallest one that answers your clinical question. A comprehensive panel ordered without a question gives limited guidance, however many markers it contains.</p></div>
<p style="margin-top:1.4rem"><a href="{sv_url}">Läs på svenska →</a></p></section>
</div>
{band('Find out', 'why', 'An initial consultation gives a clinical assessment and a clear next step.')}
"""
    return page("Symptom guides — from symptom to measurable cause | MediBalans",
                "Guides by symptom: bloating, fatigue despite sleep, food reactions, brain fog and hormonal symptoms after 40. Common causes, when to seek care and what can be measured.",
                url, sv_url, schema, content)


# ═══════════════════════════════════════════════════ WRITINGS (EN)
ESSAY_SECTIONS = [
    ("category-error", "The category error", [
        "Allergy in the strict sense is IgE-mediated. Immunoglobulin E binds to mast cells, the reaction appears within minutes, it is predictable and it can be life-threatening. This is a well-defined and well-validated clinical phenomenon, and that investigation belongs with an allergist when suspicion exists.",
        "Cellular reactivity to foods is something else. It arises largely from the innate immune system — granulocytes and other cells responding to substances they do not recognise as harmless. The reaction appears hours to days later, it is dose-dependent and it is rarely dramatic. It does not cause anaphylaxis. It causes low-grade, recurring inflammation.",
        "When these two are merged under the word &ldquo;food allergy&rdquo;, a category error follows with two unfortunate consequences. Patients with negative IgE tests are told food cannot be involved, despite clearly reacting. And patients with cellular reactivity believe they carry a dangerous allergy, which as a rule they do not.",
    ]),
    ("recognition", "Recognition, not disease", [
        "The immune system's fundamental task is to determine what belongs in the body and what does not. It is a recognition apparatus, calibrated over a long period against a particular environment.",
        "That environment has changed faster than the calibration has followed. Industrially processed proteins, hydrolysates, emulsifiers, preservatives, colourings and residues from cultivation and packaging — most of this has been introduced over a period that is, in evolutionary terms, negligible. The immune system therefore regularly encounters molecules it has no inherited reason to regard as food.",
        "From that perspective a cellular reaction is not a fault in the system. It is the system doing exactly what it was built to do, against input it was not built to meet. This is why I regard the finding as an expression of mismatch rather than of disease.",
    ]),
    ("consequence", "The clinical consequence", [
        "The distinction is not semantic. It determines how a treatment plan is understood and therefore whether it is followed.",
        "If a patient understands an elimination plan as a list of forbidden foods, it becomes a question of discipline, and discipline runs out. If the same plan is understood as a return to what their own biology actually recognises, it becomes intelligible — and intelligibility is, in my experience, a stronger driver of adherence than willpower.",
        "Equally important is that elimination here is a time-limited tool, not a permanent state. The purpose is to lower the inflammatory burden long enough for tolerance to recover, after which foods are reintroduced in a structured way. A plan without a reintroduction phase has misunderstood its own purpose.",
    ]),
    ("evidence", "What the evidence supports — and does not", [
        "Methodological criticism of cellular reactivity testing exists and should not be waved away. The most cited objection concerns reproducibility in split samples. That criticism is relevant to how a result should be interpreted, and it is one reason I never read a test result in isolation.",
        "At the same time controlled evidence exists. In a double-blind, placebo-controlled trial at Yale, elimination diets based on cellular reactivity testing were tested in patients with irritable bowel syndrome, with symptom improvement in the active group. Mechanistic work from the same research environment has since examined how foods can trigger DNA release from innate immune cells. Earlier randomised work examined body composition under reactivity-guided diets.",
        "What this supports collectively is that reactivity-guided elimination can produce clinical effect. What it does not support is the claim that the test alone explains a patient's entire clinical picture. Reactivity is as a rule a dominant driver among several — not a monocausal explanation — and anyone promising the latter is selling something other than medicine.",
    ]),
    ("limits", "What this text does not claim", [
        "This is a clinical observation and an interpretive frame, not proof of mechanism. The frame is productive in my work because it explains patterns I see recur and because it gives patients an intelligible why. It has not been tested as a hypothesis in its own right.",
        "Cellular reactivity testing does not replace allergy investigation, coeliac investigation or investigation of inflammatory bowel disease. For red-flag symptoms, conventional management applies regardless of what any functional analysis shows.",
        "And a test result remains an input, not a verdict. What matters is not what the list contains but which clinical question it was meant to answer.",
    ]),
]

ESSAY_FAQ = [
    ("Is cellular food reactivity the same as allergy?",
     "No. Allergy in the strict sense is IgE-mediated, appears within minutes and can be life-threatening. Cellular reactivity arises largely from the innate immune system, appears hours to days after intake and produces low-grade inflammation rather than acute reaction. They are different phenomena and require different investigation."),
    ("What is meant by evolutionary mismatch?",
     "That the immune system's recognition apparatus is calibrated against a food environment that is no longer the one we live in. Industrially processed proteins, additives and residues have been introduced over a period that is negligible in evolutionary terms. A cellular reaction to such substances is therefore not necessarily a fault in the system but the system working against input it was not built for."),
    ("Does it mean I can never eat those foods again?",
     "No. Elimination is a time-limited tool whose purpose is to lower the inflammatory burden long enough for tolerance to recover. A plan without a structured reintroduction phase has misunderstood its own purpose."),
    ("Is the method scientifically supported?",
     "There is controlled evidence, including a double-blind placebo-controlled trial at Yale in patients with irritable bowel syndrome and subsequent mechanistic work. There is also methodological criticism, principally concerning reproducibility in split samples. My conclusion is that reactivity-guided elimination can produce clinical effect, but that a test result should never be read in isolation."),
]

ESSAY_SOURCES = [
    "Ali A, Weiss TR, McKee D, et al. Efficacy of individualised diets in patients with irritable bowel syndrome: a randomised controlled trial. <em>BMJ Open Gastroenterology</em> 2017.",
    "Garcia-Martinez I, Weiss TR, Yousaf MN, Ali A, Mehal WZ. A leukocyte activation test identifies food items which induce release of DNA by innate immune peripheral blood leucocytes. <em>Nutrition &amp; Metabolism</em> 2018.",
    "Kaats GR, Pullin D, Parker LK. The short term efficacy of the ALCAT test of food sensitivities to facilitate changes in body composition and self-reported disease symptoms. <em>The Bariatrician</em> 1996.",
]


def build_essay():
    url = f"{BASE}/en/writings/evolutionary-mismatch/"
    sv_url = f"{BASE}/skrifter/evolutionar-missmatchning/"
    anchors = [(a, t) for a, t, _ in ESSAY_SECTIONS] + [("faq", "FAQ")]
    secs = "".join(f'<section id="{a}"><h2>{t}</h2>' + "".join(f"<p>{p}</p>" for p in ps) + "</section>"
                   for a, t, ps in ESSAY_SECTIONS)
    sources = "".join(f"<li>{s}</li>" for s in ESSAY_SOURCES)
    desc = ("The question is not whether you have become allergic to food, but what the immune system recognises. "
            "Mario Anthis on why cellular food reactivity should be understood as recognition rather than disease.")
    schema = [
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@graph": [
                AUTHOR_NODE,
                {"@type": "Article", "@id": url + "#article", "url": url,
                 "headline": "Evolutionary mismatch — what a cellular reactivity test actually measures",
                 "description": desc, "inLanguage": "en-GB",
                 "datePublished": "2026-07-28", "dateModified": "2026-07-28",
                 "author": {"@id": AUTHOR_ID}, "publisher": ORG,
                 "isPartOf": {"@id": f"{BASE}/en/writings/#collection"},
                 "genre": "Clinical observation and hypothesis"}]}, ensure_ascii=False) + "</script>",
        faq_schema(url, ESSAY_FAQ),
    ]
    content = f"""
{hero('Writings · Mario Anthis', 'Evolutionary mismatch ', 'What the test actually measures.',
      'The question I am asked most often is whether the patient has become allergic to food. Almost always the answer is no — and the question leads in the wrong direction. What a cellular reactivity test measures is not allergy. It is recognition.',
      '<a class="btn-p" href="/en/#booking">Book a consultation</a><a class="btn-s" href="/en/writings/">All writings</a>',
      'Written by Mario Anthis, founder and medical director. Clinical observation and hypothesis — not established evidence.',
      [('Writings', 'Authored text'), ('Anthis', 'Author'), ('2026', 'Published'), ('Hypothesis', 'Type')])}
{toc(anchors)}
<div class="container sec-body">
<section><div class="box"><p><strong>About this text.</strong> Writings is my own section for clinical observations, hypotheses and reasoning. The content is written in the first person and should be read as clinical experience and an interpretive frame — not as established evidence or treatment recommendation. Where evidence is invoked, the source is given.</p></div></section>
{secs}
<section id="faq"><h2>Frequently asked <em>questions</em></h2>{faq_html(ESSAY_FAQ)}</section>
<section id="sources"><h2>Sources</h2><ol class="src">{sources}</ol>
<p style="margin-top:1.6rem"><a href="/en/alcat-test/">Read about immune reactivity testing →</a> · <a href="/en/symptoms/food-reactions/">Symptom guide: I react to almost everything I eat</a> · <a href="{sv_url}">Svenska</a></p></section>
</div>
{band('Measurement', 'before interpretation', 'The reasoning above is an interpretive frame. What applies in an individual case is decided by measured data and clinical assessment — not by a model.')}
"""
    return page("Evolutionary mismatch — what a cellular reactivity test actually measures | MediBalans",
                desc, url, sv_url, schema, content)


def build_writings_index():
    url = f"{BASE}/en/writings/"
    sv_url = f"{BASE}/skrifter/"
    card = ('<a class="mb-card" href="/en/writings/evolutionary-mismatch/"><span class="k">Immunology</span>'
            '<div class="t">Evolutionary mismatch</div>'
            '<p class="d">What a cellular reactivity test actually measures — recognition rather than disease.</p>'
            '<div class="p">Mario Anthis · 2026</div></a>')
    schema = ['<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@graph": [
            AUTHOR_NODE,
            {"@type": "CollectionPage", "@id": url + "#collection", "url": url,
             "name": "Writings — Mario Anthis", "inLanguage": "en-GB",
             "author": {"@id": AUTHOR_ID}, "publisher": ORG}]}, ensure_ascii=False) + "</script>"]
    content = f"""
{hero('Writings · Mario Anthis', 'Writings ', 'What twenty-five years taught me.',
      'This section is my own. Here I write in the first person about clinical patterns I see recur, about interpretive frames that have proved productive, and about where I consider the established understanding insufficient. These texts are experience and hypothesis — not established evidence.',
      '<a class="btn-p" href="/en/#booking">Book a consultation</a><a class="btn-s" href="/en/clinical-notes/">Clinical notes</a>',
      'For institutional review of the evidence, see Clinical notes.',
      [('1', 'Published text'), ('Anthis', 'Author'), ('English', 'Language'), ('Ongoing', 'Publication')])}
<div class="container sec-body">
<section id="about"><h2>Three layers, <em>three jobs</em></h2>
<p>The site carries three kinds of text and they do different things. Keeping them apart makes each more useful.</p>
<table><tbody>
<tr><td><strong><a href="/en/symptoms/">Symptom guides</a></strong></td><td>Written for those searching by how they feel. Possible causes and what can be measured.</td></tr>
<tr><td><strong><a href="/en/clinical-notes/">Clinical notes</a></strong></td><td>Institutional review of the evidence for a specific method or question.</td></tr>
<tr><td><strong>Writings</strong></td><td>My own texts. First person, hypothesis and clinical experience — with stated limits on what they claim.</td></tr>
</tbody></table></section>
<section id="texts"><h2>Published <em>texts</em></h2><div class="card-grid">{card}</div>
<p style="margin-top:1.4rem"><a href="{sv_url}">Läs på svenska →</a></p></section>
</div>
{band('Measure', 'first', 'Every argument here rests on the same principle: measurement before interpretation, interpretation before treatment.')}
"""
    return page("Writings — Mario Anthis | MediBalans",
                "Clinical observations, hypotheses and reasoning by Mario Anthis, founder and medical director at MediBalans. Authored texts — experience and interpretive frame, not established evidence.",
                url, sv_url, schema, content)


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)
    print("  ", rel, f"({len(content):,} chars)")


if __name__ == "__main__":
    print("EN symptom guides:")
    write("en/symptoms/index.html", build_index())
    for g in GUIDES:
        write(f"en/symptoms/{g['slug']}/index.html", build_guide(g))
    print("\nDone.")
