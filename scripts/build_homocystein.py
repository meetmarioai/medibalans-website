# -*- coding: utf-8 -*-
"""
MediBalans · klinisk notering: homocystein och en-kolsmetabolismen
===================================================================
Tes: en-kolsmetabolismen är ett system, inte ett stickprov. Ett
homocysteinvärde säger att systemet inte går ihop — det säger ingenting
om vilken av sex punkter som klämmer.

Två fynd som läsaren sannolikt inte känner till, och som bär artikeln:

  RIBOFLAVIN  C677T-enzymet är termolabilt därför att det lättare
              dissocierar från sin FAD-kofaktor. Riboflavin stabiliserar
              det. Riktade randomiserade studier från Ulster-gruppen
              (McNulty 2006; Horigan 2010; Wilson 2013, Hypertension;
              fyraårsuppföljning) visar effekt specifikt hos TT-genotyp.
              Detta är den bäst belagda genotypspecifika interventionen
              i hela fältet, och den nämns nästan aldrig.

  MTRR        MTR:s kob(I)alamin oxideras till kob(II)alamin och
              enzymet stannar. MTRR återmetylerar det reduktivt med SAM
              som metyldonator. Den homocysteinhöjande effekten av
              MTRR 66AA är OBEROENDE av serumfolat, B12 och B6 — alltså
              kan alla tre proverna vara normala medan cykeln ändå
              stannar. Det är det kliniska argumentet för 38 gener i
              stället för ett MTHFR-test.

Hållning kring de negativa studierna: samma disciplin som i
SIBO-noteringen. HOPE-2 och NORVIT plockas isär på design, inte
avfärdas — och artikeln säger uttryckligen att den avgörande studien
aldrig har gjorts.

Kör:  python3 scripts/build_homocystein.py
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_new_sections import page, hero, toc, band, faq_html, faq_schema, ROOT, BASE

URL = f"{BASE}/homocystein/"
ORG = {"@id": f"{BASE}/#organization"}
AUTHOR_ID = f"{BASE}/#mario-anthis"

SECTIONS = [
    ("referens", "Laboratoriets referensintervall är för tillåtande", [
        "De flesta svenska laboratorier rapporterar homocystein under omkring 15 µmol/L som normalt. Det intervallet är konstruerat för att fånga uppenbar patologi — inte för att beskriva optimal funktion.",
        "VITACOG-studien vid Oxford är den mest upplysande i sammanhanget. Deltagare med lindrig kognitiv svikt randomiserades till B-vitaminer eller placebo. Hjärnatrofin minskade med omkring 30 procent i behandlingsgruppen. Hos dem med homocystein över 13 µmol/L var atrofitakten 53 procent lägre, och i mediala temporalloben — den region som drabbas först vid Alzheimers sjukdom — var skillnaden nästan niofaldig. Effekten var koncentrerad till deltagare över medianen på 11,3 µmol/L.",
        "Med andra ord: värden som laboratoriet rapporterar som normala sammanfaller med mätbart accelererad hjärnatrofi. Ett svar på 14 är inte ett friskbesked. Det är ett värde där en randomiserad studie har visat att intervention gör skillnad.",
        "Vi arbetar kliniskt mot 6–9 µmol/L. Det är ett funktionellt mål, inte ett gränsvärde hämtat ur en utfallsstudie — och den skillnaden är viktig nog att stå utskriven.",
    ]),
    ("systemet", "Ett värde, sex punkter", [
        "Homocystein är en korsning. Det bildas när metionin ger ifrån sig sin metylgrupp, och det försvinner därifrån längs tre vägar. Varje väg har sitt eget enzym och sin egen kofaktor. Ett förhöjt värde betyder att flödet inte går ihop — men det pekar inte ut var det klämmer.",
        "<strong>MTHFR</strong> producerar 5-MTHF, den aktiva folatformen. Enzymet kräver FAD, alltså riboflavin (B2).",
        "<strong>MTR</strong> (metioninsyntas) återmetylerar homocystein till metionin. Enzymet kräver B12 som metylbärare och 5-MTHF som metyldonator.",
        "<strong>MTRR</strong> återställer MTR när dess kobalamin har oxiderats. Kräver SAM och reduktionskapacitet.",
        "<strong>BHMT</strong> är den folatoberoende genvägen: betain (TMG) donerar en metylgrupp direkt. Cholin är förstadiet.",
        "<strong>CBS</strong> inleder avloppet — transsulfureringen som för homocystein vidare mot cystein och glutation. Kräver B6 i aktiv form.",
        "<strong>AHCY</strong> ligger uppströms om alltihop och behandlas nedan för sig. Det är enzymet som över huvud taget producerar homocystein, och det steget avgör mer än de övriga tillsammans.",
        "Sex punkter, ett mätvärde. Det är därför ett homocysteinvärde ensamt är ett larm och inte en diagnos, och därför att behandla det med en enda substans är gissning satt i system.",
    ]),
    ("ahcy", "AHCY — steget uppströms som avgör vad siffran betyder", [
        "Homocystein uppstår inte ur ingenting. SAM donerar sin metylgrupp och blir SAH — S-adenosylhomocystein. Först därefter hydrolyseras SAH till homocystein och adenosin, och det enzym som gör det är AHCY (S-adenosylhomocysteinhydrolas).",
        "Två egenskaper hos det steget förändrar hur hela mätvärdet ska läsas.",
        "<strong>Reaktionen är reversibel, och jämvikten gynnar SAH-bildning.</strong> Nettoflödet mot homocystein sker bara så länge båda produkterna — homocystein och adenosin — avlägsnas kontinuerligt. Ansamlas de går reaktionen baklänges och SAH byggs upp. Det gör AHCY-steget beroende inte bara av sitt eget enzym utan av att avloppen nedströms fungerar.",
        "<strong>SAH är en potent hämmare av i stort sett alla SAM-beroende metyltransferaser.</strong> Ansamlat SAH bromsar alltså metylering brett — DNA, histoner, neurotransmittorer, fosfolipider — oavsett hur mycket SAM som finns tillgängligt.",
        "Konsekvensen är obekväm men viktig: det egentliga metyleringsindexet är <strong>kvoten SAM:SAH</strong>, inte homocystein. Homocystein är en nedströms skugga av den kvoten. En patient kan ha ett prydligt homocysteinvärde och samtidigt ha förhöjt SAH och hämmad metyleringskapacitet — och en patient med förhöjt homocystein kan ha det just därför att AHCY-steget arbetar bra och avloppet är trångt längre ned.",
        "Det är den skarpaste illustrationen av tesen. Ett stickprov på en metabolit i mitten av en cykel kan inte i sig avgöra åt vilket håll cykeln lutar.",
    ]),
    ("riboflavin", "Riboflavin — det bäst belagda och minst använda", [
        "Om en enda punkt i den här texten är värd att ta med sig är det den här.",
        "C677T-varianten gör inte enzymet obrukbart. Den gör det <em>termolabilt</em> — enzymet har ökad benägenhet att dissociera från sin FAD-kofaktor och tappar därmed aktivitet. Riboflavin stabiliserar bindningen.",
        "Detta är inte enbart mekanistiskt resonemang. Forskargruppen i Ulster har genomfört en serie riktade randomiserade studier: riboflavin sänker homocystein specifikt hos personer med TT-genotyp (McNulty, 2006), sänker blodtrycket hos TT-bärare med kardiovaskulär sjukdom (Horigan, 2010), och sänker blodtrycket hos behandlade hypertoniker med TT-genotyp i en riktad randomiserad studie publicerad i <em>Hypertension</em> (Wilson, 2013), med bibehållen effekt vid fyraårsuppföljning.",
        "Genotypspecifikt, randomiserat, replikerat. Samtidigt handlar praktiskt taget hela den svenska MTHFR-diskussionen om methylfolat, och riboflavin nämns inte. Det är den mest förbisedda interventionen i fältet.",
    ]),
    ("mtrr", "MTRR — varför normala B12- och folatvärden inte räcker", [
        "MTR bär sin metylgrupp på kobalt i kobalamin. Med jämna mellanrum oxideras kob(I)alamin till kob(II)alamin, och enzymet stannar. Det är inte ett fel utan ett normalt slitage i reaktionscykeln.",
        "För att starta om krävs MTRR — metioninsyntasreduktas — som reduktivt återmetylerar kofaktorn med SAM som metyldonator. Utan fungerande MTRR står MTR stilla oavsett hur mycket B12 eller folat som finns tillgängligt.",
        "Det avgörande fyndet: den homocysteinhöjande effekten av MTRR 66AA-genotypen är <strong>oberoende av serumfolat, B12 och B6</strong>. En patient kan alltså ha lärobokperfekta värden på alla tre och ändå ha en cykel som gång på gång stannar.",
        "Detta är den kliniska anledningen till att ett isolerat MTHFR-test är otillräckligt. MTHFR är en av flera punkter där systemet kan fallera, och den enda av dem som allmänheten känner till.",
    ]),
    ("nad", "NAD⁺-tillskott — metyldränaget som sällan nämns", [
        "Här finns en iatrogen orsak till stigande homocystein som nästan aldrig kommer upp i samtalet, och den är värd ett eget avsnitt eftersom den drabbar just den grupp som är mest hälsomedveten.",
        "Nikotinamid — slutprodukten när NAD⁺-prekursorer som NMN, NR och niacinamid omsätts — utsöndras inte som den är. Den måste metyleras först. Enzymet NNMT tar en metylgrupp från SAM och bildar 1-metylnikotinamid, och kvar blir SAH. Varje molekyl nikotinamid som ska ut ur kroppen kostar alltså en metylgrupp. Dosen avgör notan.",
        "Effekten är dokumenterad hos människa. I en farmakokinetisk studie gavs 100 mg nikotinamid oralt — en blygsam dos jämfört med de 300–900 mg NMN som är vanligt i longevity-sammanhang. Fem timmar senare sågs stigande plasmahomocystein, utarmning av den labila metylpoolen och mätbart nedsatt COMT-aktivitet, avläst som försämrad omvandling av adrenalin till metanefrin.",
        "I djurmodell är bilden tydligare. Nikotinamidtillskott hos råtta gav betainutarmning, dosberoende sänkning av global DNA-metylering i lever mätt med LINE-1, och metyleringsförändringar vid promotorerna för NNMT, DNMT1, BHMT, metioninsyntas och CBS — alltså vid generna för själva metioninscykeln. I möss med överuttryckt NNMT kollapsade kvoten SAM:SAH under 1,0, vilket är en nivå där i praktiken alla metyltransferasreaktioner hämmas, samtidigt som BHMT1-uttrycket sjönk.",
        "Den sista detaljen är den obehagliga. Belastningen slår ut den kompensationsmekanism som skulle ha hanterat den: BHMT-grenen, kroppens folatoberoende väg att återmetylera homocystein, dämpas av samma stress som gör den nödvändig. Det är ett självförstärkande förlopp snarare än en jämvikt som söker sig tillbaka.",
        "Att bristen är korrigerbar visades i en tillväxtstudie: hämmad tillväxt hos djurungar vid hög nikotinamiddos förhindrades av metionintillskott, alltså genom att fylla på den SAM-pool som dränerats.",
    ]),
    ("nad-evidens", "Vad de kliniska studierna på NAD⁺ faktiskt visar", [
        "Underlaget hos människa ska återges som det är, inklusive det som talar emot.",
        "NR-SAFE, en randomiserad dubbelblind placebokontrollerad studie, gav nikotinamidribosid 3 000 mg dagligen i fyra veckor. Serumhomocystein steg statistiskt säkerställt med 1,66 µmol/L (p = 5,4 × 10⁻⁴) och betain sjönk jämfört med placebo. <strong>Men</strong> — och detta ska stå med — homocystein i helblod och SAM/SAH i helblod var oförändrade, och författarna drog slutsatsen att metyldonatorpoolen i huvudsak var intakt vid den dosen och den tidsrymden.",
        "En tidigare säkerhetsstudie på 140 överviktiga vuxna fann ingen signifikant homocysteinstegring vid 100–1 000 mg NR dagligen under åtta veckor. Även den studien mätte däremot homocystein som specifik säkerhetsvariabel, och dess författare hänvisade uttryckligen till att 300 mg nikotinamid respektive nikotinsyra är känt för att höja plasmahomocystein.",
        "En omfattande humanstudie publicerad 2025 bekräftade därefter i flera oberoende kohorter att långvarigt intag av NAD⁺-prekursorer — både NMN och NR — utarmar metyldonatorer och höjer homocystein.",
        "Sammantaget: effekten är dos- och tidsberoende, den syns tidigare i serum än i helblod, och den modifieras av genotyp och av hur väl kosten försörjer metylgrupper från början. Kortvariga studier på måttliga doser hos välnärda försökspersoner säger begränsat om vad flera års dagligt intag gör hos en åldrande population där MTHFR-varianter är vanliga.",
        "Den praktiska slutsatsen är inte att avstå från NAD⁺-prekursorer. Den är att de utgör en metylbelastning som ska balanseras och följas — mät homocystein före start och under pågående intag, och komplettera med metyleringsstöd i stället för att hoppas att systemet bär.",
    ]),
    ("methylfolat", "Varför “ta bara methylfolat” ofta inte fungerar", [
        "Methylfolat åtgärdar MTHFR-steget. Om flaskhalsen sitter där är effekten ofta påtaglig.",
        "Sitter den någon annanstans händer däremot lite. Är MTRR nedsatt saknas inte metyldonatorer utan reduktionskapacitet. Är B12 otillräckligt eller i fel form saknas bäraren. Är B6-status låg är avloppet till transsulfurering trångt, och homocystein stannar kvar oavsett hur mycket som återmetyleras. Är riboflavin lågt hjälper det föga att kringgå ett enzym som hade kunnat stabiliseras.",
        "Och hos den som inte bär MTHFR-variant finns ingen flaskhals att kringgå. Höga doser aktivt folat kan då driva metyleringen fortare än nedströms kapacitet medger och öka uttaget av metylgrupper, metionin, B12, B6 och cholin.",
        "Betain (TMG) förtjänar en särskild anmärkning. Det är en effektiv folatoberoende väg och kliniskt användbart när BHMT-grenen är den framkomliga. I studier har dock höga doser visat sig höja LDL och totalkolesterol. Det är ett argument för dosering under uppföljning, inte för att avstå — men det hör till bilden.",
    ]),
    ("studierna", "De negativa studierna — vad de faktiskt prövade", [
        "Invändningen kommer alltid, och den ska besvaras rakt: de stora interventionsstudierna sänkte homocystein utan att minska kardiovaskulära händelser. HOPE-2 gav 2,5 mg folsyra, 50 mg B6 och 1 mg B12 under fem år till högriskpatienter — ingen effekt på vaskulära händelser trots sänkt homocystein. NORVIT randomiserade patienter inom sju dagar efter hjärtinfarkt, såg ingen nytta och rapporterade dessutom en signal mot ökad händelsefrekvens i kombinationsarmen.",
        "Den slutsats som brukar dras är att homocystein är en markör snarare än en orsak. För den frågan studierna ställde är det en rimlig slutsats.",
        "Men frågan de ställde var smalare än den som citeras. Fyra invändningar, var och en tillräcklig för att dra utfallet mot noll:",
        "<strong>Populationen.</strong> Patienter med etablerad kranskärlssjukdom, i NORVIT inom en vecka efter infarkt. Placken finns redan. Det prövar reversering av manifest sjukdom, inte prevention över decennier.",
        "<strong>Inklusionen.</strong> Förhöjt homocystein krävdes inte för att delta. Att behandla personer som inte har det tillstånd man vill påverka kan inte visa nytta — det späder effekten. VITACOG hittade sin signal just genom att titta över medianen, och effekten skalade med utgångsvärdet.",
        "<strong>Interventionen.</strong> Syntetisk folsyra i hög dos, utan riboflavin, utan betain, utan stratifiering på genotyp. Hos bärare genererar det ometaboliserad folsyra. En studie som möjligen skadade en genotypisk undergrupp samtidigt som den behandlade ostratifierade patienter är inget rent prov på hypotesen — och NORVIT:s skadesignal blir då begriplig snarare än gåtfull.",
        "<strong>Utfallsmåttet.</strong> Hårda kardiovaskulära händelser över några år. VITACOG valde hjärnatrofi — ett känsligare och mer närliggande mått — och fann stor effekt. Valet av utfall avgjorde i hög grad svaret.",
        "Studierna prövade alltså om tillägg av högdos syntetisk folsyra till patienter med etablerad kärlsjukdom, oavsett utgångsvärde och genotyp, minskar återinsjuknande. Svaret är nej. Det är inte samma fråga som om livslång metyleringskapacitet har betydelse för kärl- och hjärnåldrande.",
    ]),
    ("granser", "Vad vi inte kan påstå", [
        "Den avgörande studien har inte gjorts. Det finns ingen utfallsstudie som visar att en frisk trettiofemåring som sänker sitt homocystein från 10 till 7 med methylfolat, riboflavin och betain lever längre eller behåller sin kognition bättre.",
        "Vårt mål på 6–9 µmol/L är därför ett funktionellt riktmärke grundat i mekanism, i VITACOG:s doseffekt och i klinisk erfarenhet — inte ett gränsvärde validerat mot hårda utfall. Den som påstår annat övertolkar underlaget.",
        "Lågt är inte heller automatiskt bättre. Mycket låga värden kan spegla ett kraftigt uttag mot transsulfurering eller ett förändrat B6-beroende, och bör tolkas i sitt sammanhang snarare än firas.",
        "Det som däremot är svårt att komma ifrån: homocystein är billigt, allmänt tillgängligt, påverkbart, och det referensintervall som används i dag rapporterar värden som normala vid vilka en randomiserad studie har visat accelererad hjärnatrofi.",
    ]),
]

FAQ = [
    ("Vad ska homocystein ligga på?",
     "De flesta laboratorier rapporterar värden under omkring 15 µmol/L som normala, men det intervallet är byggt för att fånga uppenbar patologi. VITACOG-studien visade accelererad hjärnatrofi vid värden över 11 µmol/L och störst behandlingseffekt över 13. Vi arbetar kliniskt mot 6–9 µmol/L. Det är ett funktionellt riktmärke grundat i mekanism och studieeffekt, inte ett gränsvärde validerat mot hårda utfall."),
    ("Räcker det att ta methylfolat om homocystein är högt?",
     "Sällan. Homocystein bildas och omsätts via sex punkter som var och en kan vara flaskhalsen: AHCY som hydrolyserar SAH till homocystein, MTHFR som kräver riboflavin, MTR som kräver B12, MTRR som återställer oxiderat kobalamin med SAM, BHMT som går på betain och cholin, samt CBS som för homocystein vidare mot glutation och kräver B6. Methylfolat åtgärdar enbart MTHFR-steget. Sitter problemet någon annanstans händer lite."),
    ("Varför är riboflavin (B2) viktigt vid MTHFR-variant?",
     "MTHFR-enzymet kräver FAD, som bildas av riboflavin. C677T-varianten gör enzymet termolabilt genom ökad benägenhet att dissociera från FAD. Riboflavin stabiliserar bindningen. Riktade randomiserade studier har visat att riboflavin sänker homocystein och blodtryck specifikt hos personer med TT-genotyp, med effekt kvar vid fyraårsuppföljning. Det är den bäst belagda genotypspecifika interventionen i fältet och används ändå sällan."),
    ("Kan homocystein vara högt trots normala värden på B12 och folat?",
     "Ja. Metioninsyntas stannar när dess kobalamin oxideras, och MTRR krävs för att återställa det. Den homocysteinhöjande effekten av MTRR 66AA-genotypen är oberoende av serumfolat, B12 och B6 — alla tre proverna kan alltså vara normala medan cykeln ändå stannar. Det är den kliniska anledningen till att ett isolerat MTHFR-test är otillräckligt."),
    ("Kan NMN eller NR höja homocystein?",
     "Ja, och mekanismen är väl beskriven. Nikotinamid måste metyleras av enzymet NNMT för att kunna utsöndras. Varje molekyl kostar en metylgrupp från SAM och lämnar SAH efter sig, så belastningen är dosberoende. Hos människa har 100 mg oralt nikotinamid gett stigande homocystein och nedsatt COMT-aktivitet inom fem timmar, och i en randomiserad studie med 3 000 mg nikotinamidribosid dagligen steg serumhomocystein med 1,66 µmol/L samtidigt som betain sjönk. En humanstudie från 2025 bekräftade utarmning av metyldonatorer vid långvarigt intag av både NMN och NR. Slutsatsen är inte att avstå, utan att mäta homocystein före och under intaget och balansera metylbelastningen."),
    ("Betyder de negativa hjärtstudierna att homocystein inte spelar roll?",
     "De visar att tillägg av högdos syntetisk folsyra till patienter med etablerad kranskärlssjukdom, utan krav på förhöjt utgångsvärde och utan genotypstratifiering, inte minskar återinsjuknande. Det är en smalare fråga än den som brukar citeras. Populationen hade redan manifest sjukdom, förhöjt homocystein krävdes inte för deltagande, interventionen saknade riboflavin och betain, och utfallsmåttet var hårda händelser över några år. Studierna motbevisar inte hypotesen — men den avgörande studien har heller inte gjorts."),
    ("Kan metyleringen vara hämmad trots normalt homocystein?",
     "Ja. SAM donerar sin metylgrupp och blir SAH, som därefter hydrolyseras till homocystein och adenosin av enzymet AHCY. Den reaktionen är reversibel och jämvikten gynnar SAH-bildning, så nettoflödet kräver att både homocystein och adenosin avlägsnas kontinuerligt. SAH är dessutom en potent hämmare av i stort sett alla SAM-beroende metyltransferaser. Det egentliga metyleringsindexet är därför kvoten SAM:SAH — homocystein är en nedströms skugga av den. Ett normalt homocysteinvärde utesluter inte förhöjt SAH och hämmad metylering."),
    ("Är lågt homocystein alltid bra?",
     "Nej. Mycket låga värden kan spegla ett kraftigt uttag mot transsulfurering eller ett förändrat B6-beroende. Värdet tolkas i sitt sammanhang tillsammans med B12, folat, B6, riboflavinstatus och genotyp."),
]

SOURCES = [
    "Smith AD, Smith SM, de Jager CA, et al. Homocysteine-lowering by B vitamins slows the rate of accelerated brain atrophy in mild cognitive impairment: a randomized controlled trial (VITACOG). <em>PLOS ONE</em> 2010.",
    "McNulty H, Dowey LRC, Strain JJ, et al. Riboflavin lowers homocysteine in individuals homozygous for the MTHFR 677C→T polymorphism. <em>Circulation</em> 2006.",
    "Horigan G, McNulty H, Ward M, et al. Riboflavin lowers blood pressure in cardiovascular disease patients homozygous for the 677C→T polymorphism in MTHFR. <em>Journal of Hypertension</em> 2010.",
    "Wilson CP, Ward M, McNulty H, et al. Blood pressure in treated hypertensive individuals with the MTHFR 677TT genotype is responsive to intervention with riboflavin. <em>Hypertension</em> 2013, samt fyraårsuppföljning.",
    "Gaughan DJ, Kluijtmans LAJ, Barbaux S, et al. The methionine synthase reductase (MTRR) A66G polymorphism is a novel genetic determinant of plasma homocysteine concentrations. <em>Atherosclerosis</em> 2001.",
    "Sun WP, et al. Effect of nicotinamide on plasma homocysteine and methyl pool in humans. <em>Hypertension Research</em> 2012.",
    "Shi H, et al. Nicotinamide supplementation and hepatic DNA methylation in developing rats. <em>British Journal of Nutrition</em> 2013.",
    "Komatsu M, et al. NNMT overexpression, SAM:SAH ratio and BHMT1 suppression. <em>Scientific Reports</em> 2018.",
    "Pissios P. Nicotinamide N-methyltransferase: more than a vitamin B3 clearance enzyme. <em>Nutrients</em> 2017.",
    "Berven H, et al. NR-SAFE: randomised, double-blind, placebo-controlled trial of nicotinamide riboside. <em>Nature Communications</em> 2023.",
    "Conze D, Brenner C, Kruger CL. Safety and metabolism of long-term nicotinamide riboside supplementation. <em>Scientific Reports</em> 2019.",
    "Elhassan YS, et al. Sustained NAD+ precursor supplementation and methyl donor status in humans. <em>Cell Metabolism</em> 2025.",
    "HOPE-2 Investigators. Homocysteine lowering with folic acid and B vitamins in vascular disease. <em>NEJM</em> 2006.",
    "Bønaa KH, Njølstad I, Ueland PM, et al. Homocysteine lowering and cardiovascular events after acute myocardial infarction (NORVIT). <em>NEJM</em> 2006.",
    "Om AHCY och SAM:SAH-kvoten som metyleringsindex: S-adenosylhomocysteinhydrolas katalyserar ett reversibelt steg vars jämvikt gynnar SAH-bildning; SAH hämmar SAM-beroende metyltransferaser.",
]


def build():
    anchors = [(a, t.split("—")[0].strip()) for a, t, _ in SECTIONS] + [("faq", "Vanliga frågor")]
    body = "".join(
        f'<section id="{a}"><h2>{t}</h2>' + "".join(f"<p>{p}</p>" for p in ps) + "</section>"
        for a, t, ps in SECTIONS)
    srcs = "".join(f"<li>{s}</li>" for s in SOURCES)

    title = "Vad ska homocystein ligga på? En-kolsmetabolismen är ett system, inte ett stickprov | MediBalans"
    desc = ("Laboratoriet rapporterar under 15 µmol/L som normalt, men hjärnatrofin accelererar redan över 11. "
            "Homocystein omsätts via fem punkter — MTHFR, MTR, MTRR, BHMT och CBS — med riboflavin, B12, SAM, "
            "betain och B6 som kofaktorer. Därför räcker sällan methylfolat ensamt.")

    schema = [
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@graph": [
                {"@type": "MedicalWebPage", "@id": URL + "#page", "url": URL, "name": title,
                 "inLanguage": "sv-SE", "datePublished": "2026-07-29", "dateModified": "2026-07-29",
                 "audience": {"@type": "Patient"}, "author": {"@id": AUTHOR_ID},
                 "provider": ORG, "publisher": ORG,
                 "about": {"@type": "MedicalTest", "name": "Homocystein och metyleringskapacitet"}}]},
            ensure_ascii=False) + "</script>",
        faq_schema(URL, FAQ),
    ]

    content = f"""
{hero("Klinisk notering · Metylering", "Homocystein ", "Ett system, inte ett stickprov.",
      "Ett homocysteinvärde säger att en-kolsmetabolismen inte går ihop. Det säger ingenting om vilken av fem "
      "punkter som klämmer — och det är därför behandling med en enda substans så ofta inte biter.",
      '<a class="btn-p" href="/#booking">Boka konsultation</a>'
      '<a class="btn-s" href="/methyldetox/">MethylDetox — 38 gener</a>',
      "Klinisk notering. Funktionella riktmärken anges som sådana, inte som validerade gränsvärden.",
      [("6–9", "µmol/L, vårt mål"), ("15", "Laboratoriets gräns"),
       ("6", "Punkter i systemet"), ("38", "Gener i panelen")])}
{toc(anchors)}
<div class="container sec-body">
<section><p class="lead-p"><strong>Kort svar:</strong> laboratoriets referensintervall är för tillåtande. Hjärnatrofi accelererar redan vid värden som rapporteras som normala. Vi arbetar mot 6–9 µmol/L. Men det viktigare svaret är att siffran i sig inte talar om vad som ska åtgärdas — homocystein bildas och omsätts via sex punkter med var sin kofaktor, och behandlingen avgörs av vilken av dem som är flaskhalsen.</p></section>
{body}
<section id="faq"><h2>Vanliga <em>frågor</em></h2>{faq_html(FAQ)}</section>
<section id="kallor"><h2>Källor</h2><ol class="src">{srcs}</ol>
<p style="margin-top:1.5rem"><a href="/methyldetox/">MethylDetox — 38 gener, samtliga SNP:ar →</a> · <a href="/baby-balans/">Baby Balans — före graviditet</a> · <a href="/cma/">CMA — intracellulär näringsstatus</a></p></section>
</div>
{band("Mät hela systemet,", "inte en punkt",
      "Ett homocysteinvärde är utgångspunkten, inte svaret. Vilken spak som klämmer avgörs av genotyp och "
      "intracellulär status — och det avgör i sin tur vilken form och vilken dos som är rätt för dig.")}
"""
    extra = "\n.src{font-size:.87rem;color:var(--text-mid)}.src li{margin-bottom:.6rem}"
    return page(title, desc, URL, schema, content).replace("</style>", extra + "\n</style>", 1)


if __name__ == "__main__":
    p = os.path.join(ROOT, "homocystein", "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(build())
    print("   homocystein/index.html skriven")
