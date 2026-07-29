# -*- coding: utf-8 -*-
"""
MediBalans · Kunskapsbank — genererad artikeldatabas
=====================================================
Bygger /kunskapsbank/ genom att SKANNA repot i stället för att underhålla
en handskriven lista. Titel, beskrivning, typ och längd läses ur varje
sida, så indexet kan aldrig hamna i otakt med innehållet — kör om
skriptet efter att en ny artikel lagts till.

Sidan har klientsidig sökning och kategorifiltrering (ingen backend),
ItemList- och CollectionPage-schema, och samma skal som övriga sidor.

Kategorisering sker på sökväg och innehåll:
  Symtomguide      /symtom/*
  Skrift           /skrifter/*        författad, första person
  Klinisk notering fristående noteringar och jämförelser
  Diagnostik       testpaneler
  Utredning        tillståndssidor

Kör:  python3 scripts/build_library.py
"""
import html as H
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_new_sections import page as sv_page, hero as sv_hero, band as sv_band, ROOT, BASE
from build_content_en import page as en_page, hero as en_hero, band as en_band

SV_URL = f"{BASE}/kunskapsbank/"
EN_URL = f"{BASE}/en/knowledge-base/"
ORG = {"@id": f"{BASE}/#organization"}

# ------------------------------------------------------------------ kategorier
KLINISKA_NOTERINGAR = {
    "homocystein", "mikronaringstest-jamforelse", "ibs-grundorsaker",
    "ostrogenmetabolism-forklarad", "tarmtest-guide", "utmattningssyndrom-biologi",
    "utredningsprotokoll", "global-constraint-rule",
}
DIAGNOSTIK = {
    "alcat", "cma", "methyldetox", "biologisk-alder", "alzheimers-test",
    "hrv-analys", "kroppsskanning", "gi-effects-test", "nutreval-sverige",
    "metabolomik", "sibo-test", "genova-hormontest", "organix", "fettsyror",
    "adrenal-stress", "essential-ostrogen", "menopaus-plus", "kvinnohalsa",
    "genova-diagnostics",
}
UTREDNINGAR = {
    "ibs-tarmhalsa", "utmattning", "autoimmun", "hudsjukdomar",
    "adhd-neuropsykiatri", "hypothyreos", "kognitiv-halsa", "baby-balans",
    "ibs-utredning-och-behandling", "longevitet-halsospann", "iv-terapi",
}
EN_KLINISKA = {
    "micronutrient-test-comparison", "ibs-root-causes", "estrogen-metabolism-explained",
    "gut-test-guide", "chronic-fatigue-biology", "investigation-protocol",
    "global-constraint-rule", "homocysteine",
}
EN_DIAGNOSTIK = {
    "alcat-test", "cellular-nutrient-analysis", "methylation-test", "biological-age",
    "alzheimers-assessment", "hrv-analysis", "body-composition-analysis", "gi-effects-test",
    "nutreval-test", "metabolomics", "sibo-test", "genova-hormones", "organix", "fatty-acids",
    "adrenal-stress", "essential-estrogens", "menopause-plus", "womens-health",
    "genova-diagnostics",
}
EN_UTREDNINGAR = {
    "ibs-gut-health", "chronic-fatigue", "autoimmunity", "skin-conditions",
    "adhd-neuropsychiatry", "thyroid", "cognitive-health", "baby-balans",
    "ibs-investigation-and-treatment", "longevity-healthspan", "iv-therapy",
}
EN_UNDANTAG = {"privacy-policy", "clinical-notes", "symptoms", "writings", "research",
               "theorems", "knowledge-base", "baby-balans"}

# sidor som inte hör hemma i en kunskapsbank
UNDANTAG = {".", "integritetspolicy", "clinical-notes", "symtom", "skrifter", "forskning"}

FARG = {
    "Symtomguide": "sym", "Symptom guide": "sym",
    "Skrift": "skr", "Writing": "skr",
    "Klinisk notering": "kli", "Clinical note": "kli",
    "Diagnostik": "dia", "Diagnostics": "dia",
    "Utredning": "utr", "Investigation": "utr",
}


def klassificera(slug, lang="sv"):
    top = slug.split("/")[0]
    if lang == "sv":
        if slug.startswith("symtom/"):
            return "Symtomguide"
        if slug.startswith("skrifter/"):
            return "Skrift"
        if top in KLINISKA_NOTERINGAR:
            return "Klinisk notering"
        if top in DIAGNOSTIK:
            return "Diagnostik"
        if top in UTREDNINGAR:
            return "Utredning"
        return None
    if slug.startswith("symptoms/"):
        return "Symptom guide"
    if slug.startswith("writings/"):
        return "Writing"
    if top in EN_KLINISKA:
        return "Clinical note"
    if top in EN_DIAGNOSTIK:
        return "Diagnostics"
    if top in EN_UTREDNINGAR:
        return "Investigation"
    return None


def las(p):
    h = open(p, encoding="utf-8").read()
    m = re.search(r"<title[^>]*>(.*?)</title>", h, re.S)
    titel = re.sub(r"\s+", " ", m.group(1)).split("|")[0].strip() if m else ""
    d = re.search(r'name="description"[^>]*content="(.*?)"', h, re.S) or \
        re.search(r'content="(.*?)"[^>]*name="description"', h, re.S)
    desc = re.sub(r"\s+", " ", d.group(1)).strip() if d else ""
    # ordantal i brödtext
    t = re.sub(r"<(script|style)\b.*?</\1>", "", h, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    ord_ = len(re.sub(r"\s+", " ", t).split())
    return titel, desc, ord_


def samla(lang="sv"):
    ut = []
    rot = ROOT if lang == "sv" else os.path.join(ROOT, "en")
    for dp, dirs, fs in os.walk(rot):
        dirs[:] = [d for d in dirs
                   if d not in (".git", "node_modules", "scripts", ".vercel",
                                "api", "downloads") and not d.startswith(".")
                   and not (lang == "sv" and d == "en")]
        for fn in fs:
            if fn != "index.html":
                continue
            p = os.path.join(dp, fn)
            if os.path.getsize(p) < 3000:
                continue
            slug = os.path.relpath(dp, rot).replace("\\", "/")
            if lang == "sv" and slug in UNDANTAG:
                continue
            if lang == "en" and (slug in EN_UNDANTAG or slug == "."):
                continue
            kat = klassificera(slug, lang)
            if not kat:
                continue
            titel, desc, ord_ = las(p)
            if not titel:
                continue
            ut.append(dict(slug=slug, kat=kat, titel=titel, desc=desc, ord=ord_))
    ut.sort(key=lambda x: (x["kat"], x["titel"]))
    return ut


CSS = """
.kb-tools{display:flex;gap:1rem;flex-wrap:wrap;align-items:center;margin:2rem 0 1.2rem}
.kb-search{flex:1;min-width:260px;padding:.85rem 1rem;border:1px solid var(--border);
  border-radius:4px;font-family:var(--font-body);font-size:.95rem;color:var(--text);background:#fff}
.kb-search:focus{outline:none;border-color:var(--blue)}
.kb-filters{display:flex;gap:.5rem;flex-wrap:wrap}
.kb-chip{border:1px solid var(--border);background:#fff;color:var(--text-mid);
  padding:.5rem .95rem;border-radius:999px;font-size:.82rem;cursor:pointer;
  font-family:var(--font-body);transition:all .15s}
.kb-chip:hover{border-color:var(--blue);color:var(--navy)}
.kb-chip.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.kb-count{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.12em;
  text-transform:uppercase;color:var(--text-light);margin-bottom:1rem}
.kb-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1rem}
.kb-card{border:1px solid var(--border);background:#fff;padding:1.5rem;text-decoration:none;
  display:flex;flex-direction:column;transition:border-color .18s,transform .18s}
.kb-card:hover{border-color:var(--blue);transform:translateY(-2px)}
.kb-tag{font-family:var(--font-mono);font-size:.6rem;letter-spacing:.14em;text-transform:uppercase;
  display:inline-block;padding:.25rem .6rem;border-radius:3px;margin-bottom:.75rem;align-self:flex-start}
.kb-tag.sym{background:#EDF5FA;color:#2E6B9E}
.kb-tag.skr{background:#F5F0E8;color:#8A6432}
.kb-tag.kli{background:#E8F0EC;color:#2F6B4F}
.kb-tag.dia{background:#EAEDF5;color:#3F4E8C}
.kb-tag.utr{background:#F5EAEA;color:#8C3F3F}
.kb-card h3{font-family:var(--font-display);font-weight:400;font-size:1.12rem;line-height:1.32;
  color:var(--navy);margin:0 0 .5rem}
.kb-card p{font-size:.86rem;color:var(--text-mid);line-height:1.6;margin:0 0 1rem;flex:1}
.kb-meta{font-family:var(--font-mono);font-size:.65rem;letter-spacing:.1em;color:var(--text-light);
  text-transform:uppercase;border-top:1px solid var(--border);padding-top:.7rem}
.kb-empty{padding:3rem 0;text-align:center;color:var(--text-light)}
@media(max-width:700px){.kb-tools{flex-direction:column;align-items:stretch}}
"""

JS = """
<script>
(function(){
  var q=document.getElementById('kbSearch');
  var chips=[].slice.call(document.querySelectorAll('.kb-chip'));
  var cards=[].slice.call(document.querySelectorAll('.kb-card'));
  var count=document.getElementById('kbCount');
  var empty=document.getElementById('kbEmpty');
  var aktiv='alla';

  function normalisera(s){
    return (s||'').toLowerCase()
      .replace(/å|ä/g,'a').replace(/ö/g,'o').replace(/é/g,'e');
  }
  function uppdatera(){
    var term=normalisera(q.value.trim());
    var synliga=0;
    cards.forEach(function(c){
      var matchKat = aktiv==='alla' || c.dataset.kat===aktiv;
      var matchText = !term || normalisera(c.dataset.sok).indexOf(term)!==-1;
      var visa = matchKat && matchText;
      c.style.display = visa ? '' : 'none';
      if(visa) synliga++;
    });
    count.textContent = synliga + (synliga===1 ? ' artikel' : ' artiklar');
    empty.style.display = synliga ? 'none' : 'block';
  }
  q.addEventListener('input',uppdatera);
  chips.forEach(function(ch){
    ch.addEventListener('click',function(){
      chips.forEach(function(c){c.classList.remove('on');});
      ch.classList.add('on');
      aktiv=ch.dataset.kat;
      uppdatera();
    });
  });
  uppdatera();
})();
</script>
"""


def bygg(lang="sv"):
    sv = lang == "sv"
    url, other = (SV_URL, EN_URL) if sv else (EN_URL, SV_URL)
    poster = samla(lang)
    kats = sorted({p["kat"] for p in poster})
    pre = "" if sv else "en/"

    L = dict(
        alla="Alla" if sv else "All",
        artikel="artikel" if sv else "article",
        artiklar="artiklar" if sv else "articles",
        ord="ord" if sv else "words",
        sok=("Sök på symtom, analys eller nyckelord — t.ex. uppblåst, homocystein, MTHFR"
             if sv else "Search by symptom, analysis or keyword — e.g. bloating, homocysteine, MTHFR"),
        aria="Sök i kunskapsbanken" if sv else "Search the knowledge base",
        tom=("Inga träffar. Pröva ett bredare sökord, eller "
             '<a href="/#booking">boka en konsultation</a> så hjälper vi dig vidare.'
             if sv else "No results. Try a broader term, or "
             '<a href="/en/#booking">book a consultation</a> and we will help you further.'),
        blad="Bläddra" if sv else "Browse",
        boka="Boka konsultation" if sv else "Book a consultation",
        other="English" if sv else "Svenska",
    )

    chips = f'<button class="kb-chip on" data-kat="alla">{L["alla"]}</button>' + "".join(
        f'<button class="kb-chip" data-kat="{H.escape(k)}">{H.escape(k)}</button>' for k in kats)

    kort = ""
    for p in poster:
        sok = H.escape(f'{p["titel"]} {p["desc"]} {p["kat"]} {p["slug"]}', quote=True)
        antal = f'{p["ord"]:,}'.replace(",", " ")
        kort += (
            f'<a class="kb-card" href="/{pre}{p["slug"]}/" data-kat="{H.escape(p["kat"])}" data-sok="{sok}">'
            f'<span class="kb-tag {FARG[p["kat"]]}">{H.escape(p["kat"])}</span>'
            f'<h3>{H.escape(p["titel"])}</h3>'
            f'<p>{H.escape(p["desc"][:165])}{"…" if len(p["desc"]) > 165 else ""}</p>'
            f'<div class="kb-meta">{antal} {L["ord"]}</div></a>')

    per_kat = {k: sum(1 for p in poster if p["kat"] == k) for k in kats}

    schema = ['<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "@id": url + "#page", "url": url,
             "name": "Kunskapsbank — MediBalans" if sv else "Knowledge base — MediBalans",
             "inLanguage": "sv-SE" if sv else "en-GB",
             "publisher": ORG, "isPartOf": {"@id": f"{BASE}/#website"}},
            {"@type": "ItemList", "@id": url + "#list", "numberOfItems": len(poster),
             "itemListElement": [
                 {"@type": "ListItem", "position": i + 1,
                  "url": f'{BASE}/{pre}{p["slug"]}/', "name": p["titel"]}
                 for i, p in enumerate(poster)]}]}, ensure_ascii=False) + "</script>"]

    if sv:
        titel = "Kunskapsbank — kliniska noteringar, symtomguider och diagnostik | MediBalans"
        desc = (f"Samtliga {len(poster)} artiklar och diagnostiksidor samlade och sökbara: "
                "symtomguider, kliniska noteringar, skrifter av Mario Anthis och beskrivningar "
                "av varje analys vi använder.")
        eyebrow, h1, h1em = "Kunskapsbank", "Allt vi har skrivit, ", "på ett ställe."
        lead = ("Kliniska noteringar, symtomguider, författade texter och beskrivningar av varje analys "
                "vi arbetar med. Sök fritt eller filtrera på typ.")
        fine = "Uppdateras allteftersom nya texter publiceras."
        band_a, band_b = "Vet du inte", "var du ska börja"
        band_p = ("Rätt utredning avgörs av din frågeställning, inte av hur många markörer en panel "
                  "innehåller. En inledande konsultation ger ett tydligt nästa steg.")
        stats = [(str(len(poster)), "Artiklar")] + [(str(v), k) for k, v in list(per_kat.items())[:3]]
        booking = "/#booking"
    else:
        titel = "Knowledge base — clinical notes, symptom guides and diagnostics | MediBalans"
        desc = (f"All {len(poster)} articles and diagnostic pages, collected and searchable: symptom "
                "guides, clinical notes, writings by Mario Anthis and descriptions of every analysis we use.")
        eyebrow, h1, h1em = "Knowledge base", "Everything we have written, ", "in one place."
        lead = ("Clinical notes, symptom guides, authored texts and descriptions of every analysis we work "
                "with. Search freely or filter by type.")
        fine = "Updated as new texts are published."
        band_a, band_b = "Not sure", "where to start"
        band_p = ("The right investigation is determined by your clinical question, not by how many markers "
                  "a panel contains. An initial consultation gives a clear next step.")
        stats = [(str(len(poster)), "Articles")] + [(str(v), k) for k, v in list(per_kat.items())[:3]]
        booking = "/en/#booking"

    hero_f = sv_hero if sv else en_hero
    band_f = sv_band if sv else en_band

    innehall = f"""
{hero_f(eyebrow, h1, h1em, lead,
        f'<a class="btn-p" href="{booking}">{L["boka"]}</a><a class="btn-s" href="#bank">{L["blad"]}</a>',
        fine, stats)}
<div class="container" id="bank" style="padding-bottom:4rem">
  <div class="kb-tools">
    <input class="kb-search" id="kbSearch" type="search" placeholder="{H.escape(L['sok'])}" aria-label="{H.escape(L['aria'])}">
    <div class="kb-filters">{chips}</div>
  </div>
  <div class="kb-count" id="kbCount"></div>
  <div class="kb-grid">{kort}</div>
  <div class="kb-empty" id="kbEmpty" style="display:none"><p>{L["tom"]}</p></div>
  <p style="margin-top:2rem"><a href="{other}">{L["other"]}</a></p>
</div>
{band_f(band_a, band_b, band_p)}
{JS}
"""
    if sv:
        html = sv_page(titel, desc, url, schema, innehall).replace("</style>", CSS + "\n</style>", 1)
        m = re.search(r'<link rel="alternate" hreflang="sv" href="[^"]+">', html)
        if m:
            html = html.replace(m.group(0), m.group(0) + f'\n<link rel="alternate" hreflang="en" href="{other}">', 1)
        return html, len(poster), per_kat
    return en_page(titel, desc, url, other, schema, innehall).replace("</style>", CSS + "\n</style>", 1), len(poster), per_kat


if __name__ == "__main__":
    for lang, rel in (("sv", "kunskapsbank/index.html"), ("en", "en/knowledge-base/index.html")):
        html, n, per_kat = bygg(lang)
        p = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(html)
        print(f"   {rel} — {n} artiklar")
        for k, v in sorted(per_kat.items()):
            print(f"      {k:20} {v}")
