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
from build_new_sections import page, hero, band, ROOT, BASE

URL = f"{BASE}/kunskapsbank/"
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
# sidor som inte hör hemma i en kunskapsbank
UNDANTAG = {".", "integritetspolicy", "clinical-notes", "symtom", "skrifter", "forskning"}

FARG = {
    "Symtomguide": "sym",
    "Skrift": "skr",
    "Klinisk notering": "kli",
    "Diagnostik": "dia",
    "Utredning": "utr",
}


def klassificera(slug):
    top = slug.split("/")[0]
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


def samla():
    ut = []
    for dp, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs
                   if d not in (".git", "node_modules", "scripts", ".vercel",
                                "api", "downloads", "en") and not d.startswith(".")]
        for fn in fs:
            if fn != "index.html":
                continue
            p = os.path.join(dp, fn)
            if os.path.getsize(p) < 3000:
                continue
            slug = os.path.relpath(dp, ROOT).replace("\\", "/")
            if slug in UNDANTAG:
                continue
            kat = klassificera(slug)
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


def bygg():
    poster = samla()
    kats = sorted({p["kat"] for p in poster})

    chips = '<button class="kb-chip on" data-kat="alla">Alla</button>' + "".join(
        f'<button class="kb-chip" data-kat="{H.escape(k)}">{H.escape(k)}</button>' for k in kats)

    kort = ""
    for p in poster:
        sok = H.escape(f'{p["titel"]} {p["desc"]} {p["kat"]} {p["slug"]}', quote=True)
        kort += (
            f'<a class="kb-card" href="/{p["slug"]}/" data-kat="{H.escape(p["kat"])}" data-sok="{sok}">'
            f'<span class="kb-tag {FARG[p["kat"]]}">{H.escape(p["kat"])}</span>'
            f'<h3>{H.escape(p["titel"])}</h3>'
            f'<p>{H.escape(p["desc"][:165])}{"…" if len(p["desc"]) > 165 else ""}</p>'
            f'<div class="kb-meta">{p["ord"]:,} ord</div></a>'.replace(",", " "))

    per_kat = {k: sum(1 for p in poster if p["kat"] == k) for k in kats}

    schema = ['<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "@id": URL + "#page", "url": URL,
             "name": "Kunskapsbank — MediBalans", "inLanguage": "sv-SE",
             "description": "Samtliga kliniska noteringar, symtomguider, skrifter och diagnostiksidor.",
             "publisher": ORG, "isPartOf": {"@id": f"{BASE}/#website"}},
            {"@type": "ItemList", "@id": URL + "#list",
             "numberOfItems": len(poster),
             "itemListElement": [
                 {"@type": "ListItem", "position": i + 1,
                  "url": f'{BASE}/{p["slug"]}/', "name": p["titel"]}
                 for i, p in enumerate(poster)]}]}, ensure_ascii=False) + "</script>"]

    titel = "Kunskapsbank — kliniska noteringar, symtomguider och diagnostik | MediBalans"
    desc = (f"Samtliga {len(poster)} artiklar och diagnostiksidor samlade och sökbara: "
            "symtomguider, kliniska noteringar, skrifter av Mario Anthis och beskrivningar "
            "av varje analys vi använder.")

    innehall = f"""
{hero("Kunskapsbank", "Allt vi har skrivit, ", "på ett ställe.",
      "Kliniska noteringar, symtomguider, författade texter och beskrivningar av varje analys vi arbetar med. "
      "Sök fritt eller filtrera på typ.",
      '<a class="btn-p" href="/#booking">Boka konsultation</a>'
      '<a class="btn-s" href="#bank">Bläddra</a>',
      "Uppdateras allteftersom nya texter publiceras.",
      [(str(len(poster)), "Artiklar"),
       (str(per_kat.get("Symtomguide", 0)), "Symtomguider"),
       (str(per_kat.get("Klinisk notering", 0)), "Kliniska noteringar"),
       (str(per_kat.get("Diagnostik", 0)), "Analyser")])}
<div class="container" id="bank" style="padding-bottom:4rem">
  <div class="kb-tools">
    <input class="kb-search" id="kbSearch" type="search" placeholder="Sök på symtom, analys eller nyckelord — t.ex. uppblåst, homocystein, MTHFR" aria-label="Sök i kunskapsbanken">
    <div class="kb-filters">{chips}</div>
  </div>
  <div class="kb-count" id="kbCount"></div>
  <div class="kb-grid">{kort}</div>
  <div class="kb-empty" id="kbEmpty" style="display:none">
    <p>Inga träffar. Pröva ett bredare sökord, eller <a href="/#booking">boka en konsultation</a> så hjälper vi dig vidare.</p>
  </div>
</div>
{band("Vet du inte", "var du ska börja",
      "Rätt utredning avgörs av din frågeställning, inte av hur många markörer en panel innehåller. "
      "En inledande konsultation ger ett tydligt nästa steg.")}
{JS}
"""
    return page(titel, desc, URL, schema, innehall).replace(
        "</style>", CSS + "\n</style>", 1), len(poster), per_kat


if __name__ == "__main__":
    html, n, per_kat = bygg()
    p = os.path.join(ROOT, "kunskapsbank", "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(html)
    print(f"   kunskapsbank/index.html — {n} artiklar")
    for k, v in sorted(per_kat.items()):
        print(f"      {k:20} {v}")
