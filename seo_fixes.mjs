#!/usr/bin/env node
// seo_fixes.mjs — runs all 5 SEO audit fixes in sequence

import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname);
const p = (rel) => resolve(ROOT, rel.replace(/\//g, '\\'));

function read(rel) { return readFileSync(p(rel), 'utf8'); }
function write(rel, content) { writeFileSync(p(rel), content, 'utf8'); }
function changed(a, b) { return a !== b; }

let totalChanges = 0;

// ─────────────────────────────────────────────────────────────────────────────
// FIX 1: Broken internal links
// ─────────────────────────────────────────────────────────────────────────────
console.log('\n══ FIX 1: Broken internal links ══');
const fix1Files = [
  'alcat/index.html',
  'biologisk-alder/index.html',
  'index.html',
  'sibo-test/index.html',
  'utredningsprotokoll/index.html',
  'en/cellular-nutrient-analysis/index.html',
];
let fix1Count = 0;
for (const rel of fix1Files) {
  let c = read(rel);
  const orig = c;
  c = c.replaceAll('href="/alcat-test/"', 'href="/alcat/"');
  c = c.replaceAll('href="/cellulara-naringsanalyser/"', 'href="/cma/"');
  if (changed(orig, c)) {
    write(rel, c);
    const n1 = (orig.match(/href="\/alcat-test\/"/g) || []).length;
    const n2 = (orig.match(/href="\/cellulara-naringsanalyser\/"/g) || []).length;
    console.log(`  fixed  ${rel}  (alcat-test:${n1} cellulara:${n2})`);
    fix1Count++;
  }
}
console.log(`  → ${fix1Count} files updated`);
totalChanges += fix1Count;

// ─────────────────────────────────────────────────────────────────────────────
// FIX 2: hreflang corrections
// ─────────────────────────────────────────────────────────────────────────────
console.log('\n══ FIX 2: hreflang corrections ══');

// Helper: insert string after first occurrence of anchor
function insertAfter(content, anchor, insertion) {
  const idx = content.indexOf(anchor);
  if (idx === -1) return content;
  return content.slice(0, idx + anchor.length) + '\n' + insertion + content.slice(idx + anchor.length);
}

const fix2 = [
  {
    rel: 'kvinnohalsa/index.html',
    anchor: '<link rel="alternate" hreflang="sv"',
    // Find full tag end and insert EN after
    fn: (c) => {
      // Find the sv hreflang line end
      const svMatch = c.match(/<link rel="alternate" hreflang="sv"[^\n]*/);
      if (!svMatch) return c;
      const svTag = svMatch[0];
      const insertEN = '<link rel="alternate" hreflang="en" href="https://www.medibalans.com/en/womens-health/">';
      return c.replace(svTag, svTag + '\n' + insertEN);
    }
  },
  {
    rel: 'nls-skanning-och-utredning/index.html',
    fn: (c) => {
      const svMatch = c.match(/<link rel="alternate" hreflang="sv"[^\n]*/);
      if (!svMatch) return c;
      const svTag = svMatch[0];
      const insertEN = '<link rel="alternate" hreflang="en" href="https://www.medibalans.com/en/nls-body-scan/">';
      return c.replace(svTag, svTag + '\n' + insertEN);
    }
  },
  {
    rel: 'en/baby-balans/index.html',
    fn: (c) => {
      // Missing both — insert after canonical
      const canonMatch = c.match(/<link rel="canonical"[^\n]*/);
      if (!canonMatch) return c;
      const canon = canonMatch[0];
      const hreflang = [
        '<link rel="alternate" hreflang="sv" href="https://www.medibalans.com/baby-balans/">',
        '<link rel="alternate" hreflang="en" href="https://www.medibalans.com/en/baby-balans/">',
      ].join('\n');
      return c.replace(canon, canon + '\n' + hreflang);
    }
  },
  {
    rel: 'en/research/index.html',
    fn: (c) => {
      // Has EN, missing SV — insert SV before EN
      const enMatch = c.match(/<link rel="alternate" hreflang="en"[^\n]*/);
      if (!enMatch) return c;
      const enTag = enMatch[0];
      const insertSV = '<link rel="alternate" hreflang="sv" href="https://www.medibalans.com/forskning.html">';
      return c.replace(enTag, insertSV + '\n' + enTag);
    }
  },
];

let fix2Count = 0;
for (const { rel, fn } of fix2) {
  const orig = read(rel);
  const updated = fn(orig);
  if (changed(orig, updated)) {
    write(rel, updated);
    console.log(`  fixed  ${rel}`);
    fix2Count++;
  } else {
    console.log(`  WARN: no change made to ${rel}`);
  }
}
console.log(`  → ${fix2Count} files updated`);
totalChanges += fix2Count;

// ─────────────────────────────────────────────────────────────────────────────
// FIX 3: Meta descriptions over 160 chars
// ─────────────────────────────────────────────────────────────────────────────
console.log('\n══ FIX 3: Meta descriptions over 160 chars ══');

function trimAt155(text) {
  if (text.length <= 160) return null; // no change needed
  let trimmed = text.substring(0, 155);
  // Find last complete word
  const lastSpace = trimmed.lastIndexOf(' ');
  if (lastSpace > 80) trimmed = trimmed.substring(0, lastSpace);
  return trimmed;
}

// Walk all HTML files
import { readdirSync, statSync } from 'fs';
function walk(dir) {
  const results = [];
  for (const entry of readdirSync(dir)) {
    const full = resolve(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) results.push(...walk(full));
    else if (entry.endsWith('.html')) results.push(full);
  }
  return results;
}

const SKIP_FILES = new Set([
  'google7dc4d048aac517b5.html',
  'readme.6e3acde722f18a16bec8d944312dc0df.html',
  'utredningsprotokol.html',
  'seo_audit.mjs', 'seo_fixes.mjs', 'update_nav.mjs',
]);

const allFiles = walk(ROOT).filter(f => !SKIP_FILES.has(f.split(/[/\\]/).pop()));

// Regex patterns for desc extraction (handles multiple attribute orders)
const DESC_PATTERNS = [
  // name= before content=
  { rx: /(<meta\s+name=["']description["']\s+content=["'])([^"']+)(["'][^>]*>)/gi, gi: 2 },
  // content= before name= (simple)
  { rx: /(<meta\s+content=["'])([^"']+)(["']\s+name=["']description["'][^>]*>)/gi, gi: 2 },
  // content= with other attrs before name=
  { rx: /(<meta\s+content=["'])([^"']+)(["'][^>]*name=["']description["'][^>]*>)/gi, gi: 2 },
];

let fix3Count = 0;
for (const filePath of allFiles) {
  const rel = filePath.replace(ROOT, '').replace(/\\/g, '/').replace(/^\//, '');
  let c = readFileSync(filePath, 'utf8');
  const orig = c;
  let fileChanged = false;

  for (const { rx, gi } of DESC_PATTERNS) {
    c = c.replace(rx, (match, pre, desc, post) => {
      const trimmed = trimAt155(desc);
      if (trimmed === null) return match; // already short enough
      fileChanged = true;
      return pre + trimmed + post;
    });
  }

  if (fileChanged) {
    writeFileSync(filePath, c, 'utf8');
    console.log(`  trimmed  ${rel}`);
    fix3Count++;
  }
}
console.log(`  → ${fix3Count} files updated`);
totalChanges += fix3Count;

// ─────────────────────────────────────────────────────────────────────────────
// FIX 4: Alt text for Facebook pixel (display:none tracking img)
// ─────────────────────────────────────────────────────────────────────────────
console.log('\n══ FIX 4: Alt text on Facebook tracking pixel ══');

// The FB pixel pattern: <img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?..."/>
const FB_PIXEL_NO_ALT = /<img\s+height="1"\s+width="1"\s+style="display:none"\s+src="https:\/\/www\.facebook\.com\/tr\?[^"]*"(?!\s+alt=)[^>]*\/>/gi;
const FB_PIXEL_REPLACE = (match) => {
  // Add alt before the closing />
  return match.replace('/>', ' alt="Facebook pixel">');
};

let fix4Count = 0;
for (const filePath of allFiles) {
  const rel = filePath.replace(ROOT, '').replace(/\\/g, '/').replace(/^\//, '');
  let c = readFileSync(filePath, 'utf8');
  const orig = c;

  c = c.replace(FB_PIXEL_NO_ALT, FB_PIXEL_REPLACE);

  if (changed(orig, c)) {
    writeFileSync(filePath, c, 'utf8');
    console.log(`  alt added  ${rel}`);
    fix4Count++;
  }
}
console.log(`  → ${fix4Count} files updated`);
totalChanges += fix4Count;

// ─────────────────────────────────────────────────────────────────────────────
// FIX 5: Schema JSON-LD missing (6 pages)
// ─────────────────────────────────────────────────────────────────────────────
console.log('\n══ FIX 5: Schema JSON-LD ══');

const SCHEMA_PAGES = [
  {
    rel: 'forskning.html',
    schema: JSON.stringify({
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "Forskningsprogram & Patentportfölj — MediBalans Stockholm",
      "description": "MediBalans driver klinisk forskning inom precisionsmedicin, regenerativa terapier och biologisk åldringsmätning.",
      "publisher": { "@type": "Organization", "name": "MediBalans AB", "url": "https://medibalans.com" }
    }),
  },
  {
    rel: 'metabolomik/index.html',
    schema: JSON.stringify({
      "@context": "https://schema.org",
      "@type": "MedicalTest",
      "name": "Metabolomix+® — Metabolomisk Näringsprofil | MediBalans",
      "description": "Genova Diagnostics Metabolomix+ mäter 125+ biomarkörer via urin. Kartlägger mitokondriell funktion, neurotransmittorsyntes och cellulär energiproduktion.",
      "usedToDiagnose": { "@type": "MedicalCondition", "name": "Näringsbrist, Mitokondriell Dysfunktion, Metabol Obalans" },
      "provider": {
        "@type": "MedicalOrganization",
        "name": "MediBalans AB",
        "address": { "@type": "PostalAddress", "streetAddress": "Birger Jarlsgatan 10", "addressLocality": "Stockholm", "postalCode": "114 34", "addressCountry": "SE" }
      }
    }),
  },
  {
    rel: 'nutreval-sverige/index.html',
    schema: JSON.stringify({
      "@context": "https://schema.org",
      "@type": "MedicalTest",
      "name": "NutrEval® — Komplett Näringsprofil | MediBalans",
      "description": "NutrEval mäter 125+ biomarkörer för näringsstatus och metabol funktion via blod och urin. Aminosyror, fettsyror, organiska syror, vitaminer och mineraler.",
      "usedToDiagnose": { "@type": "MedicalCondition", "name": "Näringsbrist, Kronisk Trötthet, Metabol Obalans" },
      "provider": {
        "@type": "MedicalOrganization",
        "name": "MediBalans AB",
        "address": { "@type": "PostalAddress", "streetAddress": "Birger Jarlsgatan 10", "addressLocality": "Stockholm", "postalCode": "114 34", "addressCountry": "SE" }
      }
    }),
  },
  {
    rel: 'en/investigation-protocol/index.html',
    schema: JSON.stringify({
      "@context": "https://schema.org",
      "@type": "MedicalWebPage",
      "name": "Investigation Protocol — MediBalans Stockholm",
      "description": "MediBalans investigation protocol: from first consultation to personalised treatment using ALCAT, CMA, MethylDetox, HRV, microbiome and multi-omics.",
      "publisher": { "@type": "MedicalOrganization", "name": "MediBalans AB", "url": "https://medibalans.com" }
    }),
  },
  {
    rel: 'en/nls-body-scan/index.html',
    schema: JSON.stringify({
      "@context": "https://schema.org",
      "@type": "MedicalWebPage",
      "name": "NLS Body Scan — MediBalans Stockholm",
      "description": "NLS body scan at MediBalans Stockholm: non-invasive full body bioresonance analysis mapping 100+ organs and tissues.",
      "publisher": { "@type": "MedicalOrganization", "name": "MediBalans AB", "url": "https://medibalans.com" }
    }),
  },
  {
    rel: 'en/research/index.html',
    schema: JSON.stringify({
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "Research Programme & Patent Portfolio — MediBalans Stockholm",
      "description": "MediBalans conducts clinical research in precision medicine, regenerative therapies and biological age measurement. 7 patents. Global Constraint Rule framework.",
      "publisher": { "@type": "Organization", "name": "MediBalans AB", "url": "https://medibalans.com" }
    }),
  },
];

let fix5Count = 0;
for (const { rel, schema } of SCHEMA_PAGES) {
  let c = read(rel);
  const orig = c;

  if (c.includes('application/ld+json')) {
    console.log(`  SKIP ${rel} (already has schema)`);
    continue;
  }

  // Insert before </head>
  const schemaTag = `<script type="application/ld+json">${schema}</script>`;
  c = c.replace('</head>', schemaTag + '\n</head>');

  if (changed(orig, c)) {
    write(rel, c);
    console.log(`  schema added  ${rel}`);
    fix5Count++;
  }
}
console.log(`  → ${fix5Count} files updated`);
totalChanges += fix5Count;

// ─────────────────────────────────────────────────────────────────────────────
console.log(`\n══ TOTAL CHANGES: ${totalChanges} files across 5 fixes ══`);
