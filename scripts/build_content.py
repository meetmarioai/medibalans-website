# -*- coding: utf-8 -*-
"""
MediBalans · innehåll för /symtom/ och /skrifter/
Kör från repo-roten:  python3 scripts/build_content.py
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_new_sections import (ROOT, BASE, page, hero, toc, band,
                                faq_html, faq_schema)

ORG = {"@id": f"{BASE}/#organization"}
AUTHOR_ID = f"{BASE}/#mario-anthis"
AUTHOR_NODE = {
    "@type": "Physician", "@id": AUTHOR_ID, "name": "Mario Anthis",
    "givenName": "Mario", "familyName": "Anthis",
    "jobTitle": "Grundare & Medicinsk chef",
    "worksFor": ORG, "medicalSpecialty": "PrimaryCare",
    "url": f"{BASE}/skrifter/",
}

# panelpriser hämtade ur befintlig pixel-map (PRODUCTS) — inga påhittade priser
PANEL = {
    "gi-effects-test": ("GI Effects®", "8 500 kr"),
    "nutreval-sverige": ("NutrEval® FMV", "12 200 kr"),
    "metabolomik": ("Metabolomix+", "8 100 kr"),
    "sibo-test": ("SIBO-andningstest", "3 700 kr"),
    "kvinnohalsa": ("Women's Health+", "6 200 kr"),
    "organix": ("Organix®", "5 600 kr"),
    "fettsyror": ("Fettsyreanalys", "3 900 kr"),
    "adrenal-stress": ("Adrenocortex Stress Profile", "2 100 kr"),
    "essential-ostrogen": ("Essential Estrogens", None),
    "menopaus-plus": ("Menopause Plus", None),
    "alcat": ("ALCAT immunreaktivitet", None),
}


def pcard(slug, desc):
    name, pris = PANEL[slug]
    p = f'<div class="p">{pris}</div>' if pris else '<div class="p">Pris vid konsultation</div>'
    return (f'<a class="mb-card" href="/{slug}/"><span class="k">Analys</span>'
            f'<div class="t">{name}</div><p class="d">{desc}</p>{p}</a>')


def ncard(title, href, desc="Fördjupning — evidensläge och tolkning."):
    return (f'<a class="mb-card" href="{href}"><span class="k">Klinisk notering</span>'
            f'<div class="t">{title}</div><p class="d">{desc}</p></a>')


# ═══════════════════════════════════════════════════ SYMTOMGUIDER
GUIDES = [
    dict(
        slug="uppblast-mage",
        kicker="Symtomguide · Mage &amp; tarm",
        title="Uppblåst mage hela tiden — orsaker och vad som går att mäta | MediBalans",
        desc="Uppblåst mage varje dag har sällan en enda orsak. De vanligaste förklaringarna, när du ska söka vård, och vilka orsaker som går att mäta objektivt.",
        h1="Uppblåst mage hela tiden — ", h1em="vad det kan bero på",
        lead="Att vara uppblåst efter en stor måltid är normalt. Att vara uppblåst varje dag, oavsett vad du äter, är det inte. Skillnaden är inte hur mycket det svullnar utan hur förutsägbart det är.",
        svar="Kort svar: kronisk uppblåsthet beror oftast på en av fyra saker — ofullständig nedbrytning av maten, bakteriell jäsning på fel ställe i tarmen, immunreaktivitet mot vissa födoämnen, eller rubbad tarmmotorik. De ger likartade symtom men kräver olika åtgärder, vilket är skälet till att generella kostråd så ofta inte hjälper.",
        orsaker=[
            ("Ofullständig nedbrytning av maten", "Om bukspottkörteln producerar för lite enzymer, eller om magsyran är otillräcklig, når ofullständigt nedbruten mat längre ned i tarmen än den ska. Där jäser den. Typiskt mönster: uppblåsthet oavsett vad du äter, gaser med kraftig lukt, avföring som är lös eller fettglänsande."),
            ("Bakteriell jäsning på fel ställe", "Bakterier hör hemma i tjocktarmen. Hamnar de i tunntarmen jäser de maten innan den hunnit tas upp. Typiskt mönster: svullnad inom 30–90 minuter efter måltid, ofta värre av fiberrik eller sockerhaltig mat — alltså tvärtemot vad allmänna kostråd brukar rekommendera."),
            ("Immunreaktivitet mot födoämnen", "Fördröjda immunreaktioner mot livsmedel kan driva låggradig inflammation i tarmslemhinnan. Eftersom reaktionen kommer timmar till dygn efter måltiden är den svår att koppla till rätt födoämne på egen hand."),
            ("Rubbad tarmmotorik", "Går tarmens vågrörelser för långsamt stannar innehållet kvar och jäser. Vanligt vid förstoppningsdominerad bild och kan förvärras av stress, sköldkörtelpåverkan och vissa läkemedel."),
            ("Hormonella och cykelrelaterade orsaker", "Många kvinnor har svullnad som följer menstruationscykeln. Är uppblåstheten cyklisk snarare än daglig ligger förklaringen ofta i hormonell vätskereglering, inte i tarmen."),
        ],
        roda=["Blod i avföringen eller svart avföring", "Ofrivillig viktnedgång", "Blodbrist (anemi)",
              "Feber, nattliga svettningar eller symtom som väcker dig",
              "Svullnad som är ihållande och inte varierar över dagen",
              "Nytillkomna besvär efter 50 års ålder",
              "Ärftlighet för tarmcancer, celiaki eller inflammatorisk tarmsjukdom"],
        matbart=[("Ofullständig nedbrytning", "Pankreaselastas-1, fekalt fett, muskelfibrer", "gi-effects-test"),
                 ("Bakteriell jäsning i tunntarmen", "Väte- och metangas i utandningsluft över tid", "sibo-test"),
                 ("Tarmflorans sammansättning", "Mikrobiom via PCR, kortkedjiga fettsyror", "gi-effects-test"),
                 ("Inflammation i slemhinnan", "Kalprotektin, EPX, sekretoriskt IgA", "gi-effects-test"),
                 ("Cyklisk, hormonell svullnad", "Könshormoner och metaboliter över tid", "kvinnohalsa")],
        sjalv=[("Börja med vårdcentralen om du inte redan gjort det", "Fekalt kalprotektin och blodstatus är kostnadsfria, snabba och utesluter det allvarliga. All vidare utredning blir mer meningsfull när det är gjort."),
               ("För dagbok i två veckor — men på rätt sätt", "Notera tidpunkt för måltid och tidpunkt för svullnad, inte bara vad du åt. Tidsfördröjningen är ofta mer informativ än innehållet."),
               ("Var försiktig med att eliminera på egen hand", "Långvariga självpåtagna elimineringsdieter smalnar av kosten, försämrar tarmfloran och gör senare utredning svårare att tolka."),
               ("Notera om det följer cykeln", "Är svullnaden förutsägbart värre vissa dagar i månaden är det en helt annan utredning än daglig uppblåsthet.")],
        faq=[("Varför är jag uppblåst hela tiden trots att jag äter nyttigt?",
              "Nyttig mat är inte samma sak som lättsmält mat. Fiberrika grönsaker, baljväxter och fullkorn jäser kraftigt om de når bakterier på fel ställe i tarmen eller om nedbrytningen är ofullständig. Problemet är inte maten i sig utan var och hur den bryts ned."),
             ("Mina prover var normala — varför är jag fortfarande uppblåst?",
              "Vårdcentralens prover är byggda för att upptäcka eller utesluta inflammatorisk tarmsjukdom och blödning. De mäter inte matsmältning, bukspottkörtelns enzymproduktion, tarmflorans sammansättning eller dess metabola produktion. Normala prover utesluter sjukdom — inte funktionsstörning."),
             ("Går det att mäta vad som orsakar uppblåstheten?",
              "Flera av orsakerna går att mäta objektivt. Enzymproduktion mäts via pankreaselastas-1 i avföring, bakteriell jäsning i tunntarmen via väte- och metangasandningstest, och tarmflorans sammansättning via ett utökat avföringsprov. Vilken mätning som är motiverad avgörs av symtommönstret."),
             ("Vad kostar en utredning av uppblåst mage?",
              "GI Effects Comprehensive kostar 8 500 kr och SIBO-andningstest 3 700 kr via MediBalans, inklusive kit, analys hos Genova Diagnostics och klinisk tolkning av legitimerad läkare. Vilken analys som är motiverad avgörs i den inledande konsultationen.")],
        rel=[("gi-effects-test", "Utökat avföringsprov: matsmältning, mikrobiom, inflammation och metabol produktion."),
             ("sibo-test", "Väte- och metangasandningstest för bakteriell överväxt i tunntarmen.")],
        noter=[("Normalt kalprotektin men kvarstående besvär", "/clinical-notes/"),
               ("Är SIBO-andningstest tillförlitligt?", "/clinical-notes/")],
    ),
    dict(
        slug="trott-hela-tiden",
        kicker="Symtomguide · Energi &amp; trötthet",
        title="Trött hela tiden trots att du sover — vad tröttheten kan bero på | MediBalans",
        desc="Trötthet trots normala blodprover är vanligt och har oftast en mätbar förklaring. Vanliga orsaker, när du ska söka vård, och vad som går att mäta bortom rutinproverna.",
        h1="Trött hela tiden trots att du sover — ", h1em="och proverna är normala",
        lead="Den vanligaste meningen vi hör är att allt såg bra ut på proverna. Det är oftast sant — och samtidigt otillräckligt. Rutinprover är byggda för att upptäcka sjukdom, inte för att förklara varför energiproduktionen inte fungerar.",
        svar="Kort svar: trötthet med normala rutinprover beror sällan på en enda sak. De vanligaste förklaringarna är otillräckliga kofaktorer för cellens energiproduktion, rubbad dygnsrytm i stressystemet, låggradig inflammation, sköldkörtelpåverkan i gränslandet, eller sömn som är tillräckligt lång men inte tillräckligt återhämtande.",
        orsaker=[
            ("Cellens energiproduktion saknar kofaktorer", "Mitokondrierna behöver B-vitaminer, magnesium, järn, CoQ10 och karnitin för att omvandla mat till energi. En normal nivå i blodet betyder inte att processen inuti cellen fungerar — serum speglar transport, inte funktion."),
            ("Rubbad dygnsrytm i stressystemet", "Kortisol ska vara högt på morgonen och lågt på kvällen. Efter långvarig belastning plattas kurvan ut eller förskjuts. Typiskt mönster: svårt att komma igång, svacka mitt på dagen, paradoxalt pigg sent på kvällen."),
            ("Låggradig inflammation", "Kronisk immunaktivering förbrukar energi och påverkar hjärnan direkt. Den behöver inte synas som förhöjt CRP."),
            ("Sköldkörteln i gränslandet", "Ett TSH inom referensintervallet utesluter inte att sköldkörteln bidrar, särskilt om antikroppar finns eller om omvandlingen från T4 till T3 är otillräcklig."),
            ("Sömn som är lång men inte återhämtande", "Åtta timmar i sängen är inte åtta timmars återhämtning. Sömnapné och nattligt stresspåslag ger normal sömnlängd med utebliven återhämtning."),
            ("Järn- och B12-status i gränslandet", "Ferritin i nedre delen av referensintervallet ger ofta symtom långt innan blodvärdet påverkas, särskilt hos menstruerande kvinnor."),
        ],
        roda=["Ofrivillig viktnedgång", "Feber eller nattliga svettningar",
              "Andfåddhet eller bröstsmärta vid ansträngning",
              "Nytillkomna neurologiska symtom — domningar, synpåverkan, svaghet",
              "Trötthet som snabbt förvärrats över veckor",
              "Nedstämdhet, hopplöshet eller tankar på att inte vilja leva",
              "Blodbrist som inte förklaras"],
        matbart=[("Cellens energiproduktion", "Organiska syror, aminosyror, mitokondriella markörer", "nutreval-sverige"),
                 ("Metabol flaskhals utan blodprov", "Organiska syror via urinprov hemma", "metabolomik"),
                 ("Stressystemets dygnskurva", "Kortisol vid flera tidpunkter plus DHEA", "adrenal-stress"),
                 ("Inflammatorisk grundton", "Omega-3-index och omega-6/omega-3-kvot", "fettsyror"),
                 ("Hormonell orsak hos kvinnor", "Könshormoner, kortisol och melatonin över tid", "kvinnohalsa")],
        sjalv=[("Se till att basutredningen faktiskt är gjord", "Blodstatus, ferritin, B12, folat, TSH, glukos och CRP. Det är gratis, snabbt och nödvändigt innan något mer avancerat är meningsfullt. Be om att få se siffrorna, inte bara beskedet att allt var normalt."),
               ("Notera tröttheten över dygnet i två veckor", "Skatta din energi tre gånger om dagen. Mönstret är diagnostiskt: jämnt låg energi pekar mot något annat än energi som är låg på morgonen och stiger på kvällen."),
               ("Uteslut sömnapné om du snarkar", "Det är vanligt, underdiagnostiserat och behandlingsbart. Ingen näringsanalys kompenserar för fragmenterad sömn."),
               ("Var skeptisk mot att fylla på med tillskott på måfå", "Utan mätning blir det gissningar, och vissa tillskott i höga doser kan förskjuta andra system.")],
        faq=[("Varför är jag trött trots att alla prover är normala?",
              "Rutinprover är konstruerade för att upptäcka sjukdom, inte för att beskriva funktion. De mäter koncentrationen av ett fåtal ämnen i blodet, inte om de biokemiska processer som kräver dessa ämnen fungerar inne i cellen. En normal serumnivå kan därför förekomma samtidigt som cellens energiproduktion har en flaskhals."),
             ("Vilka prover kan visa varför jag är trött?",
              "Bortom basutredningen kan cellens energiproduktion mätas via organiska syror och aminosyror, stressystemets dygnskurva via kortisol vid flera tidpunkter, samt fettsyrestatus. NutrEval FMV kostar 12 200 kr, Metabolomix+ 8 100 kr och Adrenocortex Stress Profile 2 100 kr via MediBalans."),
             ("Vad är skillnaden mellan vanlig trötthet och utmattning?",
              "Vanlig trötthet förbättras av vila och sömn. Vid utmattning ger vila inte samma återhämtning, och tröttheten åtföljs ofta av kognitiva symtom, sömnstörning och nedsatt stresstolerans. Om vila inte hjälper är det ett skäl att utreda vidare."),
             ("Kan trötthet bero på tarmen?",
              "Det förekommer. Nedsatt upptag av näringsämnen, låggradig tarminflammation och immunreaktivitet mot födoämnen kan alla bidra. Har du både magbesvär och trötthet är det ofta rimligt att utreda tarmen först.")],
        rel=[("nutreval-sverige", "125+ biomarkörer: organiska syror, aminosyror, fettsyror, vitaminer och mineraler."),
             ("adrenal-stress", "Kortisol vid tidsbestämda tidpunkter under dygnet plus DHEA.")],
        noter=[],
    ),
    dict(
        slug="reagerar-pa-maten",
        kicker="Symtomguide · Mat &amp; immunreaktivitet",
        title="Magen reagerar på nästan allt jag äter — vad det kan betyda | MediBalans",
        desc="När allt fler livsmedel ger symtom är förklaringen sällan att du blivit allergisk mot allt. Vad som faktiskt händer, riskerna med att eliminera på egen hand, och vad som går att mäta.",
        h1="Magen reagerar på nästan allt jag äter — ", h1em="vad betyder det?",
        lead="Listan över mat du inte tål blir längre för varje månad. Det tolkas ofta som att kroppen blivit allergisk mot allt fler saker. Vanligare är att något annat pågår — och att den växande listan är ett symtom på det, inte förklaringen.",
        svar="Kort svar: när toleransen för mat gradvis minskar handlar det sällan om äkta allergi. De vanligaste förklaringarna är nedsatt nedbrytningskapacitet, en tarmslemhinna med pågående låggradig inflammation, fördröjda immunreaktioner mot vanliga födoämnen, och en tarmflora som blivit mindre robust — ofta som följd av upprepade elimineringsdieter.",
        orsaker=[
            ("Äkta allergi är ovanligt i den här bilden", "IgE-medierad allergi ger snabba, förutsägbara och ofta dramatiska reaktioner mot ett fåtal specifika ämnen. Det stämmer sällan med bilden av gradvis försämrad tolerans mot allt fler livsmedel."),
            ("Fördröjda immunreaktioner", "Cellulära immunreaktioner mot födoämnen kommer timmar till dygn efter måltid. Fördröjningen gör dem närmast omöjliga att identifiera med matdagbok."),
            ("Nedsatt nedbrytningskapacitet", "Är enzym- eller syraproduktionen otillräcklig blir fler livsmedel svåra att hantera — inte för att de är farliga, utan för att de inte bryts ned tillräckligt."),
            ("Tarmslemhinnan är påverkad", "Vid pågående låggradig inflammation blir slemhinnan mer lättretad. Då ger även normala födoämnen symtom, ungefär som att salt svider mer i ett sår än på hel hud."),
            ("Kosten har smalnat av", "Varje eliminering minskar mångfalden i tarmfloran, och en mindre mångfaldig flora hanterar variation sämre. Det skapar en självförstärkande spiral."),
        ],
        roda=["Svullnad i läppar, tunga eller svalg — sök akut vård",
              "Andningssvårigheter eller nässelutslag vid måltid — sök akut vård",
              "Ofrivillig viktnedgång eller näringsbrist", "Blod i avföringen",
              "Kräkningar eller svårighet att svälja",
              "Kraftigt begränsad kost under lång tid",
              "Ångest inför måltider eller växande kontrollbehov kring mat"],
        matbart=[("Fördröjd immunreaktivitet mot födoämnen", "Cellulär reaktivitet mot upp till 250 eller 483 livsmedel, tillsatser och kemikalier", "alcat"),
                 ("Tarmslemhinnans inflammation", "Kalprotektin, EPX, sekretoriskt IgA", "gi-effects-test"),
                 ("Nedbrytningskapacitet", "Pankreaselastas-1, fekalt fett", "gi-effects-test"),
                 ("Tarmflorans mångfald", "Mikrobiom via PCR och kortkedjiga fettsyror", "gi-effects-test"),
                 ("Bakteriell jäsning i tunntarmen", "Väte- och metangas i utandningsluft", "sibo-test")],
        sjalv=[("Sluta utöka elimineringen tills du vet varför", "Varje ny eliminering utan underlag gör kosten smalare och senare utredning svårare att tolka. Växer listan är det ett skäl att utreda, inte att fortsätta ta bort."),
               ("Uteslut celiaki innan du tar bort gluten", "Celiakiprov blir opålitligt om du redan slutat äta gluten. Ordningen spelar roll — testa först, eliminera sedan."),
               ("Notera tidsfördröjningen, inte bara vad du åt", "Reaktioner inom minuter, inom timmar och efter ett dygn pekar mot helt olika mekanismer."),
               ("Var uppmärksam på hur du mår kring maten", "Har måltider börjat kännas ångestfyllda eller växer kontrollbehovet kring mat är det något som förtjänar hjälp i sig, oavsett vad utredningen visar.")],
        faq=[("Kan man bli intolerant mot allt fler livsmedel?",
              "Det man upplever är verkligt, men förklaringen är sällan att immunsystemet blivit allergiskt mot allt fler ämnen. Vanligare är att nedbrytningskapaciteten är nedsatt eller att tarmslemhinnan är lättretad, vilket gör att fler livsmedel ger symtom. Då är det tröskeln som sänkts, inte antalet allergier som ökat."),
             ("Vad är skillnaden mellan allergi och intolerans?",
              "Allergi är en IgE-medierad immunreaktion som kommer snabbt och kan vara livshotande. Intolerans handlar oftast om bristande nedbrytning, exempelvis laktosintolerans. Därutöver finns fördröjda cellulära immunreaktioner mot födoämnen, som kommer timmar till dygn efter måltid och som varken standardallergitest eller matdagbok fångar väl."),
             ("Varför hjälper inte matdagbok?",
              "Därför att en fördröjd reaktion kan komma upp till ett dygn efter måltiden. Det du noterar som orsak är då oftast fel måltid. Det är också anledningen till att många hamnar i att eliminera allt fler livsmedel utan att bli bättre."),
             ("Ska jag utesluta gluten och mjölk för säkerhets skull?",
              "Inte utan att först testa för celiaki, eftersom det provet blir opålitligt när du slutat äta gluten. Långvariga elimineringar utan underlag smalnar av kosten och försämrar tarmflorans mångfald, vilket kan förvärra bilden på sikt.")],
        rel=[("gi-effects-test", "Utökat avföringsprov: inflammation, nedbrytning, mikrobiom och barriär."),
             ("sibo-test", "Väte- och metangasandningstest för bakteriell överväxt.")],
        noter=[("Evolutionär missmatchning — vad testet egentligen mäter", "/clinical-notes/#cn-011", "Klinisk notering av Mario Anthis om varför reaktivitet bör förstås som igenkänning.")],
    ),
    dict(
        slug="hjarndimma",
        kicker="Symtomguide · Kognition",
        title="Hjärndimma — varför tankarna känns sega och vad som går att mäta | MediBalans",
        desc="Hjärndimma är ett verkligt symtom med flera möjliga förklaringar. Vanliga orsaker, när du ska söka vård, och vilka faktorer som går att mäta objektivt.",
        h1="Hjärndimma — när tankarna ", h1em="går genom sirap",
        lead="Du hittar inte orden. Du läser samma stycke tre gånger. Du går in i ett rum och glömmer varför. Hjärndimma är inte ett medicinskt diagnosbegrepp, men det beskriver något verkligt — och det har nästan alltid en fysiologisk komponent som går att undersöka.",
        svar="Kort svar: hjärnan är metabolt krävande och känslig för störningar i energiförsörjning, inflammation och dygnsrytm. De vanligaste förklaringarna är otillräcklig cellulär energiproduktion, låggradig inflammation, rubbad dygnsrytm, hormonella förändringar och näringsmässiga kofaktorbrister.",
        orsaker=[
            ("Hjärnan får inte tillräckligt med energi", "Hjärnan använder omkring en femtedel av kroppens energi. När mitokondriell energiproduktion har en flaskhals märks det ofta först kognitivt, innan det märks som kroppslig trötthet."),
            ("Låggradig inflammation", "Inflammatorisk signalering påverkar hjärnan direkt och ger nedsatt koncentration och långsammare tankeverksamhet. Detta kan förekomma utan att CRP är förhöjt."),
            ("Rubbad dygnsrytm", "Kognitiv skärpa följer dygnsrytmen tätt. Vid utplattad kortisolkurva uteblir den morgonskärpa som normalt finns."),
            ("Hormonella förändringar", "Östrogen påverkar hjärnans energiomsättning och signalsubstanser. Kognitiva symtom i perimenopausen är vanliga, verkliga och underrapporterade."),
            ("Kofaktorer för signalsubstanser saknas", "Syntesen av dopamin, serotonin och noradrenalin kräver B-vitaminer, järn och magnesium. Otillräcklig tillgång ger kognitiva symtom innan det syns i standardprover."),
            ("Sömn, blodsocker och läkemedel", "Fragmenterad sömn, kraftiga blodsockersvängningar och vissa läkemedel är vanliga och ofta förbisedda bidragande orsaker."),
        ],
        roda=["Plötslig förvirring eller talsvårigheter — sök akut vård",
              "Ensidig svaghet eller domning — sök akut vård",
              "Minnesförlust som andra i din omgivning noterar",
              "Svårighet att sköta vardagliga sysslor du tidigare klarade",
              "Nytillkomna kognitiva symtom efter huvudskada",
              "Synförändringar eller ihållande huvudvärk",
              "Symtom som snabbt förvärras över veckor"],
        matbart=[("Mitokondriell energiproduktion", "Organiska syror och Krebscykelns intermediärer", "organix"),
                 ("Signalsubstansernas metabolism", "Nedbrytningsprodukter från dopamin och serotonin", "organix"),
                 ("Näringsmässiga kofaktorer", "B-vitaminer, magnesium, aminosyror, antioxidantstatus", "nutreval-sverige"),
                 ("Fettsyrestatus i hjärnan", "Omega-3-index, särskilt DHA", "fettsyror"),
                 ("Dygnsrytm och stressystem", "Kortisolkurva över dygnet", "adrenal-stress"),
                 ("Hormonell orsak i perimenopaus", "Östrogener, progesteron och melatonin över flera dagar", "menopaus-plus")],
        sjalv=[("Uteslut det enkla först", "Blodstatus, ferritin, B12, folat, TSH och glukos. Järnbrist och sköldkörtelpåverkan är vanliga, behandlingsbara orsaker till kognitiva symtom."),
               ("Kartlägg när på dygnet dimman är värst", "Värst på morgonen pekar mot dygnsrytm. Värst efter måltid pekar mot blodsocker. Jämnt över dagen pekar mot något mer grundläggande."),
               ("Se över sömnen innan något annat", "Ingen analys kompenserar för fragmenterad sömn, och sömnapné är både vanligt och behandlingsbart."),
               ("Notera om det följer cykeln", "Kognitiva symtom som kommit tillsammans med förändrad mens, sömn eller värmevallningar har ofta en hormonell komponent.")],
        faq=[("Vad är hjärndimma?",
              "Hjärndimma är inte en medicinsk diagnos utan en beskrivning av nedsatt kognitiv skärpa — sämre koncentration, ordglömska, långsammare tankeverksamhet och sämre arbetsminne. Symtomet är verkligt och har nästan alltid en fysiologisk komponent, oftast kopplad till energiförsörjning, inflammation, dygnsrytm eller hormonell förändring."),
             ("Är hjärndimma ett tecken på demens?",
              "I de allra flesta fall nej, särskilt inte hos yngre personer och när symtomen varierar över dagen eller följer sömn och stress. Minnesförlust som andra i din omgivning noterar, eller svårighet att klara vardagssysslor du tidigare hanterade, är däremot skäl att söka vård för bedömning."),
             ("Vad kan mätas vid hjärndimma?",
              "Utöver basutredningen kan mitokondriell energiproduktion och signalsubstansmetabolism mätas via organiska syror i urin. Organix kostar 5 600 kr, NutrEval FMV 12 200 kr, fettsyreanalys 3 900 kr och Adrenocortex Stress Profile 2 100 kr via MediBalans."),
             ("Kan hjärndimma bero på tarmen?",
              "Indirekt, ja. Nedsatt näringsupptag, låggradig tarminflammation och immunaktivering påverkar hjärnans energiförsörjning och inflammatoriska miljö. Har du både magbesvär och kognitiva symtom är det ofta rimligt att utreda tarmen som en del av bilden.")],
        rel=[("organix", "Organiska syror i urin: mitokondriell funktion, neurotransmittorer, avgiftning."),
             ("nutreval-sverige", "Bred metabol och näringsmässig kartläggning, 125+ biomarkörer.")],
        noter=[],
    ),
    dict(
        slug="trott-efter-40-hormoner",
        kicker="Symtomguide · Hormoner efter 40",
        title="Trött, sover dåligt och inte dig själv efter 40 — hormonella orsaker | MediBalans",
        desc="Perimenopausen börjar ofta år innan mensen förändras och ger trötthet, sömnstörning och humörsvängningar. Varför blodprover ofta är normala, och vad som går att mäta istället.",
        h1="Trött, sover dåligt och inte dig själv efter 40 — ", h1em="det kan vara hormonellt",
        lead="Det börjar sällan med värmevallningar. Det börjar med att sömnen blir sämre, att tålamodet tar slut fortare och att du inte riktigt känner igen dig själv. Perimenopausen kan börja upp till ett decennium innan mensen förändras märkbart.",
        svar="Kort svar: i perimenopausen fluktuerar hormonerna kraftigt från dag till dag innan de sjunker. Ett blodprov taget en enskild dag hamnar därför ofta inom referensintervallet trots uttalade symtom — inte för att hormonerna är stabila, utan för att provet fångade en punkt i en kurva som svänger.",
        orsaker=[
            ("Progesteron sjunker först", "Progesteron minskar ofta flera år före östrogen. Eftersom progesteron har lugnande och sömnfrämjande effekt märks nedgången först som sämre sömn och kortare stubin — långt före klassiska klimakteriebesvär."),
            ("Östrogen fluktuerar innan det sjunker", "I perimenopausen svänger östrogen kraftigt uppåt och nedåt. Det är svängningarna i sig, snarare än låga nivåer, som ger många av symtomen — och de gör enstaka blodprover svårtolkade."),
            ("Sömnen blir mindre återhämtande", "Hormonella förändringar påverkar sömnarkitekturen. Du kan sova lika många timmar men få mindre djupsömn."),
            ("Stressystemet blir känsligare", "Hormonella förändringar och HPA-axeln påverkar varandra. Många beskriver att samma arbetsbelastning som tidigare fungerade nu känns ohanterlig."),
            ("Sköldkörtel och järn förändras samtidigt", "Sköldkörtelsjukdom debuterar ofta i samma åldersspann, och tunga blödningar kan tömma järndepåerna. Båda ger liknande symtom och måste uteslutas."),
            ("Ämnesomsättning och kroppssammansättning skiftar", "Förändrad insulinkänslighet och muskelmassa gör att samma kost och träning ger andra resultat än tidigare."),
        ],
        roda=["Blödningar som är mycket rikliga eller långdragna",
              "Blödning mellan menstruationer eller efter samlag",
              "Blödning efter att mensen upphört i mer än ett år — sök vård",
              "Ofrivillig viktnedgång", "Nytillkommen kraftig nedstämdhet eller ångest",
              "Bröstförändringar eller knöl", "Symtom som snabbt förvärrats"],
        matbart=[("Hormonell fluktuation över flera dagar", "Östrogener, progesteron, P/E2-kvot, testosteron, DHEA, kortisol, melatonin", "menopaus-plus"),
                 ("Hormoner i sitt dygnssammanhang", "Könshormoner med kortisolkurva och östrogenmetabolism", "kvinnohalsa"),
                 ("Östrogenets nedbrytningsvägar", "2-OH-, 4-OH- och 16α-OH-metaboliter samt metylering", "essential-ostrogen"),
                 ("Stressystemets dygnskurva", "Kortisol vid flera tidpunkter plus DHEA", "adrenal-stress"),
                 ("Näringsstatus och energiproduktion", "Organiska syror, aminosyror, vitaminer och mineraler", "nutreval-sverige")],
        sjalv=[("Be om basproverna och se siffrorna", "TSH, ferritin, blodstatus, B12 och glukos. Sköldkörtelsjukdom och järnbrist är vanliga i den här åldern och ger symtom som lätt tillskrivs hormoner."),
               ("Följ symtomen mot cykeln i tre månader", "Notera sömn, energi och humör tillsammans med var i cykeln du befinner dig. Mönster över tid är mer informativt än enstaka värden."),
               ("Ta symtomen på allvar även om proverna är normala", "Normala prover i perimenopausen utesluter inte hormonell orsak. De speglar en dag i en kurva som svänger."),
               ("Skydda sömnen och muskelmassan", "Styrketräning och regelbunden sömnrytm är två av de mest effektiva åtgärderna i den här fasen, oavsett vad utredningen visar.")],
        faq=[("Varför är mina hormonprover normala trots tydliga symtom?",
              "I perimenopausen fluktuerar hormonnivåerna kraftigt från dag till dag. Ett blodprov taget en enskild dag kan därför falla inom referensintervallet trots uttalade symtom. Prov samlade vid flera tillfällen över flera dagar visar mönstret och fluktuationen istället för en enskild punkt."),
             ("När börjar perimenopausen?",
              "Den kan börja upp till tio år innan menstruationen upphör, ofta i 40-årsåldern och ibland tidigare. De första tecknen är sällan värmevallningar utan snarare sämre sömn, sänkt stresstolerans, humörsvängningar och trötthet."),
             ("Kan trötthet efter 40 bero på något annat än hormoner?",
              "Ja, och det bör uteslutas först. Sköldkörtelsjukdom, järnbrist, sömnapné och depression är vanliga i samma åldersspann och ger liknande symtom. En hormonell utredning är mest meningsfull när basutredningen är gjord."),
             ("Vad kan mätas vid perimenopausala besvär?",
              "Hormoner kan mätas vid flera tillfällen över flera dagar för att fånga fluktuationen, tillsammans med kortisolkurva och melatonin. Women's Health+ kostar 6 200 kr och Adrenocortex Stress Profile 2 100 kr via MediBalans. Menopause Plus och Essential Estrogens prissätts vid konsultation.")],
        rel=[("kvinnohalsa", "Könshormoner, kortisolkurva och östrogenmetabolism i ett sammanhang."),
             ("menopaus-plus", "Salivprov över flera dagar som fångar hormonell fluktuation.")],
        noter=[],
    ),
]


def build_guide(g):
    url = f"{BASE}/symtom/{g['slug']}/"
    anchors = [("orsaker", "Vanliga orsaker"), ("sok-vard", "När du ska söka vård"),
               ("matbart", "Vad som går att mäta"), ("sjalv", "Vad du kan göra själv"),
               ("faq", "Vanliga frågor")]
    orsaker = "".join(f"<h3>{t}</h3><p>{d}</p>" for t, d in g["orsaker"])
    roda = "".join(f"<li>{x}</li>" for x in g["roda"])
    sjalv = "".join(f"<h3>{t}</h3><p>{d}</p>" for t, d in g["sjalv"])
    rows = ""
    for orsak, matning, slug in g["matbart"]:
        name, pris = PANEL[slug]
        rows += (f'<tr><td><strong>{orsak}</strong></td><td>{matning}</td>'
                 f'<td><a href="/{slug}/">{name}</a></td></tr>')
    cards = "".join(pcard(s, d) for s, d in g["rel"])
    for n in g["noter"]:
        cards += ncard(n[0], n[1], n[2] if len(n) > 2 else "Fördjupning — evidensläge och tolkning.")

    schema = [
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "MedicalWebPage",
            "@id": url + "#page", "url": url, "name": g["title"], "inLanguage": "sv-SE",
            "datePublished": "2026-07-28", "dateModified": "2026-07-28",
            "audience": {"@type": "Patient"}, "provider": ORG, "publisher": ORG,
        }, ensure_ascii=False) + "</script>",
        faq_schema(url, g["faq"]),
    ]

    content = f"""
{hero(g['kicker'], g['h1'], g['h1em'], g['lead'],
      '<a class="btn-p" href="/#booking">Boka konsultation</a>'
      '<a class="btn-s" href="#matbart">Vad som går att mäta</a>',
      'Klinisk bedömning av legitimerad läkare. Patienter i hela Sverige.',
      [(str(len(g['orsaker'])), 'Möjliga orsaker'), (str(len(g['matbart'])), 'Mätbara faktorer'),
       ('Hemtest', 'Provtagning'), ('2–3 v', 'Svarstid')])}
{toc(anchors)}
<div class="container sec-body">
<section><p class="lead-p">{g['svar']}</p></section>
<section id="orsaker"><h2>Vanliga <em>orsaker</em></h2>{orsaker}</section>
<section id="sok-vard"><h2>När du ska <em>söka vård</em></h2>
<p>Följande symtom ska bedömas inom sjukvården innan någon utvidgad utredning blir aktuell. De utesluts bäst tidigt och kostar inget att kontrollera.</p>
<div class="box-warn"><ul>{roda}</ul></div>
<p>Ingen funktionell analys ersätter en konventionell medicinsk bedömning vid dessa symtom.</p></section>
<section id="matbart"><h2>Vad som faktiskt går att <em>mäta</em></h2>
<p>Flera av orsakerna ovan går att undersöka objektivt. Tabellen visar vilken mätning som svarar på vilken fråga — vilken som är motiverad i ditt fall avgörs av symtommönstret, inte av hur omfattande panelen är.</p>
<table><thead><tr><th>Möjlig orsak</th><th>Vad som mäts</th><th>Analys</th></tr></thead><tbody>{rows}</tbody></table>
<div class="box"><p>MediBalans är officiell svensk distributör för Genova Diagnostics. Analyserna beställs efter klinisk bedömning, provet tas oftast hemma och svaret tolkas av legitimerad läkare tillsammans med din sjukhistoria.</p></div></section>
<section id="sjalv"><h2>Vad du kan göra <em>själv först</em></h2>{sjalv}</section>
<section id="relaterat"><h2>Läs <em>vidare</em></h2><div class="card-grid">{cards}</div>
<p style="margin-top:1.5rem"><a href="/symtom/">Alla symtomguider →</a> · <a href="/genova-diagnostics/">Samtliga analyser</a></p></section>
<section id="faq"><h2>Vanliga <em>frågor</em></h2>{faq_html(g['faq'])}</section>
</div>
{band('Ta reda på', 'varför', 'En inledande konsultation ger en klinisk bedömning av din situation och ett tydligt nästa steg — vilken utredning som är motiverad, och vilken som inte är det.')}
"""
    return page(g["title"], g["desc"], url, schema, content)


def build_guides_index():
    url = f"{BASE}/symtom/"
    cards = "".join(
        f'<a class="mb-card" href="/symtom/{g["slug"]}/"><span class="k">{g["kicker"].split("·")[-1].strip()}</span>'
        f'<div class="t">{g["h1"].rstrip(" —")}</div><p class="d">{g["lead"][:140]}…</p>'
        f'<div class="p">Läs guiden →</div></a>' for g in GUIDES)
    schema = ['<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage", "@id": url + "#collection",
        "url": url, "name": "Symtomguider — MediBalans", "inLanguage": "sv-SE", "publisher": ORG,
        "hasPart": [{"@type": "MedicalWebPage", "url": f"{BASE}/symtom/{g['slug']}/", "name": g["title"]}
                    for g in GUIDES]}, ensure_ascii=False) + "</script>"]
    content = f"""
{hero('Symtomguide · MediBalans Stockholm', 'Symtomguider ', 'Börja med hur du mår.',
      'Guider skrivna utifrån symtom snarare än diagnoser. Varje guide går igenom de vanligaste orsakerna, när du ska söka vård i stället, vad som faktiskt går att mäta objektivt — och vad du kan göra själv först.',
      '<a class="btn-p" href="/#booking">Boka konsultation</a><a class="btn-s" href="/genova-diagnostics/">Diagnostik</a>',
      'Guiderna ersätter inte medicinsk bedömning. Vid alarmsymtom gäller konventionell vård.',
      [(str(len(GUIDES)), 'Publicerade guider'), ('Hemtest', 'Provtagning'), ('2–3 v', 'Svarstid'), ('Läkare', 'Klinisk tolkning')])}
<div class="container sec-body" style="max-width:1100px">
<section id="guider"><h2>Välj det som <em>liknar dig</em></h2><div class="card-grid">{cards}</div></section>
</div>
<div class="container sec-body">
<section id="princip"><h2>Samma <em>princip</em> i alla guider</h2>
<p>Varje guide följer samma ordning, och den ordningen är medveten. Först vad symtomet vanligen beror på. Sedan de tecken som ska föra dig till vården i stället för till en utredning hos oss. Därefter vad som faktiskt går att mäta objektivt. Sist vad du kan göra själv — inklusive de kostnadsfria stegen inom vården som bör vara gjorda innan något mer avancerat är meningsfullt.</p>
<div class="box"><p>Rätt utredning är den minsta som besvarar din kliniska fråga. Ett omfattande prov beställt utan frågeställning ger begränsad vägledning, oavsett hur många markörer det innehåller.</p></div></section>
</div>
{band('Ta reda på', 'varför', 'En inledande konsultation ger en klinisk bedömning och ett tydligt nästa steg.')}
"""
    return page("Symtomguider — från symtom till mätbar orsak | MediBalans",
                "Guider utifrån symtom: uppblåst mage, trötthet trots sömn, reaktioner på mat, hjärndimma och hormonella besvär efter 40. Vanliga orsaker, när du ska söka vård och vad som går att mäta.",
                url, schema, content)


# ═══════════════════════════════════════════════════ SKRIFTER
ESSAY = dict(
    slug="evolutionar-missmatchning",
    kicker="Skrifter · Immunologi",
    title="Evolutionär missmatchning — vad ett cellulärt reaktivitetstest egentligen mäter | MediBalans",
    desc="Frågan är inte om du blivit allergisk mot mat, utan vad immunförsvaret känner igen. Mario Anthis om varför cellulär födoämnesreaktivitet bör förstås som igenkänning snarare än sjukdom.",
    h1="Evolutionär missmatchning ", h1em="Vad testet egentligen mäter.",
    lead="Den vanligaste frågan jag får är om patienten blivit allergisk mot mat. Nästan alltid är svaret nej — och den frågan leder fel. Det som mäts vid cellulär reaktivitetstestning är inte allergi. Det är igenkänning.",
    sections=[
        ("kategorifelet", "Kategorifelet", [
            "Allergi i strikt mening är IgE-medierad. Immunglobulin E binder till mastceller, reaktionen kommer inom minuter, den är förutsägbar och den kan vara livshotande. Det är ett väldefinierat och väl validerat kliniskt fenomen, och den utredningen ska göras av allergolog när misstanken finns.",
            "Cellulär reaktivitet mot födoämnen är någonting annat. Den utgår i hög grad från det medfödda immunförsvaret — granulocyter och andra celler som reagerar på ämnen de inte känner igen som ofarliga. Reaktionen kommer timmar till dygn senare, den är dosberoende och den är sällan dramatisk. Den ger inte anafylaxi. Den ger låggradig, återkommande inflammation.",
            "När dessa två slås ihop under ordet &rdquo;matallergi&rdquo; uppstår ett kategorifel med två olyckliga konsekvenser. Patienter med negativa IgE-prover får höra att maten inte kan vara inblandad, trots att de tydligt reagerar. Och patienter med cellulär reaktivitet tror att de bär på en farlig allergi, vilket de i regel inte gör.",
        ]),
        ("igenkanning", "Igenkänning, inte sjukdom", [
            "Immunförsvarets grundläggande uppgift är att avgöra vad som hör hemma i kroppen och vad som inte gör det. Det är en igenkänningsapparat, kalibrerad under lång tid mot en viss omgivning.",
            "Den omgivningen har förändrats snabbare än kalibreringen hunnit följa med. Livsmedelsindustriella proteiner, hydrolysat, emulgeringsmedel, konserveringsmedel, färgämnen och restsubstanser från odling och förpackning — merparten av detta har introducerats under en tidsrymd som i evolutionära termer är försumbar. Immunförsvaret möter alltså regelbundet molekyler det inte har någon nedärvd anledning att betrakta som föda.",
            "Ur det perspektivet är en cellulär reaktion inte ett fel i systemet. Den är systemet som gör exakt det den är byggd för att göra, mot indata den inte är byggd för att möta. Det är därför jag betraktar fyndet som uttryck för missmatchning snarare än för sjukdom.",
        ]),
        ("konsekvensen", "Den kliniska konsekvensen", [
            "Skillnaden är inte semantisk. Den avgör hur en behandlingsplan uppfattas och därmed om den följs.",
            "Uppfattar patienten en eliminationsplan som en lista över förbjuden mat blir den en fråga om disciplin, och disciplin tar slut. Uppfattas samma plan som en återgång till det den egna biologin faktiskt känner igen blir den begriplig — och begriplighet är i min erfarenhet en starkare drivkraft för följsamhet än viljestyrka.",
            "Lika viktigt är att elimination här är ett tidsbegränsat verktyg, inte ett permanent tillstånd. Syftet är att sänka den inflammatoriska belastningen tillräckligt länge för att toleransen ska kunna återhämta sig, varefter födoämnen återintroduceras strukturerat. En plan utan återintroduktionsfas har missförstått sitt eget syfte.",
        ]),
        ("evidens", "Vad evidensen stödjer — och inte", [
            "Metodkritik mot cellulär reaktivitetstestning existerar och ska inte viftas bort. Den mest citerade invändningen rör reproducerbarhet i delade prover. Den kritiken är relevant för hur ett svar ska tolkas, och den är ett av skälen till att jag aldrig läser ett testsvar isolerat.",
            "Samtidigt finns kontrollerad evidens. I en dubbelblind, placebokontrollerad studie vid Yale prövades eliminationskost baserad på cellulär reaktivitetstestning hos patienter med irritabel tarm, med symtomförbättring i den aktiva gruppen. Mekanistiskt arbete från samma forskningsmiljö har därefter undersökt hur födoämnen kan utlösa frisättning av DNA från medfödda immunceller. Tidigare randomiserat arbete har undersökt kroppssammansättning vid reaktivitetsstyrd kost.",
            "Vad detta sammantaget stödjer är att reaktivitetsstyrd elimination kan ge klinisk effekt. Vad det inte stödjer är påståendet att testet ensamt förklarar en patients hela sjukdomsbild. Reaktivitet är i regel en dominerande drivkraft bland flera — inte en monokausal förklaring — och den som utlovar det senare säljer något annat än medicin.",
        ]),
        ("granser", "Vad denna text inte gör anspråk på", [
            "Detta är en klinisk observation och en tolkningsram, inte ett bevis för mekanism. Ramen är fruktbar i mitt arbete därför att den förklarar mönster jag ser återkomma och därför att den ger patienter ett begripligt varför. Den är inte prövad som hypotes i sin egen rätt.",
            "Cellulär reaktivitetstestning ersätter inte allergiutredning, inte celiakiutredning och inte utredning av inflammatorisk tarmsjukdom. Vid alarmsymtom gäller konventionell handläggning oavsett vad någon funktionell analys visar.",
            "Och ett provsvar är fortfarande ett underlag, inte ett utlåtande. Det avgörande är inte vad listan innehåller utan vilken klinisk fråga den var tänkt att besvara.",
        ]),
    ],
    kallor=[
        "Ali A, Weiss TR, McKee D, et al. Efficacy of individualised diets in patients with irritable bowel syndrome: a randomised controlled trial. <em>BMJ Open Gastroenterology</em> 2017.",
        "Garcia-Martinez I, Weiss TR, Yousaf MN, Ali A, Mehal WZ. A leukocyte activation test identifies food items which induce release of DNA by innate immune peripheral blood leucocytes. <em>Nutrition &amp; Metabolism</em> 2018.",
        "Kaats GR, Pullin D, Parker LK. The short term efficacy of the ALCAT test of food sensitivities to facilitate changes in body composition and self-reported disease symptoms. <em>The Bariatrician</em> 1996.",
    ],
    faq=[
        ("Är cellulär födoämnesreaktivitet samma sak som allergi?",
         "Nej. Allergi i strikt mening är IgE-medierad, kommer inom minuter och kan vara livshotande. Cellulär reaktivitet utgår i hög grad från det medfödda immunförsvaret, kommer timmar till dygn efter intag och ger låggradig inflammation snarare än akut reaktion. De är olika fenomen och kräver olika utredning."),
        ("Vad menas med evolutionär missmatchning?",
         "Att immunförsvarets igenkänningsapparat är kalibrerad mot en födoomgivning som inte längre är den vi lever i. Industriellt bearbetade proteiner, tillsatser och restsubstanser har introducerats under en tidsrymd som i evolutionära termer är försumbar. En cellulär reaktion mot sådana ämnen är därför inte nödvändigtvis ett fel i systemet utan systemet som arbetar mot indata det inte är byggt för."),
        ("Innebär det att jag aldrig mer kan äta de livsmedlen?",
         "Nej. Elimination är ett tidsbegränsat verktyg vars syfte är att sänka den inflammatoriska belastningen tillräckligt länge för att toleransen ska kunna återhämta sig. En plan utan strukturerad återintroduktionsfas har missförstått sitt eget syfte."),
        ("Är metoden vetenskapligt underbyggd?",
         "Det finns kontrollerad evidens, bland annat en dubbelblind placebokontrollerad studie vid Yale på patienter med irritabel tarm samt efterföljande mekanistiskt arbete. Det finns också metodkritik, framför allt rörande reproducerbarhet i delade prover. Slutsatsen jag drar är att reaktivitetsstyrd elimination kan ge klinisk effekt, men att ett testsvar aldrig bör läsas isolerat."),
    ],
)


def build_essay(e):
    url = f"{BASE}/skrifter/{e['slug']}/"
    anchors = [(a, t) for a, t, _ in e["sections"]] + [("faq", "Vanliga frågor")]
    secs = "".join(f'<section id="{a}"><h2>{t}</h2>' + "".join(f"<p>{p}</p>" for p in ps) + "</section>"
                   for a, t, ps in e["sections"])
    kallor = "".join(f"<li>{k}</li>" for k in e["kallor"])
    schema = [
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@graph": [
                AUTHOR_NODE,
                {"@type": "Article", "@id": url + "#article", "url": url,
                 "headline": "Evolutionär missmatchning — vad ett cellulärt reaktivitetstest egentligen mäter",
                 "description": e["desc"], "inLanguage": "sv-SE",
                 "datePublished": "2026-07-28", "dateModified": "2026-07-28",
                 "author": {"@id": AUTHOR_ID}, "publisher": ORG,
                 "isPartOf": {"@id": f"{BASE}/skrifter/#collection"},
                 "genre": "Klinisk observation och hypotes"}]}, ensure_ascii=False) + "</script>",
        faq_schema(url, e["faq"]),
    ]
    content = f"""
{hero(e['kicker'], e['h1'], e['h1em'], e['lead'],
      '<a class="btn-p" href="/#booking">Boka konsultation</a><a class="btn-s" href="/skrifter/">Alla skrifter</a>',
      'Text av Mario Anthis, grundare och medicinsk chef. Klinisk observation och hypotes — inte etablerad evidens.',
      [('Skrifter', 'Författad text'), ('Anthis', 'Författare'), ('2026', 'Publicerad'), ('Hypotes', 'Texttyp')])}
{toc(anchors)}
<div class="container sec-body">
<section><div class="box"><p><strong>Om denna text.</strong> Skrifter är min egen sektion för kliniska observationer, hypoteser och resonemang. Innehållet är författat i första person och ska läsas som klinisk erfarenhet och tolkningsram — inte som etablerad evidens eller behandlingsrekommendation. Där evidens åberopas anges källa.</p></div></section>
{secs}
<section id="faq"><h2>Vanliga <em>frågor</em></h2>{faq_html(e['faq'])}</section>
<section id="kallor"><h2>Källor</h2><ol class="src">{kallor}</ol>
<p style="margin-top:1.6rem"><a href="/alcat/">Läs om immunreaktivitetstestning →</a> · <a href="/symtom/reagerar-pa-maten/">Symtomguide: magen reagerar på allt jag äter</a></p></section>
</div>
{band('Mätning', 'före tolkning', 'Resonemanget ovan är en tolkningsram. Vad som gäller i ett enskilt fall avgörs av mätdata och klinisk bedömning — inte av en modell.')}
"""
    return page(e["title"], e["desc"], url, schema, content)


def build_skrifter_index():
    url = f"{BASE}/skrifter/"
    cards = (f'<a class="mb-card" href="/skrifter/{ESSAY["slug"]}/"><span class="k">{ESSAY["kicker"].split("·")[-1].strip()}</span>'
             f'<div class="t">Evolutionär missmatchning</div>'
             f'<p class="d">{ESSAY["lead"][:150]}…</p><div class="p">Mario Anthis · 2026</div></a>')
    schema = ['<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@graph": [
            AUTHOR_NODE,
            {"@type": "CollectionPage", "@id": url + "#collection", "url": url,
             "name": "Skrifter — Mario Anthis", "inLanguage": "sv-SE",
             "author": {"@id": AUTHOR_ID}, "publisher": ORG}]}, ensure_ascii=False) + "</script>"]
    content = f"""
{hero('Skrifter · Mario Anthis', 'Skrifter ', 'Vad tjugofem år lärt mig.',
      'Denna sektion är min egen. Här skriver jag i första person om kliniska mönster jag ser återkomma, om tolkningsramar som visat sig fruktbara, och om var jag menar att den etablerade förståelsen är otillräcklig. Texterna är erfarenhet och hypotes — inte etablerad evidens.',
      '<a class="btn-p" href="/#booking">Boka konsultation</a><a class="btn-s" href="/clinical-notes/">Kliniska noteringar</a>',
      'För institutionell evidensgenomgång, se Kliniska noteringar.',
      [('1', 'Publicerad text'), ('Anthis', 'Författare'), ('Svenska', 'Språk'), ('Löpande', 'Publicering')])}
<div class="container sec-body">
<section id="om"><h2>Tre lager, <em>tre uppgifter</em></h2>
<p>Webbplatsen har tre sorters text och de gör olika saker. Att hålla isär dem gör var och en mer användbar.</p>
<table><tbody>
<tr><td><strong><a href="/symtom/">Symtomguider</a></strong></td><td>Skrivna för dig som söker efter hur du mår. Beskriver möjliga orsaker och vad som går att mäta.</td></tr>
<tr><td><strong><a href="/clinical-notes/">Kliniska noteringar</a></strong></td><td>Institutionell genomgång av evidensläget för en specifik metod eller frågeställning.</td></tr>
<tr><td><strong>Skrifter</strong></td><td>Mina egna texter. Första person, hypotes och klinisk erfarenhet — med tydligt angivna gränser för vad de gör anspråk på.</td></tr>
</tbody></table></section>
<section id="texter"><h2>Publicerade <em>texter</em></h2><div class="card-grid">{cards}</div></section>
</div>
{band('Mät', 'först', 'Varje resonemang här vilar på samma princip: mätning före tolkning, tolkning före behandling.')}
"""
    return page("Skrifter — Mario Anthis | MediBalans",
                "Kliniska observationer, hypoteser och resonemang av Mario Anthis, grundare och medicinsk chef vid MediBalans. Författade texter — erfarenhet och tolkningsram, inte etablerad evidens.",
                url, schema, content)


# ═══════════════════════════════════════════════════ SKRIV
def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)
    print("  ", rel, f"({len(content):,} tecken)")


if __name__ == "__main__":
    print("Symtomguider:")
    write("symtom/index.html", build_guides_index())
    for g in GUIDES:
        write(f"symtom/{g['slug']}/index.html", build_guide(g))
    print("\nKlart.")
