# -*- coding: utf-8 -*-
"""
MediBalans · omskrivning av folat-avsnittet på /baby-balans/
=============================================================
Den kliniska ståndpunkten är oförändrad: 5-MTHF är rätt form för
MTHFR-bärare, och ingen bör dosera folat utan att känna sin genotyp.
Det som ändras är tre formuleringar som inte håller vid granskning, plus
två tillägg som Dr Mario efterfrågat.

ÄNDRAT
  1. "kan vara skadligt" -> knyts till HÖGA DOSER, vilket är vad
     evidensen faktiskt visar. 2025 års översikt handlar om excessive
     folic acid consumption, inte om 400 µg perikonceptionellt.
  2. "Det kan den inte" -> "30-40 % av normal kapacitet". TT-bärare
     omvandlar långsamt och ofullständigt; de har uppmätt cirka 16 %
     lägre folat i blod vid samma intag, inte frånvarande omvandling.
  3. Ny säkerhetsrad: sluta inte med folattillskott. Detta stänger den
     enda feltolkning som kan orsaka skada — att folat vore valfritt.
     Neuralröret sluts kring dag 28, ofta före känd graviditet.

TILLAGT
  4. Stark uppmaning: metyleringstest före konception, för båda parter.
  5. NIPT under graviditet — korrekt beskrivet som screening från
     vecka 10, inte diagnostik, och via mödravården eftersom MediBalans
     inte erbjuder det.

Kör:  python3 scripts/fix_folate_section.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "baby-balans", "index.html")

REPLACEMENTS = [
    # ---- 1. rubrik ----
    ('<h2 class="section-title">Folsyra är inte rätt för alla — och kan vara <em>skadligt</em></h2>',
     '<h2 class="section-title">Folsyra är fel form för minst var tredje kvinna — <em>testa innan du doserar</em></h2>'),

    # ---- 2. varningsblocket ----
    ('<p>Det är rådet nästan alla läkare ger. Det bygger på forskning som är korrekt i sin grundprincip — folat är kritiskt för neuraltubestängning och DNA-syntes. Men rådet förutsätter att kroppen kan omvandla syntetisk folsyra till den aktiva formen. <strong>Det kan den inte, vid MTHFR-variant.</strong></p>\n<p>Minst <strong>40% av befolkningen</strong> bär en eller flera MTHFR-varianter. Standardscreening testar inte detta. Resultatet är att miljontals gravida kvinnor tar ett tillskott som ger dem en falsk trygghet — och som i värsta fall förvärrar deras situation.</p>',

     '<p>Det är rådet nästan alla läkare ger, och grundprincipen är riktig: folat är kritiskt för neuralrörets slutning och för DNA-syntes. <strong>Folat ska du ta.</strong> Men rådet förutsätter något som inte gäller alla — att kroppen effektivt omvandlar syntetisk folsyra till den aktiva formen.</p>\n'
     '<p>Vid <strong>MTHFR C677T homozygot</strong> arbetar enzymet på 30–40 % av normal kapacitet. Omvandlingen sker, men långsamt och ofullständigt. Minst <strong>40 % av befolkningen</strong> bär en eller flera MTHFR-varianter, och standardscreening testar inte detta. Konsekvensen är inte att folat är fel — utan att <em>formen</em> och <em>dosen</em> sätts blint, och att ett normalt folatvärde i blod kan dölja otillräcklig tillgång inne i cellen.</p>'),

    # ---- 3. direkt svar ----
    ('<div class="direct-answer-label">Direkt svar — Är folsyra farligt vid MTHFR?</div>\n<p><strong>Syntetisk folsyra (B9) kräver MTHFR-enzymet för att omvandlas till 5-MTHF</strong> — den enda formen celler kan använda. Vid MTHFR C677T homozygot fungerar enzymet på 30–40% av normal kapacitet. Ometaboliserad folsyra (UMFA) ackumuleras då i blodet, kan blockera folatreceptorer och försämra cellernas förmåga att ta upp naturligt folat. Den kliniskt korrekta formen för MTHFR-bärare är aktivt <strong>methylfolat (5-MTHF)</strong>, doserat utifrån individuell MTHFR-genotyp och verifierad intracellulär folatstatus.</p>',

     '<div class="direct-answer-label">Direkt svar — Ska jag ta folsyra om jag har MTHFR-variant?</div>\n'
     '<p><strong>Ja — sluta aldrig med folattillskott. Men välj rätt form.</strong> Syntetisk folsyra (B9) kräver MTHFR-enzymet för att omvandlas till 5-MTHF, den form cellen faktiskt använder. Vid C677T homozygot arbetar enzymet på 30–40 % av normal kapacitet. Vid <em>höga</em> intag mättas omvandlingen och ometaboliserad folsyra (UMFA) ackumuleras i blodet — kopplat i litteraturen till maskerad B12-brist och ogynnsamma graviditetsutfall. '
     'Den kliniskt rimliga formen för MTHFR-bärare är aktivt <strong>methylfolat (5-MTHF)</strong>, doserat utifrån genotyp och verifierad intracellulär folatstatus.</p>\n'
     '<p style="margin-top:.7rem"><strong>Viktigt:</strong> folattillskott periekonceptionellt minskar risken för neuralrörsdefekter med omkring 70 %, och neuralröret sluts kring dag 28 — ofta innan graviditeten är känd. Är du osäker på din genotyp: fortsätt med folat och välj methylfolat. Diskutera formen med din barnmorska eller läkare. Sluta inte.</p>'),

    # ---- 4. jämförelsekortet: mjuka "falsk trygghet" ----
    ('<li>Ger falsk trygghet — ser ut som tillräckligt folat i blodprov</li>',
     '<li>Blodprov kan se normalt ut trots otillräcklig tillgång i cellen</li>'),
    ('<li>Ackumuleras som UMFA vid nedsatt MTHFR</li>',
     '<li>Ackumuleras som UMFA vid höga doser och nedsatt MTHFR</li>'),
]

# ---- 5. nya block som läggs in före </section> i folate-avsnittet ----
NEW_BLOCKS = """
<!-- TESTA FÖRST — stark uppmaning -->
<div class="warning-block reveal reveal-d2" style="margin-top:2rem">
<div class="warning-block-label">Vår tydliga rekommendation</div>
<h3>Testa metyleringen innan ni försöker bli gravida — båda två</h3>
<p>Folat, B12, cholin och betain går alla genom samma metyleringsmaskineri. Vilken form och vilken dos som är rätt för dig avgörs av din genotyp, inte av ett schablonråd på förpackningen. Det är en engångsmätning som gäller resten av livet, och den kostar en bråkdel av vad en utebliven graviditet gör.</p>
<p><strong>Testa båda parter.</strong> Spermiekvalitet och DNA-fragmentering påverkas av samma metyleringsvägar. Halva barnets genom kommer från fadern, och hans folatstatus är lika relevant som moderns — något som i praktiken aldrig undersöks.</p>
<p style="margin-top:.8rem"><a href="/methyldetox/" style="color:var(--blue-light);font-weight:600">MethylDetox — 38 gener, samtliga SNP:ar →</a></p>
</div>

<!-- NIPT -->
<div class="warning-block reveal reveal-d2" style="margin-top:1.4rem">
<div class="warning-block-label">Under graviditeten</div>
<h3>Gör även NIPT</h3>
<p>NIPT (non-invasivt prenatalt test) analyserar fritt foster-DNA i moderns blod från omkring graviditetsvecka 10 och screenar för de vanligaste kromosomavvikelserna — trisomi 21, 18 och 13. Det är ett blodprov utan missfallsrisk, till skillnad från fostervattenprov och moderkaksprov.</p>
<p>NIPT är ett <strong>screeningtest, inte ett diagnostiskt svar</strong>. Ett positivt fynd ska alltid bekräftas med moderkaksprov eller fostervattenprov innan några slutsatser dras. Testet ersätter inte heller den prekonceptionella kartläggningen — det mäter något helt annat, vid en helt annan tidpunkt.</p>
<p><strong>Vi erbjuder NIPT.</strong> Vår uppfattning är att alla som kan bör göra det, och fördelen med att göra det hos oss är att svaret läses tillsammans med er metyleringsprofil och övriga fynd i stället för som ett isolerat besked.</p>
<p style="margin-top:.8rem"><a href="/#booking" style="color:var(--blue-light);font-weight:600">Boka prekonceptions- eller graviditetsbesök →</a></p>
</div>
"""


def main():
    h = open(F, encoding="utf-8").read()
    orig = h
    done = 0
    for old, new in REPLACEMENTS:
        if old in h:
            h = h.replace(old, new, 1)
            done += 1
        else:
            print(f"  ! hittade inte: {old[:70]}…")

    # sätt in nya block sist i folate-sektionen
    i = h.find('id="folate"')
    j = h.find("</section>", i)
    if "Testa metyleringen innan" not in h:
        h = h[:j] + NEW_BLOCKS + h[j:]
        done += 1

    open(F, "w", encoding="utf-8").write(h)
    print(f"\n{done} ändringar skrivna. Storlek {len(orig):,} -> {len(h):,}")


if __name__ == "__main__":
    main()
