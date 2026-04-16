#!/usr/bin/env node
// add_faq_schema.mjs — replace or add FAQPage JSON-LD schema on specified pages

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
    // No existing FAQPage — insert after the last ld+json block, before </head>
    const lastJsonLd = c.lastIndexOf('</script>');
    // Find the last ld+json closing script tag
    let insertPos = -1;
    let searchFrom = 0;
    let m;
    const jsonLdRx = /<\/script>/g;
    // Walk all </script> tags and find the last one that closes a ld+json block
    const allJsonLd = [...c.matchAll(/<script\s+type="application\/ld\+json">/g)];
    if (allJsonLd.length > 0) {
      const lastStart = allJsonLd[allJsonLd.length - 1].index;
      const closeIdx = c.indexOf('</script>', lastStart);
      if (closeIdx !== -1) insertPos = closeIdx + '</script>'.length;
    }
    if (insertPos !== -1) {
      c = c.slice(0, insertPos) + '\n' + replacement + c.slice(insertPos);
    } else {
      // Fallback: insert before </head>
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

  // ── GI Effects SV ─────────────────────────────────────────────────────────
  { rel: 'gi-effects-test/index.html', qas: [
    { q: 'Vad är ett mikrobiom test?', a: 'Ett mikrobiomtest analyserar sammansättningen och funktionen av bakterier, svampar och parasiter i tarmen. GI Effects® från Genova Diagnostics använder PCR-teknik, MALDI-TOF och odling — tre metoder kombinerade — för att ge en kliniskt handlingsbar bild av tarmhälsan.' },
    { q: 'Vad är skillnaden mellan GI Effects och vanliga mikrobiomtester som GetTested eller KÄLLA?', a: 'GI Effects använder klinisk laboratoriemetodik (PCR + MALDI-TOF + odling) i ett CLIA-certifierat laboratorium. Konsumentbaserade tester som GetTested och KÄLLA använder 16S rRNA-sekvensering — en billigare teknik som identifierar bakterietyper men inte mäter inflammation, matsmältning, parasiter eller kortkedjade fettsyror. GI Effects mäter 6 kliniska domäner; konsumenttest mäter typiskt 1-2.' },
    { q: 'Är GI Effects tillgängligt i Sverige?', a: 'Ja. MediBalans AB är officiell svensk distributör av Genova Diagnostics. GI Effects kan beställas direkt på medibalans.com med hemleverans av testkitet till hela Sverige.' },
    { q: 'Hur tar man ett GI Effects prov?', a: 'Testkitet skickas hem till dig. Du samlar ett avföringsprov hemma enligt medföljande instruktioner och skickar det direkt till Genovas laboratorium med det förbetalda returkuvertet. Inga klinikbesök krävs för provtagningen.' },
    { q: 'Hur lång tid tar det att få svar på ett GI Effects test?', a: 'Svarstiden är normalt 14-21 arbetsdagar från det att laboratoriet mottagit provet.' },
    { q: 'Vad kostar ett GI Effects tarmtest?', a: 'GI Effects® Comprehensive kostar 8 500 kr hos MediBalans, vilket inkluderar testkitet, laboratorieanalys och klinisk tolkning av läkare. Priset speglar den kliniska kvaliteten — PCR-metodiken är 10-15 gånger känsligare än konsumentbaserade 16S-tester.' },
  ]},

  // ── GI Effects EN ─────────────────────────────────────────────────────────
  { rel: 'en/gi-effects-test/index.html', qas: [
    { q: 'What is a microbiome test?', a: 'A microbiome test analyses the composition and function of bacteria, fungi and parasites in the gut. GI Effects® from Genova Diagnostics combines PCR technology, MALDI-TOF mass spectrometry and culture methods — three techniques in one panel — to deliver a clinically actionable picture of gut health.' },
    { q: 'What is the difference between GI Effects and consumer microbiome tests like Thryve or Viome?', a: 'GI Effects uses clinical laboratory methodology (PCR + MALDI-TOF + culture) in a CLIA-certified laboratory. Consumer tests use 16S rRNA sequencing — a cheaper technique that identifies bacterial types but does not measure inflammation, digestion, parasites or short-chain fatty acids. GI Effects covers 6 clinical domains; consumer tests typically cover 1-2.' },
    { q: 'Is GI Effects available outside the US?', a: 'Yes. MediBalans AB is the official Swedish distributor of Genova Diagnostics. GI Effects can be ordered directly at medibalans.com with home delivery of the test kit across Sweden and the EU.' },
    { q: 'How do you collect a GI Effects sample?', a: 'The test kit is sent to your home address. You collect a stool sample following the included instructions and send it directly to the Genova laboratory using the prepaid return envelope. No clinic visit is required for sample collection.' },
    { q: 'How long does GI Effects take?', a: 'Turnaround time is typically 14-21 business days from the date the laboratory receives the sample.' },
    { q: 'How much does a GI Effects test cost?', a: 'GI Effects® Comprehensive is priced at SEK 8,500 at MediBalans, including the test kit, laboratory analysis and physician interpretation. The price reflects the clinical quality — PCR methodology is 10-15× more sensitive than consumer-grade 16S testing.' },
  ]},

  // ── NutrEval SV ───────────────────────────────────────────────────────────
  { rel: 'nutreval-sverige/index.html', qas: [
    { q: 'Vad är ett näringsbrist test?', a: 'Ett näringsbristtest mäter om din kropp har tillräckliga nivåer av vitaminer, mineraler, aminosyror och fettsyror för optimal funktion. NutrEval® från Genova Diagnostics mäter över 125 biomarkörer i blod och urin och identifierar funktionella brister — inte bara om nivåerna är "normala" utan om cellerna faktiskt kan använda näringen.' },
    { q: 'Vad är skillnaden mellan NutrEval och ett vanligt blodprov?', a: 'Standardblodprover mäter cirkulerande nivåer av enstaka vitaminer. NutrEval mäter funktionell näringsstatus — hur väl cellerna faktiskt använder näringen — via organiska syror, aminosyror, fettsyror och antioxidantmarkörer. Det identifierar brister som är osynliga i vanliga blodprover.' },
    { q: 'Vem behöver ett näringsbrist test?', a: 'NutrEval är relevant vid kronisk trötthet, hjärndimma, muskelsvaghet, humörsvängningar, återkommande infektioner eller när standardprover inte ger svar. Det är också indicerat vid autoimmunitet, ADHD, utmattningssyndrom och för personer som äter restriktivt.' },
    { q: 'Hur tar man NutrEval provet?', a: 'NutrEval kräver ett blodprov (fastande) och ett urinprov (morgonurin). Testkitet skickas hem med instruktioner. Blodprovet tas hos MediBalans eller närmaste provtagningscentral.' },
    { q: 'Vad kostar NutrEval i Sverige?', a: 'NutrEval® FMV kostar 12 200 kr hos MediBalans, Sveriges officiella Genova-distributör. Priset inkluderar testkitet, laboratorieanalys av 125+ biomarkörer och läkartolkning.' },
  ]},

  // ── NutrEval EN ───────────────────────────────────────────────────────────
  { rel: 'en/nutreval-test/index.html', qas: [
    { q: 'What is a nutritional deficiency test?', a: 'A nutritional deficiency test measures whether your body has adequate levels of vitamins, minerals, amino acids and fatty acids for optimal function. NutrEval® from Genova Diagnostics measures over 125 biomarkers in blood and urine, identifying functional deficiencies — not just whether levels appear "normal" but whether cells can actually utilise the nutrients.' },
    { q: 'What is the difference between NutrEval and a standard blood panel?', a: 'Standard blood tests measure circulating levels of individual vitamins. NutrEval measures functional nutritional status — how well cells actually use nutrients — via organic acids, amino acids, fatty acids and antioxidant markers. It identifies deficiencies that are invisible in routine blood work.' },
    { q: 'Who needs a nutritional deficiency test?', a: 'NutrEval is relevant for chronic fatigue, brain fog, muscle weakness, mood swings, recurrent infections, or when standard tests return no answers. It is also indicated in autoimmunity, ADHD, burnout syndrome and restrictive diets.' },
    { q: 'How do you collect the NutrEval sample?', a: 'NutrEval requires a fasting blood draw and a first-morning urine sample. The test kit is shipped to your home with instructions. The blood draw is done at MediBalans or the nearest collection centre.' },
    { q: 'How much does NutrEval cost in Sweden?', a: 'NutrEval® FMV is priced at SEK 12,200 at MediBalans, the official Swedish Genova distributor. The price includes the test kit, laboratory analysis of 125+ biomarkers and physician interpretation.' },
  ]},

  // ── SIBO SV ───────────────────────────────────────────────────────────────
  { rel: 'sibo-test/index.html', qas: [
    { q: 'Vad är SIBO?', a: 'SIBO (Small Intestinal Bacterial Overgrowth) innebär att det finns för mycket bakterier i tunntarmen. Dessa bakterier fermenterar kolhydrater och producerar vätgas och metan, vilket orsakar uppblåsthet, gaser, diarré, förstoppning och buksmärtor. SIBO är en vanlig underliggande orsak till IBS.' },
    { q: 'Hur diagnostiseras SIBO?', a: 'SIBO diagnostiseras med ett andningstest där du dricker en lösning av lactulose och sedan andas i påsar var 20:e minut under 2-3 timmar. Förhöjda nivåer av vätgas eller metan i utandningsluften indikerar bakterieöverväxt i tunntarmen.' },
    { q: 'Kan man ha SIBO utan att veta om det?', a: 'Ja. Många med SIBO har fått diagnosen IBS utan att den underliggande orsaken identifierats. Symtom som uppblåsthet direkt efter måltid, gaser och omväxlande avföringsvanor är klassiska tecken. Standardblodprover och gastroskopi/koloskopi missar SIBO.' },
    { q: 'Vad är skillnaden mellan ett 2-timmars och 3-timmars SIBO test?', a: '3-timmars testet är mer komplett och rekommenderas för patienter med förstoppning eller långsam tarmpassage. Det kan också identifiera vätesulfid-producerande bakterier som syns som en plan kurva i de sista mätningarna.' },
    { q: 'Vad kostar SIBO-test i Sverige?', a: 'SIBO-testet kostar 3 700 kr hos MediBalans. Testkitet skickas hem och provet tas på morgonen efter 12 timmars fasta.' },
  ]},

  // ── SIBO EN ───────────────────────────────────────────────────────────────
  { rel: 'en/sibo-test/index.html', qas: [
    { q: 'What is SIBO?', a: 'SIBO (Small Intestinal Bacterial Overgrowth) means there are too many bacteria in the small intestine. These bacteria ferment carbohydrates and produce hydrogen and methane gas, causing bloating, flatulence, diarrhoea, constipation and abdominal pain. SIBO is a common underlying cause of IBS.' },
    { q: 'How is SIBO diagnosed?', a: 'SIBO is diagnosed with a breath test. You drink a lactulose solution and breathe into collection tubes every 20 minutes for 2-3 hours. Elevated levels of hydrogen or methane in the exhaled breath indicate bacterial overgrowth in the small intestine.' },
    { q: 'Can you have SIBO without knowing it?', a: 'Yes. Many people with SIBO have been given an IBS diagnosis without the underlying cause being identified. Bloating immediately after meals, gas and alternating bowel habits are classic signs. Standard blood tests and endoscopy/colonoscopy miss SIBO.' },
    { q: 'What is the difference between a 2-hour and 3-hour SIBO test?', a: 'The 3-hour test is more complete and is recommended for patients with constipation or slow intestinal transit. It can also identify hydrogen sulphide-producing bacteria, which appear as a flat curve in the final readings.' },
    { q: 'How much does a SIBO test cost?', a: 'The SIBO breath test is priced at SEK 3,700 at MediBalans. The test kit is sent to your home and the test is performed in the morning after a 12-hour fast.' },
  ]},

  // ── ALCAT SV ──────────────────────────────────────────────────────────────
  { rel: 'alcat/index.html', qas: [
    { q: 'Vad är skillnaden mellan matintolerans och matallergi?', a: 'Matallergi är en IgE-medierad immunreaktion som ger omedelbara symtom (inom minuter). Matintolerans är en försenad immunreaktion (IgG/IgA eller cellulär) som kan ge symtom 24-72 timmar efter intag — vilket gör det extremt svårt att identifiera utan test. ALCAT mäter den cellulära immunreaktionen, inte IgG-antikroppar.' },
    { q: 'Vad mäter ALCAT-testet?', a: 'ALCAT (Antigen Leukocyte Cellular Antibody Test) mäter hur dina vita blodkroppar (leukocyter) reagerar på specifika livsmedel, tillsatser och kemikalier. En reaktion indikerar att livsmedlet triggar inflammation — oavsett om det är IgE, IgG eller cellulär mekanism.' },
    { q: 'Är matintoleranstest med IgG-antikroppar lika bra som ALCAT?', a: 'Nej. IgG-tester mäter bara en typ av immunreaktion och har begränsad klinisk validering. ALCAT mäter den direkta cellulära reaktionen och har stöd i peer-reviewed forskning för symtomlindring vid IBS, migrän, eksem och kronisk trötthet.' },
    { q: 'Hur många livsmedel testar ALCAT?', a: 'MediBalans erbjuder ALCAT 250 — som testar reaktivitet mot 250 livsmedel, kryddor, tillsatser och kemikalier. Detta ger en heltäckande bild av immunreaktiviteten.' },
    { q: 'Vad kostar ALCAT-test i Sverige?', a: 'ALCAT 250 ingår i MediBalans diagnostikpaket. Kontakta kliniken för aktuell prissättning.' },
  ]},

  // ── ALCAT EN ──────────────────────────────────────────────────────────────
  { rel: 'en/alcat-test/index.html', qas: [
    { q: 'What is the difference between food intolerance and food allergy?', a: 'Food allergy is an IgE-mediated immune reaction causing immediate symptoms (within minutes). Food intolerance is a delayed immune reaction (IgG/IgA or cellular) that can trigger symptoms 24-72 hours after ingestion — making it extremely difficult to identify without testing. ALCAT measures the cellular immune response, not IgG antibodies.' },
    { q: 'What does the ALCAT test measure?', a: 'ALCAT (Antigen Leukocyte Cellular Antibody Test) measures how your white blood cells (leukocytes) react to specific foods, additives and chemicals. A reaction indicates that the food item triggers inflammation — regardless of whether the mechanism is IgE, IgG or cellular.' },
    { q: 'Are IgG food intolerance tests as accurate as ALCAT?', a: 'No. IgG tests measure only one type of immune reaction and have limited clinical validation. ALCAT measures the direct cellular response and is supported by peer-reviewed research demonstrating symptom relief in IBS, migraine, eczema and chronic fatigue.' },
    { q: 'How many foods does ALCAT test?', a: 'MediBalans offers ALCAT 250 — testing reactivity against 250 foods, spices, additives and chemicals. This provides a comprehensive picture of immune reactivity.' },
    { q: 'How much does an ALCAT food intolerance test cost?', a: 'ALCAT 250 is included in MediBalans diagnostic packages. Contact the clinic for current pricing.' },
  ]},

  // ── CMA SV ────────────────────────────────────────────────────────────────
  { rel: 'cma/index.html', qas: [
    { q: 'Vad är intracellulär näring?', a: 'Intracellulär näring mäter koncentrationen av vitaminer och mineraler inuti cellerna — inte bara i blodet. En person kan ha normala blodnivåer av magnesium men ändå ha intracellulär brist, vilket påverkar energiproduktion, muskelfunktion och hundratals enzymatiska processer.' },
    { q: 'Vad är skillnaden mellan CMA och vanliga blodprover för vitaminer?', a: 'Vanliga blodprover mäter cirkulerande nivåer i serum. CMA (Cellular Micronutrient Analysis) mäter vad som faktiskt finns inne i cellerna — vilket är det kliniskt relevanta måttet. Studier visar att intracellulära brister kan existera trots normala serumvärden.' },
    { q: 'Vilka brister hittar CMA som vanliga prover missar?', a: 'CMA identifierar ofta brister på magnesium, zink, B-vitaminer, CoQ10, antioxidanter och essentiella aminosyror som är osynliga i standardblodprover. Dessa brister är vanliga vid kronisk trötthet, fibromyalgi, autoimmunitet och neurologiska symtom.' },
    { q: 'Vad kostar CMA-test i Sverige?', a: 'CMA ingår i MediBalans diagnostikpaket och utförs via Cell Science Systems. Kontakta kliniken för prissättning.' },
  ]},

  // ── CMA EN ────────────────────────────────────────────────────────────────
  { rel: 'en/cellular-nutrient-analysis/index.html', qas: [
    { q: 'What is intracellular nutrition?', a: 'Intracellular nutrition measures the concentration of vitamins and minerals inside cells — not just in the bloodstream. A person can have normal blood levels of magnesium but still have an intracellular deficiency that impairs energy production, muscle function and hundreds of enzymatic processes.' },
    { q: 'What is the difference between CMA and standard vitamin blood tests?', a: 'Standard blood tests measure circulating levels in serum. CMA (Cellular Micronutrient Analysis) measures what is actually present inside cells — which is the clinically relevant measurement. Studies show that intracellular deficiencies can exist despite normal serum values.' },
    { q: 'Which deficiencies does CMA find that standard tests miss?', a: 'CMA frequently identifies deficiencies in magnesium, zinc, B-vitamins, CoQ10, antioxidants and essential amino acids that are invisible in standard blood panels. These deficiencies are common in chronic fatigue, fibromyalgia, autoimmunity and neurological symptoms.' },
    { q: 'How much does a CMA test cost?', a: 'CMA is included in MediBalans diagnostic packages and is performed via Cell Science Systems. Contact the clinic for pricing.' },
  ]},

  // ── MethylDetox SV ────────────────────────────────────────────────────────
  { rel: 'methyldetox/index.html', qas: [
    { q: 'Vad är ett metyleringstest?', a: 'Ett metyleringstest analyserar genetiska varianter i de enzymer som styr methyleringsprocesserna i kroppen. Methylering är en fundamental biokemisk process som påverkar DNA-reparation, neurotransmittorproduktion, avgiftning och hormonbalans.' },
    { q: 'Vad är MTHFR och varför är det viktigt?', a: 'MTHFR (metylentetrahydrofolat reduktas) är ett enzym som omvandlar folsyra till aktiv metylfolat. Varianter i MTHFR-genen (rs1801133, rs1801131) kan reducera enzymaktiviteten med 30-70%, vilket påverkar homocysteinnivåer, B12-metabolism och risk för kardiovaskulär sjukdom.' },
    { q: 'Hur många gener analyserar MethylDetox?', a: 'MethylDetox analyserar 38 genetiska varianter i methyleringsrelaterade gener inklusive MTHFR, COMT, MTR, MTRR, CBS och VDR.' },
    { q: 'Vad kostar metyleringstest i Sverige?', a: 'MethylDetox ingår i MediBalans genetiska utredningspaket. Kontakta kliniken för prissättning.' },
  ]},

  // ── MethylDetox EN ────────────────────────────────────────────────────────
  { rel: 'en/methylation-test/index.html', qas: [
    { q: 'What is a methylation test?', a: 'A methylation test analyses genetic variants in the enzymes that regulate methylation processes in the body. Methylation is a fundamental biochemical process that affects DNA repair, neurotransmitter production, detoxification and hormone balance.' },
    { q: 'What is MTHFR and why does it matter?', a: 'MTHFR (methylenetetrahydrofolate reductase) is an enzyme that converts folic acid into active methylfolate. Variants in the MTHFR gene (rs1801133, rs1801131) can reduce enzyme activity by 30-70%, affecting homocysteine levels, B12 metabolism and cardiovascular risk.' },
    { q: 'How many genes does MethylDetox analyse?', a: 'MethylDetox analyses 38 genetic variants in methylation-related genes including MTHFR, COMT, MTR, MTRR, CBS and VDR.' },
    { q: 'How much does a methylation test cost?', a: 'MethylDetox is included in MediBalans genetic assessment packages. Contact the clinic for pricing.' },
  ]},

  // ── IBS Tarmhälsa SV ──────────────────────────────────────────────────────
  { rel: 'ibs-tarmhalsa/index.html', qas: [
    { q: 'Varför fortsätter IBS trots diet och behandling?', a: 'IBS utan känd orsak är sällan slumpmässigt. De vanligaste underliggande drivkrafterna är SIBO (bakterieöverväxt i tunntarmen), matimmunreaktivitet (ALCAT), dysbiosis (obalans i tarmfloran) och intracellulär näringsbrist — ingen av dessa identifieras med standardutredning.' },
    { q: 'Vad är skillnaden mellan IBS-utredning på MediBalans och på en vanlig vårdcentral?', a: 'Standardvård utesluter allvarlig sjukdom (koloskopi, blodprover) men identifierar sällan orsaken. MediBalans mäter direkt: tarmflora (GI Effects), bakterieöverväxt (SIBO-test), matimmunreaktivitet (ALCAT) och intracellulär näring (CMA) — och tolkar resultaten tillsammans.' },
    { q: 'Kan man ha IBS och SIBO samtidigt?', a: 'Ja. Forskning visar att 30-85% av IBS-patienter har positiva SIBO-test beroende på population och testmetod. SIBO är sannolikt en underliggande orsak till IBS hos en stor andel patienter.' },
    { q: 'Hur lång tid tar en IBS-utredning på MediBalans?', a: 'Den initiala konsultationen är 45 minuter. Laboratorieresultat tar 14-21 dagar. Det totala utredningsförloppet från konsultation till protokoll är typiskt 4-6 veckor.' },
  ]},

  // ── IBS EN ────────────────────────────────────────────────────────────────
  { rel: 'en/ibs-gut-health/index.html', qas: [
    { q: 'Why does IBS persist despite dietary changes and treatment?', a: 'IBS without a known cause is rarely random. The most common underlying drivers are SIBO (small intestinal bacterial overgrowth), food immune reactivity (ALCAT), dysbiosis (gut flora imbalance) and intracellular nutritional deficiency — none of which are identified by standard investigation.' },
    { q: 'What is the difference between an IBS investigation at MediBalans versus a standard GP?', a: 'Standard care rules out serious disease (colonoscopy, blood tests) but rarely identifies the cause. MediBalans measures directly: gut microbiome (GI Effects), bacterial overgrowth (SIBO test), food immune reactivity (ALCAT) and intracellular nutrition (CMA) — and interprets the results together.' },
    { q: 'Can you have IBS and SIBO at the same time?', a: 'Yes. Research shows that 30-85% of IBS patients test positive for SIBO depending on population and testing method. SIBO is likely an underlying cause of IBS in a large proportion of patients.' },
    { q: 'How long does an IBS investigation at MediBalans take?', a: 'The initial consultation is 45 minutes. Laboratory results take 14-21 days. The total investigation timeline from consultation to protocol is typically 4-6 weeks.' },
  ]},

  // ── Utmattning SV ─────────────────────────────────────────────────────────
  { rel: 'utmattning/index.html', qas: [
    { q: 'Vad orsakar utmattningssyndrom?', a: 'Utmattningssyndrom (ME/CFS) har sällan en enskild orsak. Vanliga biologiska drivkrafter inkluderar mitokondriell dysfunktion, intracellulär näringsbrist (särskilt magnesium, CoQ10, B-vitaminer), HPA-axeldysregulation (kortisol/DHEA), kronisk låggradig inflammation och SIBO.' },
    { q: 'Hur utreder MediBalans kronisk trötthet?', a: 'MediBalans kartlägger energimetabolism via CMA (intracellulär näring), NutrEval (125+ biomarkörer), Adrenal Stress Profile (kortisol/DHEA-mönster) och Organix (mitokondriell funktion). Utredningen identifierar specifika biologiska mekanismer — inte bara utesluter sjukdom.' },
    { q: 'Är kronisk trötthet och ME/CFS samma sak?', a: 'ME/CFS (Myalgisk Encefalomyelit/Kroniskt Trötthetssyndrom) är en specifik diagnos med diagnostiska kriterier. Kronisk trötthet är ett symtom med många möjliga orsaker. MediBalans utreder de biologiska mekanismerna oavsett diagnos.' },
  ]},

  // ── Chronic Fatigue EN ────────────────────────────────────────────────────
  { rel: 'en/chronic-fatigue/index.html', qas: [
    { q: 'What causes chronic fatigue syndrome?', a: 'ME/CFS (Myalgic Encephalomyelitis/Chronic Fatigue Syndrome) rarely has a single cause. Common biological drivers include mitochondrial dysfunction, intracellular nutritional deficiency (especially magnesium, CoQ10, B-vitamins), HPA-axis dysregulation (cortisol/DHEA), chronic low-grade inflammation and SIBO.' },
    { q: 'How does MediBalans investigate chronic fatigue?', a: 'MediBalans maps energy metabolism via CMA (intracellular nutrition), NutrEval (125+ biomarkers), Adrenal Stress Profile (cortisol/DHEA patterns) and Organix (mitochondrial function). The investigation identifies specific biological mechanisms — not just rules out disease.' },
    { q: 'Is chronic fatigue the same as ME/CFS?', a: 'ME/CFS (Myalgic Encephalomyelitis/Chronic Fatigue Syndrome) is a specific diagnosis with defined diagnostic criteria. Chronic fatigue is a symptom with many possible causes. MediBalans investigates the biological mechanisms regardless of diagnosis.' },
  ]},

  // ── Autoimmun SV ──────────────────────────────────────────────────────────
  { rel: 'autoimmun/index.html', qas: [
    { q: 'Vad orsakar autoimmunsjukdom?', a: 'Autoimmunsjukdom uppstår när immunsystemet attackerar kroppens egna vävnader. Vanliga biologiska drivkrafter inkluderar tarmdysbiosis och ökad tarmpermeabilitet ("läckande tarm"), matimmunreaktivitet, virusinfektioner (molekylär mimikry), tungmetallbelastning och genetisk predisposition.' },
    { q: 'Kan autoimmunitet gå i remission?', a: 'Fullständig remission är möjlig vid vissa autoimmuntillstånd. MediBalans fokuserar på att identifiera och eliminera de biologiska drivkrafterna — matimmunreaktivitet (ALCAT), tarmdysbiosis (GI Effects), intracellulär näringsbrist (CMA) och methyleringsrubbning (MethylDetox) — som underhåller immunaktiveringen.' },
    { q: 'Vad är kopplingen mellan tarmhälsa och autoimmunitet?', a: 'Tarmpermeabilitet (läckande tarm) tillåter obearbetade peptider att passera tarmbarriären och aktivera systemisk immunreaktion. Specifika bakteriemönster (Klebsiella, Proteus) är kopplade till reumatoid artrit och ankyloserande spondylit. GI Effects kartlägger dessa mönster direkt.' },
    { q: 'Hur utreder MediBalans autoimmunitet?', a: 'MediBalans utredning inkluderar ALCAT (matimmunreaktivitet), GI Effects (tarmflora och barriärfunktion), CMA (intracellulär näring), MethylDetox (MTHFR och genetisk risk) och vid behov NutrEval (metabolomisk profil). Resultaten tolkas i ett integrerat kliniskt protokoll.' },
  ]},

  // ── Autoimmunity EN ───────────────────────────────────────────────────────
  { rel: 'en/autoimmunity/index.html', qas: [
    { q: 'What causes autoimmune disease?', a: 'Autoimmune disease occurs when the immune system attacks the body\'s own tissues. Common biological drivers include gut dysbiosis and increased intestinal permeability ("leaky gut"), food immune reactivity, viral infections (molecular mimicry), heavy metal burden and genetic predisposition.' },
    { q: 'Can autoimmunity go into remission?', a: 'Full remission is possible in certain autoimmune conditions. MediBalans focuses on identifying and eliminating the biological drivers — food immune reactivity (ALCAT), gut dysbiosis (GI Effects), intracellular nutritional deficiency (CMA) and methylation dysfunction (MethylDetox) — that sustain immune activation.' },
    { q: 'What is the connection between gut health and autoimmunity?', a: 'Intestinal permeability (leaky gut) allows unprocessed peptides to cross the gut barrier and trigger systemic immune reactions. Specific bacterial patterns (Klebsiella, Proteus) are linked to rheumatoid arthritis and ankylosing spondylitis. GI Effects maps these patterns directly.' },
    { q: 'How does MediBalans investigate autoimmunity?', a: 'MediBalans investigation includes ALCAT (food immune reactivity), GI Effects (gut microbiome and barrier function), CMA (intracellular nutrition), MethylDetox (MTHFR and genetic risk) and when indicated, NutrEval (metabolomic profile). Results are interpreted in an integrated clinical protocol.' },
  ]},

  // ── Hypothyreos SV ────────────────────────────────────────────────────────
  { rel: 'hypothyreos/index.html', qas: [
    { q: 'Kan man ha hypothyreos med normalt TSH?', a: 'Ja. TSH mäter hypofysens signal, inte vävnadernas faktiska respons. Nedsatt konversion av T4 till aktivt T3 kan ge hypotyreossymtom trots normalt TSH. Omvänt T3 (rT3) blockerar sköldkörtelreceptorer. Dessa mäts inte i standardprover men ingår i MediBalans utredning.' },
    { q: 'Vad är skillnaden mellan Hashimotos och vanlig hypothyreos?', a: 'Hashimotos tyreoidit är en autoimmun attack mot sköldkörteln — den vanligaste orsaken till hypothyreos i Sverige. TPO-antikroppar och thyroglobulin-antikroppar bekräftar diagnosen. Klinisk remission kräver identifiering av de underliggande autoimmuna drivkrafterna: matimmunreaktivitet (ALCAT), tarmdysbiosis (GI Effects) och methyleringsrubbning (MethylDetox).' },
    { q: 'Hur påverkar näringsbrist sköldkörtelfunktionen?', a: 'Selen är essentiellt för deiodinasenzymerna som konverterar T4 till T3. Zink, järn och jod är kritiska för tyroxinsyntesen. Magnesium och B-vitaminer stödjer sköldkörtelns energimetabolism. CMA identifierar intracellulära brister som påverkar sköldkörtelfunktionen oavsett serumnivåer.' },
    { q: 'Inkluderar MediBalans-utredning genetisk analys för sköldkörtel?', a: 'Ja. MethylDetox inkluderar MTHFR och COMT-varianter som påverkar biotillgängligheten av sköldkörtelhormonet. WGS (helgenomsekvensering) identifierar varianter i deiodinasgenerna DIO1, DIO2 och DIO3 som styr T4 till T3-konversionen.' },
  ]},

  // ── Thyroid EN ────────────────────────────────────────────────────────────
  { rel: 'en/thyroid/index.html', qas: [
    { q: 'Can you have hypothyroidism with a normal TSH?', a: 'Yes. TSH measures the pituitary\'s signal, not tissues\' actual response. Impaired conversion of T4 to active T3 can cause hypothyroid symptoms despite a normal TSH. Reverse T3 (rT3) blocks thyroid receptors. These are not measured in standard panels but are included in the MediBalans investigation.' },
    { q: 'What is the difference between Hashimoto\'s and regular hypothyroidism?', a: 'Hashimoto\'s thyroiditis is an autoimmune attack on the thyroid gland — the most common cause of hypothyroidism. TPO antibodies and thyroglobulin antibodies confirm the diagnosis. Clinical remission requires identifying the underlying autoimmune drivers: food immune reactivity (ALCAT), gut dysbiosis (GI Effects) and methylation dysfunction (MethylDetox).' },
    { q: 'How does nutritional deficiency affect thyroid function?', a: 'Selenium is essential for the deiodinase enzymes that convert T4 to T3. Zinc, iron and iodine are critical for thyroxine synthesis. Magnesium and B-vitamins support thyroid energy metabolism. CMA identifies intracellular deficiencies affecting thyroid function regardless of serum levels.' },
    { q: 'Does MediBalans include genetic analysis for thyroid conditions?', a: 'Yes. MethylDetox includes MTHFR and COMT variants that affect thyroid hormone bioavailability. WGS (whole genome sequencing) identifies variants in the deiodinase genes DIO1, DIO2 and DIO3 that govern T4-to-T3 conversion.' },
  ]},

  // ── Kognitiv hälsa SV ─────────────────────────────────────────────────────
  { rel: 'kognitiv-halsa/index.html', qas: [
    { q: 'Vad orsakar hjärndimma?', a: 'Hjärndimma (kognitiv dimma) har typiskt biologiska orsaker: intracellulär näringsbrist (magnesium, B12, zink, CoQ10), methyleringsrubbning (MTHFR), mitokondriell dysfunktion, subklinisk hypothyreos, kronisk låggradig inflammation och SIBO. MediBalans kartlägger vilken mekanism som är primär.' },
    { q: 'Kan näringsbrist orsaka minnesproblem?', a: 'Ja. B12-brist orsakar reversibel neurodegeneration. Magnesium är essentiellt för synaptisk plasticitet och minneskodning. Omega-3 fettsyror (DHA) är strukturella komponenter i neuronala membran. CMA och NutrEval identifierar dessa brister funktionellt.' },
    { q: 'Vad är kopplingen mellan tarmen och hjärnan?', a: 'Tarm-hjärn-axeln är en bidirektionell kommunikationskanal via vagusnerven, immunsystemet och neurotransmittorer. 90% av serotonin produceras i tarmen. Tarmdysbiosis påverkar humör, kognition och stressrespons. GI Effects kartlägger tarmmikrobiomets funktionella kapacitet för neurotransmittorsyntes.' },
    { q: 'Hur förebygger MediBalans kognitiv nedgång?', a: 'MediBalans biologiska åldersutredning inkluderar telomermätning (biologisk ålder), WGS (APOE4, MTHFR), NutrEval (näringsprofil) och GI Effects (tarmprofil). Protokollet adresserar de modifierbara riskfaktorerna för kognitiv nedgång.' },
  ]},

  // ── Cognitive Health EN ───────────────────────────────────────────────────
  { rel: 'en/cognitive-health/index.html', qas: [
    { q: 'What causes brain fog?', a: 'Brain fog has typically biological causes: intracellular nutritional deficiency (magnesium, B12, zinc, CoQ10), methylation dysfunction (MTHFR), mitochondrial impairment, subclinical hypothyroidism, chronic low-grade inflammation and SIBO. MediBalans identifies which mechanism is primary.' },
    { q: 'Can nutritional deficiency cause memory problems?', a: 'Yes. B12 deficiency causes reversible neurodegeneration. Magnesium is essential for synaptic plasticity and memory encoding. Omega-3 fatty acids (DHA) are structural components of neuronal membranes. CMA and NutrEval identify these deficiencies functionally.' },
    { q: 'What is the gut-brain connection?', a: 'The gut-brain axis is a bidirectional communication channel via the vagus nerve, immune system and neurotransmitters. 90% of serotonin is produced in the gut. Gut dysbiosis affects mood, cognition and stress response. GI Effects maps the gut microbiome\'s functional capacity for neurotransmitter synthesis.' },
    { q: 'How does MediBalans prevent cognitive decline?', a: 'MediBalans biological age assessment includes telomere measurement (biological age), WGS (APOE4, MTHFR), NutrEval (nutritional profile) and GI Effects (gut profile). The protocol addresses the modifiable risk factors for cognitive decline.' },
  ]},

  // ── ADHD SV ───────────────────────────────────────────────────────────────
  { rel: 'adhd-neuropsykiatri/index.html', qas: [
    { q: 'Kan näringsbrist orsaka ADHD-symtom?', a: 'Ja. Zink, magnesium, järn, omega-3 och B6 är kritiska för dopamin- och noradrenalinsyntesen. Studier visar att barn och vuxna med ADHD-diagnoser ofta har lägre intracellulära nivåer av dessa mikronutrienter jämfört med kontroller. CMA identifierar dessa brister funktionellt.' },
    { q: 'Vad är kopplingen mellan MTHFR och ADHD?', a: 'MTHFR-varianter (rs1801133) reducerar folsyraomvandlingen och påverkar methyldonationen till neurotransmittorsyntes och genregulation. Studier visar association mellan MTHFR C677T och ADHD. MethylDetox analyserar 38 methyleringsrelaterade varianter.' },
    { q: 'Hur utreder MediBalans ADHD och neuropsykiatri?', a: 'MediBalans utredning inkluderar MethylDetox (genetisk methylering), CMA (intracellulär näring), NutrEval (organiska syror inklusive neurotransmittormarkörer) och vid behov ALCAT (matimmunreaktivitet). Protokollet kompletterar, ersätter inte, neuropsykiatrisk utredning.' },
    { q: 'Finns det biologiska behandlingsalternativ vid ADHD?', a: 'Biologisk precisionsmedicin vid ADHD fokuserar på att optimera methylering (metylfolat, metyl-B12), intracellulär mineralnäring (magnesium, zink) och mitokondriell funktion. Detta kan minska symtombörda och ibland medicinbehov som komplement till konventionell behandling.' },
  ]},

  // ── ADHD EN ───────────────────────────────────────────────────────────────
  { rel: 'en/adhd-neuropsychiatry/index.html', qas: [
    { q: 'Can nutritional deficiency cause ADHD symptoms?', a: 'Yes. Zinc, magnesium, iron, omega-3 and B6 are critical for dopamine and noradrenaline synthesis. Studies show that children and adults with ADHD diagnoses often have lower intracellular levels of these micronutrients compared to controls. CMA identifies these deficiencies functionally.' },
    { q: 'What is the connection between MTHFR and ADHD?', a: 'MTHFR variants (rs1801133) reduce folate conversion and affect methyl donation to neurotransmitter synthesis and gene regulation. Studies show an association between MTHFR C677T and ADHD. MethylDetox analyses 38 methylation-related variants.' },
    { q: 'How does MediBalans investigate ADHD and neuropsychiatry?', a: 'MediBalans investigation includes MethylDetox (genetic methylation), CMA (intracellular nutrition), NutrEval (organic acids including neurotransmitter markers) and when indicated, ALCAT (food immune reactivity). The protocol complements, but does not replace, neuropsychiatric assessment.' },
    { q: 'Are there biological treatment options for ADHD?', a: 'Biological precision medicine for ADHD focuses on optimising methylation (methylfolate, methyl-B12), intracellular mineral nutrition (magnesium, zinc) and mitochondrial function. This can reduce symptom burden and sometimes medication needs as a complement to conventional treatment.' },
  ]},

  // ── Hudsjukdomar SV ───────────────────────────────────────────────────────
  { rel: 'hudsjukdomar/index.html', qas: [
    { q: 'Vad orsakar eksem, psoriasis och kronisk akne?', a: 'Kroniska hudsjukdomar drivs typiskt av immunologisk hyperaktivitet, matimmunreaktivitet, tarmdysbiosis och intracellulär näringsbrist. ALCAT identifierar specifika livsmedel som triggar inflammation. GI Effects kartlägger tarmfloran och barriärfunktionen som är en primär drivkraft vid Th17-medierade hudsjukdomar som psoriasis.' },
    { q: 'Kan mat orsaka psoriasis?', a: 'Ja. Matimmunreaktivitet (IgG/cellulär) driver systemisk inflammation som manifesteras i huden. Gluten, mejeriprodukter och socker är vanliga triggers, men ALCAT identifierar individspecifika reaktioner — inte generella grupper. Elimineringsprotokoll baserat på ALCAT-resultat visar klinisk förbättring vid psoriasis.' },
    { q: 'Vad är kopplingen mellan tarm och hud?', a: 'Tarmdysbiosis och ökad tarmpermeabilitet ("gut-skin axis") driver systemisk inflammation som triggar hudsjukdomar. GI Effects identifierar dessa mönster och vägleder målinriktad tarmbehandling som ofta ger parallell förbättring av hudstatus.' },
    { q: 'Hur utreder MediBalans hudsjukdomar?', a: 'MediBalans identifierar de biologiska drivkrafterna: ALCAT (matimmunreaktivitet), GI Effects (tarmprofil), CMA (zink, omega-3, A-vitamin — kritiska för hudbarriären) och vid behov MethylDetox (COMT-varianter påverkar histaminmetabolism vid atopiskt eksem).' },
  ]},

  // ── Skin Conditions EN ────────────────────────────────────────────────────
  { rel: 'en/skin-conditions/index.html', qas: [
    { q: 'What causes eczema, psoriasis and chronic acne?', a: 'Chronic skin conditions are typically driven by immune hyperactivity, food immune reactivity, gut dysbiosis and intracellular nutritional deficiency. ALCAT identifies specific foods that trigger inflammation. GI Effects maps the gut microbiome and barrier function, which is a primary driver in Th17-mediated skin conditions such as psoriasis.' },
    { q: 'Can food cause psoriasis?', a: 'Yes. Food immune reactivity (IgG/cellular) drives systemic inflammation that manifests in the skin. Gluten, dairy and sugar are common triggers, but ALCAT identifies individual-specific reactions — not general food groups. Elimination protocols based on ALCAT results show clinical improvement in psoriasis.' },
    { q: 'What is the gut-skin connection?', a: 'Gut dysbiosis and increased intestinal permeability ("gut-skin axis") drive systemic inflammation that triggers skin conditions. GI Effects identifies these patterns and guides targeted gut treatment that often produces parallel improvement in skin status.' },
    { q: 'How does MediBalans investigate skin conditions?', a: 'MediBalans identifies the biological drivers: ALCAT (food immune reactivity), GI Effects (gut profile), CMA (zinc, omega-3, vitamin A — critical for skin barrier function) and when indicated, MethylDetox (COMT variants affect histamine metabolism in atopic eczema).' },
  ]},

  // ── Alzheimers-test SV ────────────────────────────────────────────────────
  { rel: 'alzheimers-test/index.html', qas: [
    { q: 'Kan Alzheimer förebyggas?', a: 'Forskning visar att upp till 40% av Alzheimer kan förebyggas eller fördröjas via modifierbara riskfaktorer. APOE4-genvarianten ökar risken 3-12 gånger men är inte deterministisk. Biologisk åldersutredning hos MediBalans identifierar APOE4-status, telomerlängd, mitokondriell funktion och intracellulär näringsbrist — alla modifierbara faktorer.' },
    { q: 'Vad är APOE4 och hur påverkar det Alzheimer-risken?', a: 'APOE4 är en genetisk variant som försämrar amyloid-clearance i hjärnan, ökar neuroinflammation och reducerar mitokondriell effektivitet. En kopia av APOE4 ger ungefär 3 gånger ökad risk; två kopior ger 8-12 gånger ökad risk. MediBalans WGS (helgenomsekvensering) identifierar APOE4-status och 50+ andra neurologiska riskmarkörer.' },
    { q: 'Vilka tester är relevanta vid Alzheimer-prevention?', a: 'MediBalans erbjuder ett Alzheimer-preventionsprotokoll med: WGS (APOE4, CLU, PICALM, TREM2), biologisk åldersbestämning (telomermätning), NutrEval (omega-3, B12, D-vitamin, folat — neuroskyddande näring) och MethylDetox (MTHFR — homocystein är en oberoende riskfaktor för demens).' },
    { q: 'Kan homocystein orsaka demens?', a: 'Förhöjt homocystein är en oberoende riskfaktor för kognitiv nedgång och demens. Homocysteinreduktion via B12, folat och B6 reducerar hjärnatrofi enligt randomiserade studier (VITACOG, FACIT). MTHFR-varianter begränsar förmågan att metabolisera folsyra — MethylDetox identifierar dessa varianter.' },
  ]},

  // ── Alzheimer's Assessment EN ─────────────────────────────────────────────
  { rel: 'en/alzheimers-assessment/index.html', qas: [
    { q: 'Can Alzheimer\'s disease be prevented?', a: 'Research suggests up to 40% of Alzheimer\'s cases may be preventable or delayed through modifiable risk factors. The APOE4 genetic variant increases risk 3-12 fold but is not deterministic. MediBalans biological age assessment identifies APOE4 status, telomere length, mitochondrial function and intracellular nutritional deficiency — all modifiable factors.' },
    { q: 'What is APOE4 and how does it affect Alzheimer\'s risk?', a: 'APOE4 is a genetic variant that impairs amyloid clearance in the brain, increases neuroinflammation and reduces mitochondrial efficiency. One copy of APOE4 confers approximately 3-fold increased risk; two copies confer 8-12 fold increased risk. MediBalans WGS (whole genome sequencing) identifies APOE4 status and 50+ other neurological risk markers.' },
    { q: 'Which tests are relevant for Alzheimer\'s prevention?', a: 'MediBalans offers an Alzheimer\'s prevention protocol including: WGS (APOE4, CLU, PICALM, TREM2), biological age assessment (telomere measurement), NutrEval (omega-3, B12, vitamin D, folate — neuroprotective nutrients) and MethylDetox (MTHFR — homocysteine is an independent risk factor for dementia).' },
    { q: 'Can homocysteine cause dementia?', a: 'Elevated homocysteine is an independent risk factor for cognitive decline and dementia. Homocysteine reduction via B12, folate and B6 reduces brain atrophy according to randomised trials (VITACOG, FACIT). MTHFR variants limit the ability to metabolise folic acid — MethylDetox identifies these variants.' },
  ]},

];

// ─── APPLY ───────────────────────────────────────────────────────────────────

let updated = 0, skipped = 0, missing = 0;

for (const { rel, qas } of PAGES) {
  try {
    read(rel); // test file exists
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
