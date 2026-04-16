#!/usr/bin/env node
// add_comparison_tables.mjs — inject comparison table sections into all Genova test pages

import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname);
const p = (rel) => resolve(ROOT, rel.replace(/\//g, '\\'));
function read(rel) { return readFileSync(p(rel), 'utf8'); }
function write(rel, c) { writeFileSync(p(rel), c, 'utf8'); }

// ─── HTML builder ────────────────────────────────────────────────────────────

function fmt(val) {
  return val
    .replace(/✓/g, '<span style="color:#2a7a4b;">✓</span>')
    .replace(/—/g, '<span style="color:#999;">—</span>');
}

function buildTable({ heading, sub, cols, rows, closing }) {
  const thCells = [
    `<th style="padding:10px 12px;text-align:left;font-weight:500;min-width:120px;"> </th>`,
    `<th style="padding:10px 12px;text-align:left;font-weight:600;">${cols[0]}</th>`,
    ...cols.slice(1).map(c => `<th style="padding:10px 12px;text-align:left;font-weight:500;">${c}</th>`),
  ].join('\n          ');

  const rowsHtml = rows.map((row, i) => {
    const bg = i % 2 === 0 ? '#fff' : '#f4f4f0';
    const [label, mbVal, ...rest] = row;
    const labelCell = `<td style="padding:10px 12px;color:#333;font-weight:500;white-space:nowrap;">${label}</td>`;
    const mbCell = `<td style="padding:10px 12px;font-weight:600;color:#1a2744;">${fmt(mbVal)}</td>`;
    const restCells = rest.map(v => `<td style="padding:10px 12px;">${fmt(v)}</td>`).join('');
    return `        <tr style="background:${bg};">${labelCell}${mbCell}${restCells}</tr>`;
  }).join('\n');

  return `\n<section style="background:#f8f8f6;border-radius:16px;padding:32px 28px;margin:40px 0;">
  <h2 style="font-family:system-ui,-apple-system,sans-serif;font-size:18px;font-weight:600;color:#1a2744;margin:0 0 8px 0;">${heading}</h2>
  <p style="font-size:14px;color:#555;margin:0 0 24px 0;">${sub}</p>
  <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:13px;font-family:system-ui,sans-serif;">
      <thead>
        <tr style="background:#1a2744;color:white;">
          ${thCells}
        </tr>
      </thead>
      <tbody>
${rowsHtml}
      </tbody>
    </table>
  </div>
  <p style="font-size:12px;color:#777;margin:20px 0 0 0;font-style:italic;">${closing}</p>
</section>\n`;
}

function inject(rel, html) {
  let c = read(rel);
  const orig = c;
  // Try all known CTA section class names
  const anchors = [
    '<section class="booking-cta">',
    '<section class="cta-section">',
    '<section class="booking-section"',
  ];
  for (const anchor of anchors) {
    if (c.includes(anchor)) {
      c = c.replace(anchor, html + anchor);
      break;
    }
  }
  if (c === orig) { console.log(`  WARN: no anchor in ${rel}`); return false; }
  write(rel, c);
  return true;
}

// ─── TABLE DATA ──────────────────────────────────────────────────────────────

const TABLES = [

  // ── GI Effects SV ─────────────────────────────────────────────────────────
  { rel: 'gi-effects-test/index.html', data: {
    heading: 'Hur skiljer sig GI Effects® från andra tarmtester?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / GI Effects®', 'GetTested / Tarmkollen Mega', 'GI-MAP / Nordic FM', 'Gutfeeling Labs'],
    rows: [
      ['Metodik', 'PCR + MALDI-TOF + Odling', 'qPCR DNA-analys', 'qPCR DNA-analys', 'Masspektrometri (urin)'],
      ['Laboratorium', 'Genova, CLIA-cert., USA', 'Okänt, Tyskland', 'Diagnostic Solutions, USA', 'Lunds Universitet'],
      ['Antal kliniska markörer', '60+', '91', '50+', '3 (SIBO, läckande tarm, TMAO)'],
      ['Patogener &amp; parasiter', '✓', '✓', '✓', '—'],
      ['Inflammation (kalprotektin)', '✓', '✓', '✓', '—'],
      ['Antibiotikaresistens', '✓', '—', '✓', '—'],
      ['Kortkedjade fettsyror', '✓', '—', 'Tillval', '—'],
      ['Läkartolkning', '✓ Alltid ingår', '—', 'Tillval', '—'],
      ['Personligt protokoll', '✓', '—', '—', '—'],
      ['Pris', '8 500 kr', '2 495 kr', '~5 000 kr + rådgivning', '~2 200 kr'],
    ],
    closing: 'Prisskillnaden är verklig. Den speglar tre analysmetoder istället för en, CLIA-certifierat laboratorium, legitimerad läkartolkning — och att vi är de enda i Sverige som kan beställa detta test.',
  }},

  // ── GI Effects EN ─────────────────────────────────────────────────────────
  { rel: 'en/gi-effects-test/index.html', data: {
    heading: 'How does GI Effects® compare to other gut tests?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / GI Effects®', 'GetTested / Tarmkollen Mega', 'GI-MAP / Nordic FM', 'Gutfeeling Labs'],
    rows: [
      ['Methodology', 'PCR + MALDI-TOF + Culture', 'qPCR DNA analysis', 'qPCR DNA analysis', 'Mass spectrometry (urine)'],
      ['Laboratory', 'Genova, CLIA-cert., USA', 'Unknown, Germany', 'Diagnostic Solutions, USA', 'Lund University'],
      ['Clinical markers', '60+', '91', '50+', '3 (SIBO, leaky gut, TMAO)'],
      ['Pathogens &amp; parasites', '✓', '✓', '✓', '—'],
      ['Inflammation (calprotectin)', '✓', '✓', '✓', '—'],
      ['Antibiotic resistance', '✓', '—', '✓', '—'],
      ['Short-chain fatty acids', '✓', '—', 'Add-on', '—'],
      ['Physician interpretation', '✓ Always included', '—', 'Add-on', '—'],
      ['Personal protocol', '✓', '—', '—', '—'],
      ['Price', 'SEK 8,500', 'SEK 2,495', '~SEK 5,000 + consultation', '~SEK 2,200'],
    ],
    closing: 'The price difference is real. It reflects three analytical methods instead of one, a CLIA-certified laboratory, licensed physician interpretation — and being the only provider in Sweden able to order this test.',
  }},

  // ── SIBO SV ───────────────────────────────────────────────────────────────
  { rel: 'sibo-test/index.html', data: {
    heading: 'Hur skiljer sig MediBalans SIBO-test från andra?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / SIBO-test', 'GetTested / SIBO-test', 'Gutfeeling Labs', 'Holistic SIBO-test'],
    rows: [
      ['Metod', 'Lactulose andningstest', 'Lactulose andningstest', 'Urintest (masspektrometri)', 'Lactulose andningstest'],
      ['Gaser som mäts', 'H₂ + CH₄ + H₂S (flat line)', 'H₂ + CH₄', 'SIBO-metaboliter i urin', 'H₂ + CH₄'],
      ['Provtagningstid', '3 timmar (10 mätpunkter)', '2 timmar (7 rör)', 'Engångsprov', '2 timmar'],
      ['Läkartolkning', '✓ Alltid ingår', '—', '—', '—'],
      ['Behandlingsprotokoll', '✓', '—', 'Kostråd', '—'],
      ['Laboratorium', 'Genova, CLIA-cert., USA', 'Okänt', 'Lunds Universitet', 'ISO15189'],
      ['Pris', '3 700 kr', '995 kr', '~2 200 kr', '~995 kr'],
    ],
    closing: 'Skillnaden är inte bara priset — det är hur många gaser vi mäter, hur länge vi mäter, och att en läkare tolkar resultatet och skriver ett behandlingsprotokoll.',
  }},

  // ── SIBO EN ───────────────────────────────────────────────────────────────
  { rel: 'en/sibo-test/index.html', data: {
    heading: 'How does MediBalans SIBO test compare?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / SIBO test', 'GetTested / SIBO test', 'Gutfeeling Labs', 'Holistic SIBO test'],
    rows: [
      ['Method', 'Lactulose breath test', 'Lactulose breath test', 'Urine test (mass spectrometry)', 'Lactulose breath test'],
      ['Gases measured', 'H₂ + CH₄ + H₂S (flat line)', 'H₂ + CH₄', 'SIBO metabolites in urine', 'H₂ + CH₄'],
      ['Collection time', '3 hours (10 data points)', '2 hours (7 tubes)', 'Single sample', '2 hours'],
      ['Physician interpretation', '✓ Always included', '—', '—', '—'],
      ['Treatment protocol', '✓', '—', 'Dietary advice', '—'],
      ['Laboratory', 'Genova, CLIA-cert., USA', 'Unknown', 'Lund University', 'ISO15189'],
      ['Price', 'SEK 3,700', 'SEK 995', '~SEK 2,200', '~SEK 995'],
    ],
    closing: 'The difference is not just the price — it is how many gases we measure, how long we measure for, and that a physician interprets the result and writes a treatment protocol.',
  }},

  // ── ALCAT SV ──────────────────────────────────────────────────────────────
  { rel: 'alcat/index.html', data: {
    heading: 'Varför är ALCAT annorlunda än IgG-matintoleranstester?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / ALCAT', 'GetTested / IgG-test', 'Quicktest / IgG-test', 'Cerascreen / IgG-test'],
    rows: [
      ['Testmetod', 'Cellulär (leukocytreaktivitet)', 'ELISA IgG-antikroppar', 'ELISA IgG-antikroppar', 'ELISA IgG-antikroppar'],
      ['Mäter', 'Direkt cellulär immunreaktion', 'IgG-antikroppsnivåer', 'IgG-antikroppsnivåer', 'IgG-antikroppsnivåer'],
      ['Klinisk validering', '✓ Peer-reviewed studier', 'Begränsad', 'Begränsad', 'Begränsad'],
      ['Antal testade ämnen', '250 livsmedel, tillsatser, kemikalier', '78–120 ämnen', '120 ämnen + 20 tillsatser', '76 livsmedel'],
      ['Falska positiva vid rotation', 'Lägre risk', 'Högre risk', 'Högre risk', 'Högre risk'],
      ['Läkartolkning', '✓ Alltid ingår', '—', '—', '—'],
      ['Eliminationsprotokoll', '✓ Personligt', 'Generiska råd', 'Generiska råd', 'Generiska råd'],
      ['Pris', 'Ingår i paketet', '995–1 595 kr', '895 kr', '899 kr'],
    ],
    closing: 'IgG-antikroppar bildas naturligt när vi äter mat — höga nivåer kan spegla frekvens av intag snarare än intolerans. ALCAT mäter den faktiska cellulära reaktionen. Det är en fundamental metodologisk skillnad.',
  }},

  // ── ALCAT EN ──────────────────────────────────────────────────────────────
  { rel: 'en/alcat-test/index.html', data: {
    heading: 'Why is ALCAT different from IgG food intolerance tests?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / ALCAT', 'GetTested / IgG test', 'Quicktest / IgG test', 'Cerascreen / IgG test'],
    rows: [
      ['Test method', 'Cellular (leukocyte reactivity)', 'ELISA IgG antibodies', 'ELISA IgG antibodies', 'ELISA IgG antibodies'],
      ['Measures', 'Direct cellular immune response', 'IgG antibody levels', 'IgG antibody levels', 'IgG antibody levels'],
      ['Clinical validation', '✓ Peer-reviewed studies', 'Limited', 'Limited', 'Limited'],
      ['Substances tested', '250 foods, additives, chemicals', '78–120 items', '120 items + 20 additives', '76 foods'],
      ['False positives on rotation', 'Lower risk', 'Higher risk', 'Higher risk', 'Higher risk'],
      ['Physician interpretation', '✓ Always included', '—', '—', '—'],
      ['Elimination protocol', '✓ Personalised', 'Generic advice', 'Generic advice', 'Generic advice'],
      ['Price', 'Included in package', 'SEK 995–1,595', 'SEK 895', 'SEK 899'],
    ],
    closing: 'IgG antibodies form naturally when we eat food — high levels may reflect frequency of consumption rather than intolerance. ALCAT measures the actual cellular response. That is a fundamental methodological difference.',
  }},

  // ── NutrEval SV ───────────────────────────────────────────────────────────
  { rel: 'nutreval-sverige/index.html', data: {
    heading: 'Vad är skillnaden mellan NutrEval och ett vanligt blodprov?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / NutrEval®', 'Standard blodprov (1177/Werlabs)', 'GetTested / Näringspanel', 'Zinzino BalanceTest'],
    rows: [
      ['Vad mäts', 'Funktionell näringsstatus, intracellulär', 'Serumnivåer (utanför cellen)', 'Serumnivåer', '11 fettsyror'],
      ['Antal biomarkörer', '125+', '5–20 (beroende på panel)', '10–30', '11'],
      ['Metod', 'Blod + urin (GC/MS, LC/MS)', 'Venöst blod, serum', 'Venöst blod, serum', 'Torkat blodprov (DBS)'],
      ['Identifierar dold brist', '✓ (normal serum, låg cellulär)', '—', '—', '—'],
      ['Aminosyror', '✓', '—', '—', '—'],
      ['Fettsyror', '✓', '—', '—', '✓ (11 fettsyror)'],
      ['Oxidativ stress', '✓', '—', '—', '—'],
      ['Läkartolkning', '✓ Alltid ingår', 'Via remiss', '—', '—'],
      ['Syfte', 'Klinisk precision', 'Utesluta sjukdom', 'Hälsoscreening', 'Sälja kosttillskott'],
      ['Pris', '12 200 kr', '0–500 kr', '500–1 500 kr', '~400 kr (+ prenumeration)'],
    ],
    closing: 'Du kan ha normala serumvärden och ändå ha funktionell näringsbrist på cellnivå. Det är precis vad NutrEval mäter — och det är vad standardprover missar.',
  }},

  // ── NutrEval EN ───────────────────────────────────────────────────────────
  { rel: 'en/nutreval-test/index.html', data: {
    heading: 'How does NutrEval compare to standard blood tests?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / NutrEval®', 'Standard blood test (GP/Werlabs)', 'GetTested / Nutrition panel', 'Zinzino BalanceTest'],
    rows: [
      ['What is measured', 'Functional nutritional status, intracellular', 'Serum levels (outside cells)', 'Serum levels', '11 fatty acids'],
      ['Biomarkers', '125+', '5–20 (depending on panel)', '10–30', '11'],
      ['Method', 'Blood + urine (GC/MS, LC/MS)', 'Venous blood, serum', 'Venous blood, serum', 'Dried blood spot (DBS)'],
      ['Identifies hidden deficiency', '✓ (normal serum, low intracellular)', '—', '—', '—'],
      ['Amino acids', '✓', '—', '—', '—'],
      ['Fatty acids', '✓', '—', '—', '✓ (11 fatty acids)'],
      ['Oxidative stress', '✓', '—', '—', '—'],
      ['Physician interpretation', '✓ Always included', 'Via referral', '—', '—'],
      ['Purpose', 'Clinical precision', 'Rule out disease', 'Health screening', 'Sell supplements'],
      ['Price', 'SEK 12,200', 'SEK 0–500', 'SEK 500–1,500', '~SEK 400 (+ subscription)'],
    ],
    closing: 'You can have normal serum values and still have functional nutritional deficiency at the cellular level. That is exactly what NutrEval measures — and what standard tests miss.',
  }},

  // ── CMA SV ────────────────────────────────────────────────────────────────
  { rel: 'cma/index.html', data: {
    heading: 'Varför mäter CMA näring annorlunda än blodprov?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / CMA', 'Standard blodprov', 'GetTested / Näringspanel', 'Werlabs hälsokontroll'],
    rows: [
      ['Mätplats', 'Inuti cellen (intracellulär)', 'Serum (utanför cellen)', 'Serum', 'Serum'],
      ['Klinisk relevans', 'Visar faktisk cellulär funktion', 'Visar cirkulerande nivåer', 'Visar cirkulerande nivåer', 'Visar cirkulerande nivåer'],
      ['Identifierar dold brist', '✓', '—', '—', '—'],
      ['Magnesium (intracellulär)', '✓', '—', '—', '—'],
      ['Zink, selen, antioxidanter', '✓', 'Delvis (serum)', 'Delvis', 'Delvis'],
      ['Läkartolkning', '✓ Alltid ingår', 'Via remiss', '—', 'Delvis'],
      ['Pris', 'Ingår i paketet', '0–300 kr', '300–800 kr', '500–2 000 kr'],
    ],
    closing: '80% av kroppens magnesium finns inuti cellerna. Standardblodprov mäter det 20% som cirkulerar i serum. CMA mäter det som faktiskt driver enzymfunktion och energiproduktion.',
  }},

  // ── CMA EN ────────────────────────────────────────────────────────────────
  { rel: 'en/cellular-nutrient-analysis/index.html', data: {
    heading: 'Why does CMA measure nutrition differently from blood tests?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / CMA', 'Standard blood test', 'GetTested / Nutrition panel', 'Werlabs health check'],
    rows: [
      ['Measurement site', 'Inside cells (intracellular)', 'Serum (outside cells)', 'Serum', 'Serum'],
      ['Clinical relevance', 'Shows actual cellular function', 'Shows circulating levels', 'Shows circulating levels', 'Shows circulating levels'],
      ['Identifies hidden deficiency', '✓', '—', '—', '—'],
      ['Magnesium (intracellular)', '✓', '—', '—', '—'],
      ['Zinc, selenium, antioxidants', '✓', 'Partial (serum)', 'Partial', 'Partial'],
      ['Physician interpretation', '✓ Always included', 'Via referral', '—', 'Partial'],
      ['Price', 'Included in package', 'SEK 0–300', 'SEK 300–800', 'SEK 500–2,000'],
    ],
    closing: '80% of the body\'s magnesium is inside cells. Standard blood tests measure the 20% that circulates in serum. CMA measures what actually drives enzyme function and energy production.',
  }},

  // ── Organix SV ────────────────────────────────────────────────────────────
  { rel: 'organix/index.html', data: {
    heading: 'Hur skiljer sig Organix® från andra tester för organiska syror?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / Organix®', 'GetTested / Organic Acids', 'Nordic FM / Organix', 'Standard blodprov'],
    rows: [
      ['Antal markörer', '70+ organiska syror', '21 markörer', '70+', '—'],
      ['Laboratorium', 'Genova, CLIA-cert., USA', 'Okänt', 'Genova, USA', 'Karolinska/regionlab'],
      ['Kliniska domäner', 'Mitokondrier, methylering, toxiner, neurotransmittorer, dysbiosis', 'Energi, näring, dysbiosis', 'Samma som Genova', 'Utesluter metabola sjukdomar'],
      ['Neurotransmittormetaboliter', '✓', 'Delvis', '✓', '—'],
      ['Toxinexponering', '✓', '—', '✓', '—'],
      ['Oxidativ stress (8-OHdG)', '✓', '—', '✓', '—'],
      ['Läkartolkning', '✓ Alltid ingår', '—', 'Tillval', 'Via remiss'],
      ['Pris', '5 600 kr', '~1 500 kr', '~3 500 kr + rådgivning', '0 kr (remiss krävs)'],
    ],
    closing: 'GetTesteds Organic Acids-test mäter 21 markörer — en tredjedel av vad Organix® mäter. Skillnaden är inte bara kvantitativ: de kliniska domänerna för neurotransmittorer, toxinexponering och oxidativ stress saknas helt.',
  }},

  // ── Organix EN ────────────────────────────────────────────────────────────
  { rel: 'en/organix/index.html', data: {
    heading: 'How does Organix® compare to other organic acids tests?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / Organix®', 'GetTested / Organic Acids', 'Nordic FM / Organix', 'Standard blood test'],
    rows: [
      ['Markers', '70+ organic acids', '21 markers', '70+', '—'],
      ['Laboratory', 'Genova, CLIA-cert., USA', 'Unknown', 'Genova, USA', 'Regional lab'],
      ['Clinical domains', 'Mitochondria, methylation, toxins, neurotransmitters, dysbiosis', 'Energy, nutrition, dysbiosis', 'Same as Genova', 'Rules out metabolic disease'],
      ['Neurotransmitter metabolites', '✓', 'Partial', '✓', '—'],
      ['Toxin exposure', '✓', '—', '✓', '—'],
      ['Oxidative stress (8-OHdG)', '✓', '—', '✓', '—'],
      ['Physician interpretation', '✓ Always included', '—', 'Add-on', 'Via referral'],
      ['Price', 'SEK 5,600', '~SEK 1,500', '~SEK 3,500 + consultation', 'SEK 0 (referral required)'],
    ],
    closing: 'GetTested\'s Organic Acids test measures 21 markers — one third of what Organix® measures. The difference is not only quantitative: the clinical domains for neurotransmitters, toxin exposure and oxidative stress are entirely absent.',
  }},

  // ── Fettsyror SV ──────────────────────────────────────────────────────────
  { rel: 'fettsyror/index.html', data: {
    heading: 'Hur skiljer sig fettsyreanalysen från Zinzino och andra tester?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / Fettsyror', 'GetTested / Omega-3 test', 'Zinzino BalanceTest', 'Standard blodprov'],
    rows: [
      ['Antal fettsyror', '30+', '11', '11', '2–5 (omega-3 index)'],
      ['Metod', 'GC/MS, venöst blod', 'Torkat blodprov (DBS)', 'Torkat blodprov (DBS)', 'Venöst blod, serum'],
      ['Laboratorium', 'Genova, CLIA-cert., USA', 'Okänt', 'Vitas, Oslo', 'Regionlab'],
      ['Omega-3 index', '✓', '✓', '✓', 'Sällan'],
      ['AA/EPA-kvot (kardiovaskulär risk)', '✓', '—', '—', '—'],
      ['Trans-fetter (elaidinsyra)', '✓', '—', '—', '—'],
      ['Mättade fettsyror (full profil)', '✓', '—', '—', '—'],
      ['Läkartolkning', '✓ Alltid ingår', '—', '—', '—'],
      ['Syfte', 'Klinisk diagnostik', 'Hälsoscreening', 'Sälja BalanceOil', 'Screening'],
      ['Pris', '3 900 kr', '~500 kr', '~400 kr (+ prenumeration)', '0–300 kr'],
    ],
    closing: 'Zinzinos BalanceTest är utformat för att motivera köp av deras supplement. Det mäter 11 fettsyror. Genova mäter 30+ — inklusive kardiovaskulära riskmarkörer och transfetter som saknas i konsumenttesterna.',
  }},

  // ── Fatty Acids EN ────────────────────────────────────────────────────────
  { rel: 'en/fatty-acids/index.html', data: {
    heading: 'How does the fatty acid analysis compare to Zinzino and others?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / Fatty Acids', 'GetTested / Omega-3 test', 'Zinzino BalanceTest', 'Standard blood test'],
    rows: [
      ['Fatty acids measured', '30+', '11', '11', '2–5 (omega-3 index)'],
      ['Method', 'GC/MS, venous blood', 'Dried blood spot (DBS)', 'Dried blood spot (DBS)', 'Venous blood, serum'],
      ['Laboratory', 'Genova, CLIA-cert., USA', 'Unknown', 'Vitas, Oslo', 'Regional lab'],
      ['Omega-3 Index', '✓', '✓', '✓', 'Rarely'],
      ['AA/EPA ratio (cardiovascular risk)', '✓', '—', '—', '—'],
      ['Trans fats (elaidic acid)', '✓', '—', '—', '—'],
      ['Saturated fatty acids (full profile)', '✓', '—', '—', '—'],
      ['Physician interpretation', '✓ Always included', '—', '—', '—'],
      ['Purpose', 'Clinical diagnostics', 'Health screening', 'Sell BalanceOil', 'Screening'],
      ['Price', 'SEK 3,900', '~SEK 500', '~SEK 400 (+ subscription)', 'SEK 0–300'],
    ],
    closing: 'Zinzino\'s BalanceTest is designed to motivate purchases of their supplement. It measures 11 fatty acids. Genova measures 30+ — including cardiovascular risk markers and trans fats absent from consumer tests.',
  }},

  // ── Adrenal Stress SV ─────────────────────────────────────────────────────
  { rel: 'adrenal-stress/index.html', data: {
    heading: 'Hur skiljer sig Adrenal Stress Profile från andra kortisoltest?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / Adrenal Stress', 'GetTested / Hormontest kvinna', 'Holistic Kortisoltest', 'Standard blodprov'],
    rows: [
      ['Kortisol mätpunkter', '4 under dagen + CAR', '1 (morgon)', '7 under dagen', '1 (slumpmässig)'],
      ['DHEA', '✓', '✓', '—', 'Separat test'],
      ['DHEA/Kortisol-kvot', '✓', '—', '—', '—'],
      ['Cortisol Awakening Response (CAR)', '✓', '—', '—', '—'],
      ['Dygnsrytm (kurva)', '✓ Full kurva', 'Morgonvärde', '✓ Full kurva', '—'],
      ['Laboratorium', 'Genova, CLIA-cert., USA', 'Okänt', 'ISO15189', 'Regionlab'],
      ['Läkartolkning', '✓ Alltid ingår', '—', '—', 'Via remiss'],
      ['Pris', '2 100 kr', 'Ingår i paketet ~1 500 kr', '~1 200 kr', '0–200 kr'],
    ],
    closing: 'En enda morgonmätning av kortisol berättar ingenting om dygnsrytmen. Det är kurvan — hur kortisol stiger, toppar och sjunker under dagen — som avslöjar om HPA-axeln fungerar normalt.',
  }},

  // ── Adrenal Stress EN ─────────────────────────────────────────────────────
  { rel: 'en/adrenal-stress/index.html', data: {
    heading: 'How does the Adrenal Stress Profile compare to other cortisol tests?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / Adrenal Stress', 'GetTested / Female hormone test', 'Holistic Cortisol test', 'Standard blood test'],
    rows: [
      ['Cortisol data points', '4 during the day + CAR', '1 (morning)', '7 during the day', '1 (random)'],
      ['DHEA', '✓', '✓', '—', 'Separate test'],
      ['DHEA/Cortisol ratio', '✓', '—', '—', '—'],
      ['Cortisol Awakening Response (CAR)', '✓', '—', '—', '—'],
      ['Diurnal rhythm (curve)', '✓ Full curve', 'Morning value only', '✓ Full curve', '—'],
      ['Laboratory', 'Genova, CLIA-cert., USA', 'Unknown', 'ISO15189', 'Regional lab'],
      ['Physician interpretation', '✓ Always included', '—', '—', 'Via referral'],
      ['Price', 'SEK 2,100', 'Included in package ~SEK 1,500', '~SEK 1,200', 'SEK 0–200'],
    ],
    closing: 'A single morning cortisol measurement tells you nothing about the diurnal rhythm. It is the curve — how cortisol rises, peaks and declines through the day — that reveals whether the HPA axis is functioning normally.',
  }},

  // ── Women's Health+ SV ────────────────────────────────────────────────────
  { rel: 'kvinnohalsa/index.html', data: {
    heading: 'Vad mäter Women\'s Health+ som andra hormontest inte gör?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / Women\'s Health+', 'GetTested / Hormontest kvinna', 'Holistic / Hormontest kvinna', 'Werlabs / Hormon kvinna'],
    rows: [
      ['Könshormoner (E1, E2, E3, P4, T)', '✓', '✓ (E2, P4, T, DHEA)', '✓ (E2, P4, T, DHEA)', '✓ (E2, FSH, LH)'],
      ['Östrogenmetabolism (2-OH, 4-OH, 16-OH)', '✓', '—', '—', '—'],
      ['Kortisol (dygnskurva)', '✓', '1 mätpunkt', '1 mätpunkt', '—'],
      ['DHEA', '✓', '✓', '✓', '—'],
      ['Provtyp', 'Saliv + urin', 'Saliv', 'Saliv', 'Blod (serum)'],
      ['Laboratorium', 'Genova, CLIA-cert., USA', 'Okänt', 'ISO15189', 'Karolinska/Unilabs'],
      ['Läkartolkning', '✓ Alltid ingår', '—', '—', 'Delvis (läkarkommentar)'],
      ['Pris', '6 200 kr', '~1 500 kr', '~895 kr', '~1 000 kr'],
    ],
    closing: 'FSH och E2 i blod bekräftar att menopaus sker. De förklarar inte varför en kvinna har svåra symtom och en annan inga alls vid samma hormonnivåer. Östrogenmetabolism är den saknade pusselbit.',
  }},

  // ── Women's Health+ EN ────────────────────────────────────────────────────
  { rel: 'en/womens-health/index.html', data: {
    heading: 'What does Women\'s Health+ measure that other hormone tests miss?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / Women\'s Health+', 'GetTested / Female hormone test', 'Holistic / Female hormone test', 'Werlabs / Female hormones'],
    rows: [
      ['Sex hormones (E1, E2, E3, P4, T)', '✓', '✓ (E2, P4, T, DHEA)', '✓ (E2, P4, T, DHEA)', '✓ (E2, FSH, LH)'],
      ['Oestrogen metabolism (2-OH, 4-OH, 16-OH)', '✓', '—', '—', '—'],
      ['Cortisol (diurnal curve)', '✓', '1 data point', '1 data point', '—'],
      ['DHEA', '✓', '✓', '✓', '—'],
      ['Sample type', 'Saliva + urine', 'Saliva', 'Saliva', 'Blood (serum)'],
      ['Laboratory', 'Genova, CLIA-cert., USA', 'Unknown', 'ISO15189', 'Karolinska/Unilabs'],
      ['Physician interpretation', '✓ Always included', '—', '—', 'Partial (physician comment)'],
      ['Price', 'SEK 6,200', '~SEK 1,500', '~SEK 895', '~SEK 1,000'],
    ],
    closing: 'FSH and E2 in blood confirm that menopause is happening. They do not explain why one woman has severe symptoms and another has none at the same hormone levels. Oestrogen metabolism is the missing piece.',
  }},

  // ── Essential Östrogen SV ─────────────────────────────────────────────────
  { rel: 'essential-ostrogen/index.html', data: {
    heading: 'Essential Estrogens™ — det enda testet av sitt slag i Sverige',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / Essential Estrogens™', 'GetTested', 'Werlabs / Östrogen', 'Standard blodprov'],
    rows: [
      ['Mäter östrogenmetabolism', '✓ (8 metaboliter)', '—', '—', '—'],
      ['2-OH-metaboliter (skyddande)', '✓', '—', '—', '—'],
      ['4-OH-metaboliter (potentiellt skadliga)', '✓', '—', '—', '—'],
      ['16-OH-metaboliter', '✓', '—', '—', '—'],
      ['COMT methyleringsaktivitet', '✓', '—', '—', '—'],
      ['2/16-kvot (cancerriskmått)', '✓', '—', '—', '—'],
      ['Östrogennivåer (E1, E2, E3)', '✓', '—', '✓', '✓ (E2)'],
      ['Laboratorium', 'Genova, CLIA-cert., USA', '—', 'Karolinska', 'Regionlab'],
      ['Läkartolkning', '✓ Alltid ingår', '—', 'Delvis', 'Via remiss'],
      ['Pris', '6 800 kr', 'Ej tillgängligt', '~500 kr', '0–200 kr'],
    ],
    closing: 'Ingen annan aktör i Sverige mäter östrogenmetabolism. Det är den enda informationen som avgör om ditt östrogen bryts ned via skyddande eller skadliga vägar — och som är avgörande för riskbedömning vid hormonbehandling.',
  }},

  // ── Essential Estrogens EN ────────────────────────────────────────────────
  { rel: 'en/essential-estrogens/index.html', data: {
    heading: 'Essential Estrogens™ — the only test of its kind in Sweden',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / Essential Estrogens™', 'GetTested', 'Werlabs / Oestrogen', 'Standard blood test'],
    rows: [
      ['Measures oestrogen metabolism', '✓ (8 metabolites)', '—', '—', '—'],
      ['2-OH metabolites (protective)', '✓', '—', '—', '—'],
      ['4-OH metabolites (potentially harmful)', '✓', '—', '—', '—'],
      ['16-OH metabolites', '✓', '—', '—', '—'],
      ['COMT methylation activity', '✓', '—', '—', '—'],
      ['2/16 ratio (cancer risk marker)', '✓', '—', '—', '—'],
      ['Oestrogen levels (E1, E2, E3)', '✓', '—', '✓', '✓ (E2)'],
      ['Laboratory', 'Genova, CLIA-cert., USA', '—', 'Karolinska', 'Regional lab'],
      ['Physician interpretation', '✓ Always included', '—', 'Partial', 'Via referral'],
      ['Price', 'SEK 6,800', 'Not available', '~SEK 500', 'SEK 0–200'],
    ],
    closing: 'No other provider in Sweden measures oestrogen metabolism. It is the only information that determines whether your oestrogen is broken down via protective or harmful pathways — and is critical for risk assessment with hormone therapy.',
  }},

  // ── Menopaus Plus SV ──────────────────────────────────────────────────────
  { rel: 'menopaus-plus/index.html', data: {
    heading: 'Vad gör Menopause Plus™ mer komplett än andra menopaustest?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / Menopause Plus™', 'GetTested / Menopaustest', 'Werlabs / Klimakterietest', 'Medisera / Klimakterietest'],
    rows: [
      ['Könshormoner (E1, E2, E3, P4, T)', '✓ (saliv)', 'FSH snabbtest (urin)', 'E2 + FSH (blod)', 'E2 + FSH + AMH (blod)'],
      ['Melatonin (3 mätpunkter)', '✓', '—', '—', '—'],
      ['Kortisol', '✓', '—', '—', '—'],
      ['DHEA', '✓', '—', '—', '—'],
      ['Östrogenmetabolism', '✓', '—', '—', '—'],
      ['P/E2-kvot', '✓', '—', '—', '—'],
      ['Terapeutiska referensvärden', '✓ (bioidentisk HRT kohort)', '—', '—', '—'],
      ['Läkartolkning', '✓ Alltid ingår', '—', 'Läkarkommentar', 'Läkarkommentar'],
      ['Pris', '9 300 kr', '~200 kr (snabbtest)', '~800 kr', '~1 200 kr'],
    ],
    closing: 'Ett FSH-snabbtest bekräftar att du är i klimakteriet. Menopause Plus™ berättar varför du mår som du gör — och vad som kan göras åt det.',
  }},

  // ── Menopause Plus EN ─────────────────────────────────────────────────────
  { rel: 'en/menopause-plus/index.html', data: {
    heading: 'What makes Menopause Plus™ more complete than other menopause tests?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / Menopause Plus™', 'GetTested / Menopause test', 'Werlabs / Menopause test', 'Medisera / Menopause test'],
    rows: [
      ['Sex hormones (E1, E2, E3, P4, T)', '✓ (saliva)', 'FSH rapid test (urine)', 'E2 + FSH (blood)', 'E2 + FSH + AMH (blood)'],
      ['Melatonin (3 data points)', '✓', '—', '—', '—'],
      ['Cortisol', '✓', '—', '—', '—'],
      ['DHEA', '✓', '—', '—', '—'],
      ['Oestrogen metabolism', '✓', '—', '—', '—'],
      ['P/E2 ratio', '✓', '—', '—', '—'],
      ['Therapeutic reference ranges', '✓ (bioidentical HRT cohort)', '—', '—', '—'],
      ['Physician interpretation', '✓ Always included', '—', 'Physician comment', 'Physician comment'],
      ['Price', 'SEK 9,300', '~SEK 200 (rapid test)', '~SEK 800', '~SEK 1,200'],
    ],
    closing: 'A FSH rapid test confirms you are in menopause. Menopause Plus™ tells you why you feel the way you do — and what can be done about it.',
  }},

  // ── Metabolomix+ SV ───────────────────────────────────────────────────────
  { rel: 'metabolomik/index.html', data: {
    heading: 'Metabolomix+ eller NutrEval — vad är skillnaden?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / Metabolomix+', 'MediBalans / NutrEval®', 'GetTested / Organic Acids', 'Standard urinprov'],
    rows: [
      ['Provtyp', 'Urin (FMV)', 'Blod + urin', 'Urin', 'Urin'],
      ['Antal biomarkörer', '125+', '125+', '21', '5–10'],
      ['Fettsyror i blod', 'Tillval (Bloodspot)', '✓', '—', '—'],
      ['Passar om', 'Du vill undvika blodprov', 'Komplett bild önskas', 'Enkel screening', 'Infektion/njurfunktion'],
      ['Laboratorium', 'Genova, CLIA-cert., USA', 'Genova, CLIA-cert., USA', 'Okänt', 'Regionlab'],
      ['Läkartolkning', '✓ Alltid ingår', '✓ Alltid ingår', '—', 'Via remiss'],
      ['Pris', '8 100 kr', '12 200 kr', '~1 500 kr', '0 kr (remiss)'],
    ],
    closing: 'Metabolomix+ och NutrEval mäter i princip samma saker. Välj Metabolomix+ om du vill undvika blodprov. Välj NutrEval om du vill ha fettsyreprofilen i blod inkluderad från start.',
  }},

  // ── Metabolomics EN ───────────────────────────────────────────────────────
  { rel: 'en/metabolomics/index.html', data: {
    heading: 'Metabolomix+ or NutrEval — what is the difference?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / Metabolomix+', 'MediBalans / NutrEval®', 'GetTested / Organic Acids', 'Standard urine test'],
    rows: [
      ['Sample type', 'Urine (FMV)', 'Blood + urine', 'Urine', 'Urine'],
      ['Biomarkers', '125+', '125+', '21', '5–10'],
      ['Blood fatty acids', 'Add-on (Bloodspot)', '✓', '—', '—'],
      ['Best suited for', 'Avoiding blood draw', 'Complete picture desired', 'Basic screening', 'Infection/kidney function'],
      ['Laboratory', 'Genova, CLIA-cert., USA', 'Genova, CLIA-cert., USA', 'Unknown', 'Regional lab'],
      ['Physician interpretation', '✓ Always included', '✓ Always included', '—', 'Via referral'],
      ['Price', 'SEK 8,100', 'SEK 12,200', '~SEK 1,500', 'SEK 0 (referral)'],
    ],
    closing: 'Metabolomix+ and NutrEval measure essentially the same things. Choose Metabolomix+ if you want to avoid a blood draw. Choose NutrEval if you want the blood fatty acid profile included from the start.',
  }},

  // ── MethylDetox SV ────────────────────────────────────────────────────────
  { rel: 'methyldetox/index.html', data: {
    heading: 'Hur skiljer sig MethylDetox från vanliga MTHFR-tester?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / MethylDetox', 'GetTested / DNA Hormone Health', 'Werlabs / MTHFR', 'Standard genetiktest'],
    rows: [
      ['Antal gener', '38 SNPs', '~12 hormongener', '1–2 (MTHFR C677T, A1298C)', '1'],
      ['Metyleringsvägen', '✓ Komplett (MTHFR, MTR, MTRR, COMT, CBS, BHMT m.fl.)', 'Hormoner, ej methylering', 'MTHFR endast', 'MTHFR endast'],
      ['COMT (östrogenmetabolism)', '✓', '—', '—', '—'],
      ['Avgiftningsgener', '✓ (CYP, NQO1, NAT1)', '—', '—', '—'],
      ['Neurotransmittorgener (MAO)', '✓', '—', '—', '—'],
      ['Klinisk tolkning', '✓ Alltid ingår', '—', 'Läkarkommentar', '—'],
      ['Livstidsgiltigt', '✓ (DNA förändras ej)', '✓', '✓', '✓'],
      ['Pris', 'Ingår i paketet', '1 599 kr', '~400 kr', '200–500 kr'],
    ],
    closing: 'MTHFR-test svarar på en fråga. MethylDetox svarar på 38. Methylering är ett nätverk av enzymer — att testa ett gen är som att kontrollera en länk i en kedja på 38.',
  }},

  // ── MethylDetox EN ────────────────────────────────────────────────────────
  { rel: 'en/methylation-test/index.html', data: {
    heading: 'How does MethylDetox compare to standard MTHFR tests?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / MethylDetox', 'GetTested / DNA Hormone Health', 'Werlabs / MTHFR', 'Standard genetic test'],
    rows: [
      ['Genes analysed', '38 SNPs', '~12 hormone genes', '1–2 (MTHFR C677T, A1298C)', '1'],
      ['Methylation pathway', '✓ Complete (MTHFR, MTR, MTRR, COMT, CBS, BHMT etc.)', 'Hormones, not methylation', 'MTHFR only', 'MTHFR only'],
      ['COMT (oestrogen metabolism)', '✓', '—', '—', '—'],
      ['Detoxification genes', '✓ (CYP, NQO1, NAT1)', '—', '—', '—'],
      ['Neurotransmitter genes (MAO)', '✓', '—', '—', '—'],
      ['Clinical interpretation', '✓ Always included', '—', 'Physician comment', '—'],
      ['Lifetime validity', '✓ (DNA does not change)', '✓', '✓', '✓'],
      ['Price', 'Included in package', 'SEK 1,599', '~SEK 400', 'SEK 200–500'],
    ],
    closing: 'An MTHFR test answers one question. MethylDetox answers 38. Methylation is a network of enzymes — testing one gene is like checking one link in a chain of 38.',
  }},

  // ── Alzheimers SV ─────────────────────────────────────────────────────────
  { rel: 'alzheimers-test/index.html', data: {
    heading: 'Hur skiljer sig Alzheimer\'s Assessment från standard demensutredning?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['MediBalans / Alzheimer\'s Assessment', 'Standard primärvård', 'Werlabs / Kognitiv hälsa', 'GetTested'],
    rows: [
      ['p-tau217 blodprov', '✓', '—', '—', '—'],
      ['APOE4 genotypning', '✓', '—', '—', '—'],
      ['Tidig diagnos (4–7 år före symtom)', '✓', '—', '—', '—'],
      ['Kognitiv screening (MMSE)', '—', '✓', '✓', '—'],
      ['Biomarkör för amyloidpatologi', '✓', '—', '—', '—'],
      ['Neurologisk remiss vid positivt svar', '✓', '✓', '—', '—'],
      ['Läkartolkning', '✓ Alltid ingår', 'Via remiss', 'Läkarkommentar', '—'],
      ['Pris', '6 500 kr', '0 kr (remiss krävs)', '~800 kr', 'Ej tillgängligt'],
    ],
    closing: 'Standardvård utreder demens när symtom redan är tydliga. p-tau217 kan identifiera Alzheimers biologiska process 4–7 år innan minnesproblem uppstår. Det är skillnaden mellan att reagera och att förebygga.',
  }},

  // ── Alzheimers EN ─────────────────────────────────────────────────────────
  { rel: 'en/alzheimers-assessment/index.html', data: {
    heading: 'How does the Alzheimer\'s Assessment compare to standard dementia screening?',
    sub: 'A fact-based comparison.',
    cols: ['MediBalans / Alzheimer\'s Assessment', 'Standard primary care', 'Werlabs / Cognitive health', 'GetTested'],
    rows: [
      ['p-tau217 blood test', '✓', '—', '—', '—'],
      ['APOE4 genotyping', '✓', '—', '—', '—'],
      ['Early diagnosis (4–7 years before symptoms)', '✓', '—', '—', '—'],
      ['Cognitive screening (MMSE)', '—', '✓', '✓', '—'],
      ['Amyloid pathology biomarker', '✓', '—', '—', '—'],
      ['Neurology referral on positive result', '✓', '✓', '—', '—'],
      ['Physician interpretation', '✓ Always included', 'Via referral', 'Physician comment', '—'],
      ['Price', 'SEK 6,500', 'SEK 0 (referral required)', '~SEK 800', 'Not available'],
    ],
    closing: 'Standard care investigates dementia when symptoms are already clear. p-tau217 can identify Alzheimer\'s biological process 4–7 years before memory problems emerge. That is the difference between reacting and preventing.',
  }},

  // ── Genova Diagnostics SV ─────────────────────────────────────────────────
  { rel: 'genova-diagnostics/index.html', data: {
    heading: 'Varför är Genova Diagnostics det ledande valet inom funktionsmedicin?',
    sub: 'En faktabaserad jämförelse.',
    cols: ['Genova Diagnostics (MediBalans)', 'GetTested', 'Holistic Hälsotest', 'Nordic Labs'],
    rows: [
      ['Grundat', '1986', '2016', '2000-tal', '2010-tal'],
      ['Certifiering', 'CLIA-cert., USA', 'ISO (labb okänt)', 'ISO15189', 'CE-certifierat'],
      ['Testmetoder', 'PCR, MALDI-TOF, LC-MS/MS, GC/MS, EIA, LIA', 'ELISA, qPCR', 'EIA, odling', 'ELISA, LC-MS'],
      ['Kliniska domäner', 'Tarm, näring, hormoner, genetik, metabolomik', 'Tarm, hormoner, näring', 'Hormoner, tarm', 'Hormoner, näring'],
      ['Peer-reviewed forskning', '✓ Extensiv', 'Begränsad', 'Begränsad', 'Begränsad'],
      ['Läkartolkning', '✓ Alltid via MediBalans', '—', '20 min näringsterapeut', 'Tillval'],
      ['Tillgänglig i Sverige', '✓ MediBalans — officiell distributör', '✓', '✓', '✓'],
      ['Pris', 'Varierar per test', 'Lägre', 'Lägre', 'Lägre'],
    ],
    closing: 'MediBalans är officiell svensk distributör av Genova Diagnostics sedan 2026. Genova-tester kan inte beställas via något annat företag i Sverige.',
  }},

  // ── Genova Diagnostics EN ─────────────────────────────────────────────────
  { rel: 'en/genova-diagnostics/index.html', data: {
    heading: 'Why is Genova Diagnostics the leading choice in functional medicine?',
    sub: 'A fact-based comparison.',
    cols: ['Genova Diagnostics (MediBalans)', 'GetTested', 'Holistic Health tests', 'Nordic Labs'],
    rows: [
      ['Founded', '1986', '2016', '2000s', '2010s'],
      ['Certification', 'CLIA-cert., USA', 'ISO (lab unknown)', 'ISO15189', 'CE-certified'],
      ['Test methods', 'PCR, MALDI-TOF, LC-MS/MS, GC/MS, EIA, LIA', 'ELISA, qPCR', 'EIA, culture', 'ELISA, LC-MS'],
      ['Clinical domains', 'Gut, nutrition, hormones, genetics, metabolomics', 'Gut, hormones, nutrition', 'Hormones, gut', 'Hormones, nutrition'],
      ['Peer-reviewed research', '✓ Extensive', 'Limited', 'Limited', 'Limited'],
      ['Physician interpretation', '✓ Always via MediBalans', '—', '20 min nutritionist', 'Add-on'],
      ['Available in Sweden', '✓ MediBalans — official distributor', '✓', '✓', '✓'],
      ['Price', 'Varies by test', 'Lower', 'Lower', 'Lower'],
    ],
    closing: 'MediBalans has been the official Swedish distributor of Genova Diagnostics since 2026. Genova tests cannot be ordered through any other provider in Sweden.',
  }},

];

// ─── RUN ─────────────────────────────────────────────────────────────────────

let updated = 0, skipped = 0;

for (const { rel, data } of TABLES) {
  const html = buildTable(data);
  const ok = inject(rel, html);
  if (ok) { console.log(`  ✓  ${rel}`); updated++; }
  else { skipped++; }
}

console.log(`\n══ DONE: ${updated} updated · ${skipped} skipped ══`);
