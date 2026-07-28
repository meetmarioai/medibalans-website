# -*- coding: utf-8 -*-
"""
MediBalans · rätta döda navigationslänkar och språkläckage
===========================================================
A. DÖDA LÄNKAR
   Nio href:ar i navigationen pekar på sidor som inte finns. Samtliga har
   ett korrekt mål som verifierats existera i repot.

B. SPRÅKLÄCKAGE
   Tolv engelska sidor har svenska URL:er i navigationen. En engelsk
   besökare klickar på en menypost och hamnar på en svensk sida.
   Endast länkar INUTI nav-regionerna byts; den avsiktliga
   språkväxlaren till svenska lämnas orörd.

Torrkörning:  python3 scripts/fix_nav_links.py --dry
Skarpt:       python3 scripts/fix_nav_links.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
SKIP = (".git", "node_modules", "scripts", ".vercel")

# ---- A. döda länkar → verifierat existerande mål ----
DEAD = {
    "/en/methyldetox/": "/en/methylation-test/",
    "/en/alcat/": "/en/alcat-test/",
    "/en/alzheimers-test/": "/en/alzheimers-assessment/",
    "/en/autoimmune/": "/en/autoimmunity/",
    "/en/thyroid-hormones/": "/en/thyroid/",
    "/en/hormone-panels/": "/en/genova-hormones/",
    "/en/essential-estrogen/": "/en/essential-estrogens/",
    "/kronisk-trotthet/": "/utmattning/",
    "/autoimmunitet/": "/autoimmun/",
}

# ---- B. svensk URL → engelsk motsvarighet (endast på EN-sidor) ----
SV_TO_EN = {
    "/ibs-tarmhalsa/": "/en/ibs-gut-health/",
    "/utmattning/": "/en/chronic-fatigue/",
    "/autoimmun/": "/en/autoimmunity/",
    "/hudsjukdomar/": "/en/skin-conditions/",
    "/adhd-neuropsykiatri/": "/en/adhd-neuropsychiatry/",
    "/hypothyreos/": "/en/thyroid/",
    "/kognitiv-halsa/": "/en/cognitive-health/",
    "/alcat/": "/en/alcat-test/",
    "/cma/": "/en/cellular-nutrient-analysis/",
    "/methyldetox/": "/en/methylation-test/",
    "/biologisk-alder/": "/en/biological-age/",
    "/alzheimers-test/": "/en/alzheimers-assessment/",
    "/hrv-analys/": "/en/hrv-analysis/",
    "/kroppsskanning/": "/en/body-composition-analysis/",
    "/genova-diagnostics/": "/en/genova-diagnostics/",
    "/gi-effects-test/": "/en/gi-effects-test/",
    "/nutreval-sverige/": "/en/nutreval-test/",
    "/metabolomik/": "/en/metabolomics/",
    "/sibo-test/": "/en/sibo-test/",
    "/genova-hormontest/": "/en/genova-hormones/",
    "/organix/": "/en/organix/",
    "/fettsyror/": "/en/fatty-acids/",
    "/adrenal-stress/": "/en/adrenal-stress/",
    "/essential-ostrogen/": "/en/essential-estrogens/",
    "/menopaus-plus/": "/en/menopause-plus/",
    "/kvinnohalsa/": "/en/womens-health/",
    "/iv-terapi/": "/en/iv-therapy/",
    "/clinical-notes/": "/en/clinical-notes/",
    "/forskning.html": "/en/research/",
    "/global-constraint-rule/": "/en/global-constraint-rule/",
    "/longevitet-halsospann/": "/en/longevity-healthspan/",
    "/integritetspolicy/": "/en/privacy-policy/",
    "/symtom/": "/en/symptoms/",
    "/skrifter/": "/en/writings/",
    "/baby-balans/": "/en/baby-balans/",
}


def exists(href):
    p = href.split("#")[0].strip("/")
    return os.path.exists(os.path.join(ROOT, p, "index.html")) or \
        os.path.exists(os.path.join(ROOT, p))


def nav_spans(h):
    """(start, slut) för desktop- och mobilnavigation."""
    out = []
    d = re.search(r"<header\b.*?</header>", h, re.S)
    if d:
        out.append((d.start(), d.end()))
    i = h.find('<div class="mobile-nav"')
    if i != -1:
        m = re.search(r"</div>\s*(?=<(?!a\b)[a-zA-Z])", h[i:])
        if m:
            out.append((i, i + m.end()))
    return sorted(out, reverse=True)          # bakifrån så index håller


def process(path, is_en):
    h = open(path, encoding="utf-8").read()
    orig = h
    stats = {"död": 0, "läckage": 0}

    # Döda länkar rättas i HELA dokumentet — måladressen existerar inte
    # någonstans, så länken är trasig oavsett om den står i navigationen
    # eller i brödtexten (t.ex. relaterade-länkar längst ned på sidan).
    for bad, good in DEAD.items():
        n = h.count(f'href="{bad}"')
        if n:
            h = h.replace(f'href="{bad}"', f'href="{good}"')
            stats["död"] += n

    # Språkläckage rättas ENDAST i navigationen. Svenska länkar i brödtext
    # på engelska sidor kan vara avsiktliga hänvisningar och kräver
    # redaktionell bedömning, inte en sökning-och-ersättning.
    for start, end in nav_spans(h):
        region = h[start:end]

        if is_en:
            for sv, en in SV_TO_EN.items():
                if not exists(en):
                    continue
                n = region.count(f'href="{sv}"')
                if n:
                    region = region.replace(f'href="{sv}"', f'href="{en}"')
                    stats["läckage"] += n

        h = h[:start] + region + h[end:]

    if h != orig and not DRY:
        open(path, "w", encoding="utf-8").write(h)
    return (h != orig), stats


def main():
    tot = {"död": 0, "läckage": 0}
    files = 0
    for dp, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        for fn in fs:
            if fn != "index.html":
                continue
            p = os.path.join(dp, fn)
            if os.path.getsize(p) < 1000:
                continue
            rel = os.path.relpath(p, ROOT)
            is_en = rel.startswith(("en/", "en-"))
            did, st = process(p, is_en)
            if did:
                files += 1
                tot["död"] += st["död"]
                tot["läckage"] += st["läckage"]
                print(f"  ✓ {rel:48} döda={st['död']} läckage={st['läckage']}")
    print("\n" + ("TORRKÖRNING — inget skrivet" if DRY else "SKRIVET"))
    print(f"  {files} filer · {tot['död']} döda länkar · {tot['läckage']} språkläckage")


if __name__ == "__main__":
    main()
