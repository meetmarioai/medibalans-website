# -*- coding: utf-8 -*-
"""
MediBalans · CMA vs SpectraCell — engelsk version
==================================================
Byggs ur det ENGELSKA sidskalet så att engelsk nav och footer följer med.
Innehållet importeras från build_cma_comparison.py.

Kör:  python3 scripts/build_cma_comparison_en.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from build_content_en import page as en_page, hero, toc, band, faq_html, faq_schema, BASE, ROOT
from build_cma_comparison import EN_SECTIONS, EN_FAQ, SV_SOURCES, SV_URL, EN_URL, ORG, AUTHOR_ID


def build():
    anchors = [(a, t.split(":")[0].split("—")[0].strip()) for a, t, _ in EN_SECTIONS]
    anchors.append(("faq", "FAQ"))

    body = "".join(
        f'<section id="{a}"><h2>{t}</h2>' + "".join(f"<p>{p}</p>" for p in ps) + "</section>"
        for a, t, ps in EN_SECTIONS)

    title = "CMA or SpectraCell? Two intracellular micronutrient tests compared | MediBalans"
    desc = ("CMA and SpectraCell both measure nutrient status inside white blood cells but use opposite designs — "
            "repletion in the patient's own serum versus depletion in an optimised medium, 55 analytes against 31. "
            "A methodological comparison with the evidence position stated openly.")

    schema = [
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@graph": [
                {"@type": "MedicalWebPage", "@id": EN_URL + "#page", "url": EN_URL, "name": title,
                 "inLanguage": "en-GB", "datePublished": "2026-07-28", "dateModified": "2026-07-28",
                 "audience": {"@type": "Patient"}, "author": {"@id": AUTHOR_ID},
                 "provider": ORG, "publisher": ORG}]}, ensure_ascii=False) + "</script>",
        faq_schema(EN_URL, EN_FAQ),
    ]

    note = ("<strong>About this text.</strong> This is a methodological comparison of two laboratory assays. "
            "It states openly that neither assay is established standard diagnostics and that both are assessed "
            "similarly by US payers. The comparison concerns construction and resolution, not evidentiary status.")

    content = f"""
{hero('Clinical note · Micronutrient diagnostics', 'CMA or SpectraCell? ', 'Two tests, two different questions.',
      "Both measure nutrient status inside the cell rather than in serum. The difference lies not in the ambition "
      "but in the construction — and that determines what the answer can be used for.",
      '<a class="btn-p" href="/en/#booking">Book a consultation</a>'
      '<a class="btn-s" href="/en/cellular-nutrient-analysis/">About CMA</a>',
      'Clinical note — methodological comparison, not a marketing claim.',
      [("55", "CMA analytes"), ("31", "SpectraCell analytes"),
       ("Autologous", "CMA serum"), ("2026", "Published")])}
{toc(anchors)}
<div class="container sec-body">
<section><div class="box"><p>{note}</p></div></section>
{body}
<section id="faq"><h2>Frequently asked <em>questions</em></h2>{faq_html(EN_FAQ)}</section>
<section id="sources"><h2>Sources</h2><ol class="src">{"".join(f"<li>{s}</li>" for s in SV_SOURCES)}</ol>
<p style="margin-top:1.5rem"><a href="/en/cellular-nutrient-analysis/">Read more about CMA →</a> · <a href="{SV_URL}">Svenska</a></p></section>
</div>
{band('Measurement', 'before interpretation',
      'Which assay is warranted depends on the clinical question — and conventional tests should be done first. '
      'An initial consultation determines what actually adds something.')}
"""
    html = en_page(title, desc, EN_URL, SV_URL, schema, content)
    return html.replace("</style>", "\n.src{font-size:.87rem;color:var(--text-mid)}.src li{margin-bottom:.6rem}\n</style>", 1)


if __name__ == "__main__":
    p = os.path.join(ROOT, "en/micronutrient-test-comparison/index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(build())
    print("   en/micronutrient-test-comparison/index.html skriven")
