#!/usr/bin/env node
// add_faq_schema2.mjs — second batch of FAQPage JSON-LD schema injections

import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname);
const p = (rel) => resolve(ROOT, rel.replace(/\//g, '\\'));

function read(rel) { return readFileSync(p(rel), 'utf8'); }
function write(rel, content) { writeFileSync(p(rel), content, 'utf8'); }

function makeFAQ(qas) {
  return JSON.stringify({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": qas.map(({ q, a }) => ({
      "@type": "Question",
      "name": q,
      "acceptedAnswer": { "@type": "Answer", "text": a }
    }))
  });
}

function applyFAQ(rel, faqJson) {
  let c = read(rel);
  const orig = c;

  // Replace existing FAQPage block (handles minified or pretty-printed)
  const faqBlockRx = /<script\s+type="application\/ld\+json">[^<]*"@type"\s*:\s*"FAQPage"[\s\S]*?<\/script>/;
  const replacement = `<script type="application/ld+json">${faqJson}</script>`;

  if (faqBlockRx.test(c)) {
    c = c.replace(faqBlockRx, replacement);
  } else {
    // No existing FAQPage — insert after the last ld+json block
    const allJsonLd = [...c.matchAll(/<script\s+type="application\/ld\+json">/g)];
    let insertPos = -1;
    if (allJsonLd.length > 0) {
      const lastStart = allJsonLd[allJsonLd.length - 1].index;
      const closeIdx = c.indexOf('</script>', lastStart);
      if (closeIdx !== -1) insertPos = closeIdx + '</script>'.length;
    }
    if (insertPos !== -1) {
      c = c.slice(0, insertPos) + '\n' + replacement + c.slice(insertPos);
    } else {
      c = c.replace('</head>', replacement + '\n</head>');
    }
  }

  if (c !== orig) {
    write(rel, c);
    return true;
  }
  return false;
}

// ─── FAQ DATA ────────────────────────────────────────────────────────────────

const PAGES = [

  // ── Organix SV ────────────────────────────────────────────────────────────
  { rel: 'organix/index.html', qas: [
    { q: 'Vad är ett organiska syror test?', a: 'Organix® mäter organiska syror i urinen — metaboliter som berättar hur väl din kropp producerar energi, hanterar oxidativ stress och utför methylering. Det är ett funktionellt test som identifierar störningar i mitokondriell funktion, B-vitaminbrist och toxisk exponering.' },
    { q: 'Vad är skillnaden mellan Organix och ett vanligt urinprov?', a: 'Standardurinprov kontrollerar njurfunktion och infektion. Organix mäter 70+ metaboliter kopplade till energiproduktion (citronsyracykeln), neurotransmittorfunktion, avgiftning och methylering — störningar som är osynliga i rutinprover.' },
    { q: 'Vem behöver ett Organix test?', a: 'Organix är indicerat vid kronisk trötthet, fibromyalgi, hjärndimma, ADHD, migrän, kemisk känslighet och autoimmunitet. Det är särskilt värdefullt när standardutredningar inte ger svar.' },
    { q: 'Hur tar man Organix provet?', a: 'Organix är ett urinprov (första morgonurin). Testkitet skickas hem med instruktioner och förbetalat returkuvert till Genovas laboratorium.' },
    { q: 'Vad kostar Organix test i Sverige?', a: 'Organix® kostar 5 600 kr hos MediBalans, Sveriges officiella Genova-distributör. Priset inkluderar testkitet, analys och läkartolkning.' },
  ]},

  // ── Organix EN ────────────────────────────────────────────────────────────
  { rel: 'en/organix/index.html', qas: [
    { q: 'What is an organic acids test?', a: 'Organix® measures organic acids in urine — metabolites that reveal how well your body produces energy, manages oxidative stress and performs methylation. It is a functional test that identifies disturbances in mitochondrial function, B-vitamin deficiency and toxic exposure.' },
    { q: 'What is the difference between Organix and a standard urine test?', a: 'Standard urine tests check kidney function and infection. Organix measures 70+ metabolites linked to energy production (the citric acid cycle), neurotransmitter function, detoxification and methylation — disturbances that are invisible in routine panels.' },
    { q: 'Who needs an Organix test?', a: 'Organix is indicated in chronic fatigue, fibromyalgia, brain fog, ADHD, migraine, chemical sensitivity and autoimmunity. It is particularly valuable when standard investigations return no answers.' },
    { q: 'How do you collect the Organix sample?', a: 'Organix requires a first-morning urine sample. The test kit is sent to your home with instructions and a prepaid return envelope to the Genova laboratory.' },
    { q: 'How much does an Organix test cost?', a: 'Organix® is priced at SEK 5,600 at MediBalans, the official Swedish Genova distributor. The price includes the test kit, analysis and physician interpretation.' },
  ]},

  // ── Fettsyror SV ──────────────────────────────────────────────────────────
  { rel: 'fettsyror/index.html', qas: [
    { q: 'Vad är ett omega-3 test?', a: 'Ett omega-3 test mäter koncentrationen av omega-3, omega-6, mättade och omättade fettsyror i blodet. Essential & Metabolic Fatty Acids från Genova mäter 30+ fettsyror och beräknar Omega-3 Index — en stark markör för kardiovaskulär risk.' },
    { q: 'Varför är balansen mellan omega-3 och omega-6 viktig?', a: 'Omega-6 fettsyror (från vegetabiliska oljor och processad mat) driver inflammation. Omega-3 (från fisk och linfröolja) dämpar den. De flesta i Sverige har ett omega-6/omega-3 förhållande på 15-20:1 — optimalt är 4:1. Obalansen bidrar till kronisk inflammation, hjärtsjukdom och autoimmunitet.' },
    { q: 'Vad är Omega-3 Index?', a: 'Omega-3 Index mäter andelen EPA och DHA i röda blodkroppar. Värden under 4% är förknippade med kraftigt ökad kardiovaskulär risk. Optimalt är 8-12%. Det är ett av de mest validerade kardiovaskulära riskmarkörerna som finns.' },
    { q: 'Vad kostar fettsyreanalys i Sverige?', a: 'Essential & Metabolic Fatty Acids kostar 3 900 kr hos MediBalans. Testkitet skickas hem och blodprovet tas på närmaste provtagningscentral.' },
  ]},

  // ── Fatty Acids EN ────────────────────────────────────────────────────────
  { rel: 'en/fatty-acids/index.html', qas: [
    { q: 'What is an omega-3 test?', a: 'An omega-3 test measures the concentration of omega-3, omega-6, saturated and unsaturated fatty acids in the blood. Essential & Metabolic Fatty Acids from Genova measures 30+ fatty acids and calculates the Omega-3 Index — a powerful marker for cardiovascular risk.' },
    { q: 'Why is the balance between omega-3 and omega-6 important?', a: 'Omega-6 fatty acids (from vegetable oils and processed food) drive inflammation. Omega-3 (from fish and flaxseed oil) suppresses it. Most people in Western countries have an omega-6/omega-3 ratio of 15-20:1 — optimal is 4:1. The imbalance contributes to chronic inflammation, heart disease and autoimmunity.' },
    { q: 'What is the Omega-3 Index?', a: 'The Omega-3 Index measures the proportion of EPA and DHA in red blood cells. Values below 4% are associated with significantly elevated cardiovascular risk. Optimal is 8-12%. It is one of the most validated cardiovascular risk markers available.' },
    { q: 'How much does a fatty acid analysis cost?', a: 'Essential & Metabolic Fatty Acids is priced at SEK 3,900 at MediBalans. The test kit is sent to your home and the blood draw is done at the nearest collection centre.' },
  ]},

  // ── Adrenal Stress SV ─────────────────────────────────────────────────────
  { rel: 'adrenal-stress/index.html', qas: [
    { q: 'Vad visar ett kortisol test?', a: 'Ett salivbaserat kortisoltest mäter dygnsrytmen för kortisol — kroppens primära stresshormon. Normalt är kortisol högt på morgonen och sjunker under dagen. Vid utmattning och HPA-axeldysregulation störs detta mönster, vilket ger lågt morgonkortisol, plattkurva eller omvänt mönster.' },
    { q: 'Vad är skillnaden mellan salivkortisol och blodkortisol?', a: 'Blodkortisol mäter ett ögonblicksvärde och speglar total kortisol inklusive proteinbundet. Salivkortisol mäter fritt, biologiskt aktivt kortisol vid fyra tidpunkter under dagen — vilket ger en kliniskt meningsfull bild av HPA-axelns funktion och dygnsrytm.' },
    { q: 'Vad är DHEA och varför mäts det tillsammans med kortisol?', a: 'DHEA är ett anabolt hormon från binjurarna som motverkar kortisolets katabola effekter. DHEA/kortisol-kvoten är en markör för binjurereserv och biologisk åldrande. Lågt DHEA vid utmattning indikerar utarmad binjurefunktion.' },
    { q: 'Vad kostar Adrenal Stress Profile i Sverige?', a: 'Adrenal Stress Profile kostar 2 100 kr hos MediBalans. Saliven samlas hemma vid fyra tidpunkter under en dag med det medföljande salivkitet.' },
  ]},

  // ── Adrenal Stress EN ─────────────────────────────────────────────────────
  { rel: 'en/adrenal-stress/index.html', qas: [
    { q: 'What does a cortisol test show?', a: 'A saliva-based cortisol test measures the diurnal rhythm of cortisol — the body\'s primary stress hormone. Normally cortisol is high in the morning and declines through the day. In burnout and HPA-axis dysregulation this pattern is disrupted, showing low morning cortisol, a flat curve or an inverted pattern.' },
    { q: 'What is the difference between saliva cortisol and blood cortisol?', a: 'Blood cortisol measures a single point-in-time value and reflects total cortisol including protein-bound fraction. Saliva cortisol measures free, biologically active cortisol at four time points across the day — giving a clinically meaningful picture of HPA-axis function and diurnal rhythm.' },
    { q: 'What is DHEA and why is it measured alongside cortisol?', a: 'DHEA is an anabolic hormone from the adrenal glands that counteracts the catabolic effects of cortisol. The DHEA/cortisol ratio is a marker of adrenal reserve and biological ageing. Low DHEA in the context of fatigue indicates depleted adrenal function.' },
    { q: 'How much does Adrenal Stress Profile cost?', a: 'Adrenal Stress Profile is priced at SEK 2,100 at MediBalans. Saliva is collected at home at four time points during one day using the included saliva kit.' },
  ]},

  // ── Essential Östrogen SV ─────────────────────────────────────────────────
  { rel: 'essential-ostrogen/index.html', qas: [
    { q: 'Vad mäter Essential Estrogens testet?', a: 'Essential Estrogens™ FMV mäter östrogen och dess metaboliter i urinen — hur östrogen faktiskt bryts ned i kroppen via fas 1 och fas 2 avgiftning. Det inkluderar skyddande 2-OH metaboliter och potentiellt skadliga 4-OH och 16-OH metaboliter, samt methyleringsaktivitet via COMT-enzymet.' },
    { q: 'Varför är östrogenmetabolism viktig för cancerrisken?', a: 'Östrogen metaboliseras via flera vägar. 2-OH metaboliter är skyddande och associerade med minskad cancerrisk. 4-OH metaboliter kan skada DNA och är förknippade med ökad risk för hormonrelaterade cancerformer. Förhållandet 2-OH/16-OH (kvoten) är en etablerad markör för bröstcancerrisk.' },
    { q: 'Vem behöver Essential Estrogens?', a: 'Testet är relevant för kvinnor med PMS, endometrios, klimakteriebesvär, familjehistorik av hormonrelaterad cancer, eller de som tar hormonbehandling (HRT). Det är också indicerat vid COMT-genvarianter (påverkar methylering av östrogen).' },
    { q: 'Vad kostar Essential Estrogens test i Sverige?', a: 'Essential Estrogens™ FMV kostar 6 800 kr hos MediBalans. Testkitet skickas hem och provet är ett urinprov (FMV — first morning void).' },
  ]},

  // ── Essential Estrogens EN ────────────────────────────────────────────────
  { rel: 'en/essential-estrogens/index.html', qas: [
    { q: 'What does the Essential Estrogens test measure?', a: 'Essential Estrogens™ FMV measures oestrogen and its metabolites in urine — how oestrogen is actually broken down in the body via phase 1 and phase 2 detoxification. It includes protective 2-OH metabolites and potentially harmful 4-OH and 16-OH metabolites, as well as methylation activity via the COMT enzyme.' },
    { q: 'Why is oestrogen metabolism important for cancer risk?', a: 'Oestrogen is metabolised via several pathways. 2-OH metabolites are protective and associated with reduced cancer risk. 4-OH metabolites can damage DNA and are linked to increased risk of hormone-related cancers. The 2-OH/16-OH ratio is an established marker for breast cancer risk.' },
    { q: 'Who needs Essential Estrogens?', a: 'The test is relevant for women with PMS, endometriosis, menopausal symptoms, a family history of hormone-related cancers, or those taking hormone replacement therapy (HRT). It is also indicated when COMT gene variants are present (affecting oestrogen methylation).' },
    { q: 'How much does an Essential Estrogens test cost?', a: 'Essential Estrogens™ FMV is priced at SEK 6,800 at MediBalans. The test kit is sent to your home and the sample is a first-morning urine collection (FMV).' },
  ]},

  // ── Menopaus Plus SV ──────────────────────────────────────────────────────
  { rel: 'menopaus-plus/index.html', qas: [
    { q: 'Vad mäter Menopause Plus testet?', a: 'Menopause Plus™ mäter könshormoner (estradiol, estron, estriol, progesteron, testosteron), östrogenmetabolism, melatonin och kortisol i saliv och urin. Det är designat för peri- och postmenopausala kvinnor och ger en komplett bild av den hormonella förändringen.' },
    { q: 'Vad är skillnaden mellan Menopause Plus och ett vanligt hormontest?', a: 'Standardblodprover mäter FSH och E2 — två markörer. Menopause Plus mäter 6 hormoner, P/E2-kvoten, melatonin (för sömnproblem) och kortisol (för stresskomponenten i klimakteriet). Det inkluderar också östrogenmetabolism som är avgörande för att bedöma risken för hormonbehandling.' },
    { q: 'Kan Menopause Plus hjälpa vid sömnproblem under klimakteriet?', a: 'Ja. Menopause Plus inkluderar en melatoninprofil (uppmätt vid tre tidpunkter) som identifierar störd dygnsrytm — en vanlig men ofta förbisedd orsak till sömnproblem under klimakteriet.' },
    { q: 'Vad kostar Menopause Plus i Sverige?', a: 'Menopause Plus™ kostar 9 300 kr hos MediBalans, Sveriges officiella Genova-distributör. Provet samlas hemma (saliv och urin).' },
  ]},

  // ── Menopause Plus EN ─────────────────────────────────────────────────────
  { rel: 'en/menopause-plus/index.html', qas: [
    { q: 'What does the Menopause Plus test measure?', a: 'Menopause Plus™ measures sex hormones (oestradiol, oestrone, oestriol, progesterone, testosterone), oestrogen metabolism, melatonin and cortisol in saliva and urine. It is designed for peri- and post-menopausal women and provides a complete picture of the hormonal transition.' },
    { q: 'What is the difference between Menopause Plus and a standard hormone test?', a: 'Standard blood tests measure FSH and E2 — two markers. Menopause Plus measures 6 hormones, the P/E2 ratio, melatonin (for sleep disturbance) and cortisol (for the stress component of menopause). It also includes oestrogen metabolism, which is critical for assessing the risk profile of hormone therapy.' },
    { q: 'Can Menopause Plus help with sleep problems during menopause?', a: 'Yes. Menopause Plus includes a melatonin profile (measured at three time points) that identifies disrupted circadian rhythm — a common but frequently overlooked cause of sleep problems during menopause.' },
    { q: 'How much does Menopause Plus cost?', a: 'Menopause Plus™ is priced at SEK 9,300 at MediBalans, the official Swedish Genova distributor. Samples are collected at home (saliva and urine).' },
  ]},

  // ── Metabolomik SV ────────────────────────────────────────────────────────
  { rel: 'metabolomik/index.html', qas: [
    { q: 'Vad är ett metabolomik test?', a: 'Metabolomix+ är ett urinbaserat näringsstatus test som mäter organiska syror, aminosyror, fettsyror och antioxidanter. Det ger en funktionell bild av hur kroppen använder näring på cellnivå — utan blodprov.' },
    { q: 'Vad är skillnaden mellan Metabolomix+ och NutrEval?', a: 'Metabolomix+ är urinbaserat och mäter 125+ biomarkörer via urin med möjlighet till tillval av blodspot. NutrEval kombinerar blod och urin för en ännu bredare bild inkluderande fettsyror i blod. Metabolomix+ är det bästa valet för de som vill undvika blodprov.' },
    { q: 'Hur tar man Metabolomix+ provet?', a: 'Metabolomix+ är ett hemtest. Du samlar första morgonurin i den medföljande behållaren och skickar provet direkt till Genovas laboratorium. Inga klinikbesök krävs.' },
    { q: 'Vad kostar Metabolomix+ test i Sverige?', a: 'Metabolomix+ kostar 8 100 kr hos MediBalans. Tillval Bloodspot (fettsyror i blod) kostar ytterligare 1 800 kr.' },
  ]},

  // ── Metabolomics EN ───────────────────────────────────────────────────────
  { rel: 'en/metabolomics/index.html', qas: [
    { q: 'What is a metabolomics test?', a: 'Metabolomix+ is a urine-based nutritional status test that measures organic acids, amino acids, fatty acids and antioxidants. It provides a functional picture of how the body uses nutrients at the cellular level — without a blood draw.' },
    { q: 'What is the difference between Metabolomix+ and NutrEval?', a: 'Metabolomix+ is urine-based and measures 125+ biomarkers via urine with an optional bloodspot add-on. NutrEval combines blood and urine for an even broader picture including blood fatty acids. Metabolomix+ is the best choice for those who prefer to avoid a blood draw.' },
    { q: 'How do you collect the Metabolomix+ sample?', a: 'Metabolomix+ is a home test. You collect first-morning urine in the included container and send the sample directly to the Genova laboratory. No clinic visit is required.' },
    { q: 'How much does Metabolomix+ cost?', a: 'Metabolomix+ is priced at SEK 8,100 at MediBalans. The optional Bloodspot add-on (blood fatty acids) costs an additional SEK 1,800.' },
  ]},

  // ── Genova Hormontest SV ──────────────────────────────────────────────────
  { rel: 'genova-hormontest/index.html', qas: [
    { q: 'Vilka hormontest erbjuder Genova Diagnostics?', a: "MediBalans erbjuder via Genova: Women's Health+ (könshormoner, kortisol, östrogenmetabolism), Essential Estrogens™ (östrogenmetabolism), Menopause Plus™ (komplett menopausutredning) och Adrenal Stress Profile (kortisol/DHEA). Alla test kan tas hemma via saliv eller urinprov." },
    { q: 'Vilket hormontest passar mig?', a: "Women's Health+ passar för en bred hormonöversikt vid PMS, oregelbunden mens eller hormonella besvär. Essential Estrogens passar vid oro för hormonrelaterade sjukdomar eller vid utvärdering av HRT. Menopause Plus passar specifikt vid klimakteriebesvär. Adrenal Stress Profile passar vid utmattning och sömnproblem." },
    { q: 'Är salivhormoner lika tillförlitliga som blodprover?', a: 'För kortisol och könshormoner är salivprover kliniskt validerade och mäter fritt, biologiskt aktivt hormon — vilket ofta är mer kliniskt relevant än totalt hormon i blod. Genova Diagnostics är ett av världens ledande laboratorier för salivbaserad hormonanalys.' },
  ]},

  // ── Genova Hormones EN ────────────────────────────────────────────────────
  { rel: 'en/genova-hormones/index.html', qas: [
    { q: 'Which hormone tests does Genova Diagnostics offer?', a: "MediBalans offers via Genova: Women's Health+ (sex hormones, cortisol, oestrogen metabolism), Essential Estrogens™ (oestrogen metabolism), Menopause Plus™ (comprehensive menopause assessment) and Adrenal Stress Profile (cortisol/DHEA). All tests can be collected at home via saliva or urine." },
    { q: 'Which hormone test is right for me?', a: "Women's Health+ is suited for a broad hormonal overview in PMS, irregular cycles or hormonal symptoms. Essential Estrogens is suited when there are concerns about hormone-related disease or when evaluating HRT. Menopause Plus is specifically designed for menopausal symptoms. Adrenal Stress Profile is suited for fatigue and sleep problems." },
    { q: 'Are saliva hormones as reliable as blood tests?', a: 'For cortisol and sex hormones, saliva testing is clinically validated and measures free, biologically active hormone — which is often more clinically relevant than total hormone in blood. Genova Diagnostics is one of the world\'s leading laboratories for saliva-based hormone analysis.' },
  ]},

  // ── Genova Diagnostics SV ─────────────────────────────────────────────────
  { rel: 'genova-diagnostics/index.html', qas: [
    { q: 'Vad är Genova Diagnostics?', a: 'Genova Diagnostics är ett CLIA-certifierat speciallaboratorium i Asheville, North Carolina, grundat 1986. Det är ett av världens ledande laboratorier inom funktionsmedicin och erbjuder avancerade diagnostiska tester för tarmhälsa, näringsstatus, hormonbalans och genetik.' },
    { q: 'Varför är Genova Diagnostics bättre än andra laboratorier?', a: 'Genova kombinerar flera analysmetoder (PCR, MALDI-TOF, LC-MS/MS, odling) för klinisk precision som saknar motstycke bland konsumentbaserade tester. Testerna är peer-reviewed validerade och används av funktionsmedicinska läkare världen över.' },
    { q: 'Var kan man beställa Genova-tester i Sverige?', a: 'MediBalans AB är officiell svensk distributör av Genova Diagnostics. Vi är det enda sättet att beställa äkta Genova-tester i Sverige med klinisk tolkning av legitimerad läkare.' },
    { q: 'Behöver man läkarremiss för Genova-tester?', a: 'Nej. Via MediBalans kan du beställa Genova-tester direkt utan remiss. En initial konsultation rekommenderas för att säkerställa att rätt tester väljs baserat på dina symtom.' },
  ]},

  // ── Genova Diagnostics EN ─────────────────────────────────────────────────
  { rel: 'en/genova-diagnostics/index.html', qas: [
    { q: 'What is Genova Diagnostics?', a: 'Genova Diagnostics is a CLIA-certified specialty laboratory in Asheville, North Carolina, founded in 1986. It is one of the world\'s leading laboratories in functional medicine, offering advanced diagnostic testing for gut health, nutritional status, hormone balance and genetics.' },
    { q: 'Why is Genova Diagnostics superior to other laboratories?', a: 'Genova combines multiple analytical methods (PCR, MALDI-TOF, LC-MS/MS, culture) for clinical precision unmatched by consumer-grade tests. The tests are peer-reviewed validated and used by functional medicine physicians worldwide.' },
    { q: 'Where can you order Genova tests in Sweden?', a: 'MediBalans AB is the official Swedish distributor of Genova Diagnostics. We are the only way to order genuine Genova tests in Sweden with clinical interpretation by a licensed physician.' },
    { q: 'Do you need a doctor\'s referral for Genova tests?', a: 'No. Through MediBalans you can order Genova tests directly without a referral. An initial consultation is recommended to ensure the right tests are selected based on your symptoms.' },
  ]},

];

// ─── APPLY ───────────────────────────────────────────────────────────────────

let updated = 0, skipped = 0, missing = 0;

for (const { rel, qas } of PAGES) {
  try {
    read(rel);
  } catch {
    console.log(`  MISSING  ${rel}`);
    missing++;
    continue;
  }

  const faqJson = makeFAQ(qas);
  const changed = applyFAQ(rel, faqJson);
  if (changed) {
    console.log(`  updated  ${rel}  (${qas.length} Q&As)`);
    updated++;
  } else {
    console.log(`  WARN: no change  ${rel}`);
    skipped++;
  }
}

console.log(`\n══ DONE: ${updated} updated · ${skipped} no-change · ${missing} missing ══`);
