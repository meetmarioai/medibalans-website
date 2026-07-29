# -*- coding: utf-8 -*-
"""
MediBalans · kanonisk navigation
=================================
EN källa för menyn. Desktop och mobil GENERERAS UR SAMMA DATASTRUKTUR,
vilket gör det omöjligt för dem att glida isär. Svenska och engelska
menyn har identisk struktur post för post.

Bakgrund: revisionen visade att 49 av 94 sidor hade en mobilmeny minst
tre poster kortare än desktop, och att menyn i övrigt varierade mellan
sidor. Efter detta har varje sida exakt samma meny.

Importeras av apply_canonical_nav.py.
"""

# Struktur: (typ, etikett, href, barn)
#   "link"    — enkel länk
#   "menu"    — dropdown med barn
# Barn: (etikett, href, är_undernivå)

NAV_SV = [
    ("link", "Kliniken", "/#about", []),
    ("link", "Metoden", "/#process", []),
    ("menu", "Utredningar", "/#investigate", [
        ("Symtomguider", "/symtom/", False),
        ("Baby Balans — före graviditet", "/baby-balans/", False),
        ("IBS &amp; Tarmhälsa", "/ibs-tarmhalsa/", False),
        ("Kronisk Trötthet &amp; ME/CFS", "/utmattning/", False),
        ("Autoimmunitet", "/autoimmun/", False),
        ("Hudsjukdomar", "/hudsjukdomar/", False),
        ("ADHD &amp; Neuropsykiatri", "/adhd-neuropsykiatri/", False),
        ("Sköldkörtel &amp; Hormoner", "/hypothyreos/", False),
        ("Kognitiv Hälsa &amp; Alzheimer", "/kognitiv-halsa/", False),
    ]),
    ("menu", "Diagnostik", "/#testing", [
        ("ALCAT — Livsmedelsintolerans", "/alcat/", False),
        ("CMA — Cellulär Mikronäring", "/cma/", False),
        ("MethylDetox — 38 Gener", "/methyldetox/", False),
        ("Biologisk Ålder", "/biologisk-alder/", False),
        ("Alzheimers-utredning", "/alzheimers-test/", False),
        ("HRV-Analys", "/hrv-analys/", False),
        ("Kroppsskanning — InBody", "/kroppsskanning/", False),
    ]),
    ("menu", "Genova", "/genova-diagnostics/", [
        ("Alla tester", "/genova-diagnostics/", False),
        ("GI Effects&#174;", "/gi-effects-test/", False),
        ("NutrEval&#174;", "/nutreval-sverige/", False),
        ("Metabolomik", "/metabolomik/", False),
        ("SIBO-test", "/sibo-test/", False),
        ("Hormonpaneler", "/genova-hormontest/", False),
        ("Organix&#174;", "/organix/", False),
        ("Fettsyror", "/fettsyror/", False),
        ("Adrenal Stress", "/adrenal-stress/", False),
        ("Essential Östrogen", "/essential-ostrogen/", False),
        ("Menopaus Plus", "/menopaus-plus/", False),
        ("Kvinnohälsa", "/kvinnohalsa/", False),
    ]),
    ("menu", "IV-Behandling", "/iv-terapi/", [
        ("IV- &amp; IM-terapi", "/iv-terapi/", False),
        ("↳ D-vitamin 100 000 IE", "/iv-terapi/d-vitamin/", True),
    ]),
    ("link", "Familjer", "/#families", []),
    ("link", "Kunskapsbank", "/kunskapsbank/", []),
    ("menu", "Forskning", "/forskning.html", [
        ("Skrifter — Mario Anthis", "/skrifter/", False),
        ("Teorem — falsifierbara satser", "/teorem/", False),
        ("Forskningsprogram", "/forskning.html", False),
        ("Kliniska Noteringar", "/clinical-notes/", False),
        ("Homocystein &amp; metylering", "/homocystein/", False),
        ("Rätt form av tillskott", "/ratt-form-av-tillskott/", False),
        ("Global Constraint Rule", "/global-constraint-rule/", False),
        ("Longevitet", "/longevitet-halsospann/", False),
    ]),
    ("link", "Frågor", "/#faq", []),
]

NAV_EN = [
    ("link", "Clinic", "/en/#about", []),
    ("link", "Method", "/en/#process", []),
    ("menu", "Conditions", "/en/#investigate", [
        ("Symptom Guides", "/en/symptoms/", False),
        ("Baby Balans — preconception", "/en/baby-balans/", False),
        ("IBS &amp; Gut Health", "/en/ibs-gut-health/", False),
        ("Chronic Fatigue &amp; ME/CFS", "/en/chronic-fatigue/", False),
        ("Autoimmunity", "/en/autoimmunity/", False),
        ("Skin Conditions", "/en/skin-conditions/", False),
        ("ADHD &amp; Neuropsychiatry", "/en/adhd-neuropsychiatry/", False),
        ("Thyroid &amp; Hormones", "/en/thyroid/", False),
        ("Cognitive Health &amp; Alzheimer's", "/en/cognitive-health/", False),
    ]),
    ("menu", "Diagnostics", "/en/#testing", [
        ("ALCAT — Food Intolerance", "/en/alcat-test/", False),
        ("CMA — Cellular Nutrients", "/en/cellular-nutrient-analysis/", False),
        ("MethylDetox — 38 Genes", "/en/methylation-test/", False),
        ("Biological Age", "/en/biological-age/", False),
        ("Alzheimer's Assessment", "/en/alzheimers-assessment/", False),
        ("HRV Analysis", "/en/hrv-analysis/", False),
        ("Body Composition — InBody", "/en/body-composition-analysis/", False),
    ]),
    ("menu", "Genova", "/en/genova-diagnostics/", [
        ("All tests", "/en/genova-diagnostics/", False),
        ("GI Effects&#174;", "/en/gi-effects-test/", False),
        ("NutrEval&#174;", "/en/nutreval-test/", False),
        ("Metabolomics", "/en/metabolomics/", False),
        ("SIBO Breath Test", "/en/sibo-test/", False),
        ("Hormonal Panels", "/en/genova-hormones/", False),
        ("Organix&#174;", "/en/organix/", False),
        ("Fatty Acids", "/en/fatty-acids/", False),
        ("Adrenal Stress", "/en/adrenal-stress/", False),
        ("Essential Estrogens", "/en/essential-estrogens/", False),
        ("Menopause Plus", "/en/menopause-plus/", False),
        ("Women's Health", "/en/womens-health/", False),
    ]),
    ("menu", "IV Therapy", "/en/iv-therapy/", [
        ("IV &amp; IM Therapy", "/en/iv-therapy/", False),
        ("↳ Vitamin D 100,000 IU", "/en/iv-therapy/vitamin-d/", True),
    ]),
    ("link", "Families", "/en/#families", []),
    ("link", "Knowledge base", "/en/knowledge-base/", []),
    ("menu", "Research", "/en/research/", [
        ("Writings — Mario Anthis", "/en/writings/", False),
        ("Theorems — propositions", "/en/theorems/", False),
        ("Research Programme", "/en/research/", False),
        ("Clinical Notes", "/en/clinical-notes/", False),
        ("Homocysteine &amp; methylation", "/en/homocysteine/", False),
        ("Supplement forms", "/en/supplement-forms/", False),
        ("Global Constraint Rule", "/en/global-constraint-rule/", False),
        ("Longevity", "/en/longevity-healthspan/", False),
    ]),
    ("link", "FAQ", "/en/#faq", []),
]

LANG = {
    "sv": dict(nav=NAV_SV, switch_label="EN", switch_long="EN — English version",
               switch_href="/en/", book="Boka Konsultation", book_href="/#booking"),
    "en": dict(nav=NAV_EN, switch_label="SV", switch_long="SV — Svenska",
               switch_href="/", book="Book Consultation", book_href="/en/#booking"),
}


def desktop_html(lang):
    cfg = LANG[lang]
    parts = []
    for kind, label, href, kids in cfg["nav"]:
        if kind == "link":
            parts.append(f'      <a href="{href}">{label}</a>')
        else:
            inner = "".join(
                f'\n          <a href="{k_href}">{k_label}</a>'
                for k_label, k_href, _sub in kids)
            parts.append(
                '      <div class="nav-dropdown">\n'
                f'        <button class="nav-dd-btn" aria-expanded="false">{label} '
                '<span class="dd-chevron">▾</span></button>\n'
                f'        <div class="dropdown-menu">{inner}\n        </div>\n'
                '      </div>')
    parts.append(f'      <a href="{cfg["switch_href"]}" class="lang-toggle">{cfg["switch_label"]}</a>')
    parts.append(f'      <a href="{cfg["book_href"]}" class="nav-cta">{cfg["book"]}</a>')
    return "\n".join(parts)


def mobile_html(lang):
    """Mobilmenyn plattar ut varje dropdown till sina underposter. Om
    ordningen följer desktop hamnar därför en toppnivålänk som ligger
    efter dropdownsen på plats ~34 av 45 — bortom all rimlig scrollning.
    Kunskapsbanken drabbades av exakt det. Enkla länkar emitteras därför
    FÖRST i mobilen, sektionerna efter."""
    cfg = LANG[lang]
    out = []
    enkla = [(l, h) for kind, l, h, _ in cfg["nav"] if kind == "link"
             for l, h in [(l, h)]]
    for label, href in enkla:
        out.append(f'  <a href="{href}" onclick="closeMobile()">{label}</a>')
    for kind, label, href, kids in cfg["nav"]:
        if kind == "link":
            continue
        out.append(f'  <div class="mob-section-label">— {label} —</div>')
        for k_label, k_href, sub in kids:
            cls = "mobile-sub" if sub else "sub"
            out.append(f'  <a href="{k_href}" onclick="closeMobile()" class="{cls}">{k_label}</a>')
    out.append(f'  <a href="{cfg["switch_href"]}" onclick="closeMobile()" class="lang-link">{cfg["switch_long"]}</a>')
    out.append(f'  <a href="{cfg["book_href"]}" onclick="closeMobile()" class="mob-cta">{cfg["book"]}</a>')
    return "\n".join(out)


def all_hrefs(lang):
    """Alla interna href i menyn — för paritetskontroll."""
    out = []
    for kind, label, href, kids in LANG[lang]["nav"]:
        if kind == "link":
            out.append(href)
        for k_label, k_href, _s in kids:
            out.append(k_href)
    out.append(LANG[lang]["switch_href"])
    out.append(LANG[lang]["book_href"])
    return out


if __name__ == "__main__":
    for lang in ("sv", "en"):
        d = [h for h in all_hrefs(lang)]
        print(f"{lang.upper()}: {len(d)} länkar i kanonisk meny")
