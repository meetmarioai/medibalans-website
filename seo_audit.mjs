#!/usr/bin/env node
// seo_audit.mjs — SEO audit for all HTML pages

import { readFileSync, readdirSync, statSync } from 'fs';
import { join, resolve } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname);

// Skip non-content files
const SKIP = new Set([
  'google7dc4d048aac517b5.html',
  'readme.6e3acde722f18a16bec8d944312dc0df.html',
  'utredningsprotokol.html', // old typo redirect stub
]);

// Old/broken internal link patterns to flag
const BROKEN_PATTERNS = [
  '/alcat-test/',
  '/cellulara-naringsanalyser/',
  '/cellular-naringsanalyser/',
  '/nutreval/',           // should be /nutreval-sverige/ or /en/nutreval-test/
];

function walk(dir) {
  const results = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      results.push(...walk(full));
    } else if (entry.endsWith('.html')) {
      results.push(full);
    }
  }
  return results;
}

function extract(content, regex) {
  const m = content.match(regex);
  return m ? m[1] : null;
}

function auditFile(filePath) {
  const rel = filePath.replace(ROOT, '').replace(/\\/g, '/');
  const filename = rel.replace(/^\//, '');

  if (SKIP.has(filename.split('/').pop())) {
    return null; // skip
  }

  const content = readFileSync(filePath, 'utf8');

  // 1. Meta title
  const title = extract(content, /<title[^>]*>([^<]+)<\/title>/i);
  const title_ok = title ? 'yes' : 'MISSING';

  // 2. Meta description
  const descMatch = content.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/i)
    || content.match(/<meta\s+content=["']([^"']+)["']\s+name=["']description["']/i);
  const desc = descMatch ? descMatch[1] : null;
  let desc_ok;
  if (!desc) desc_ok = 'MISSING';
  else if (desc.length > 160) desc_ok = `LONG(${desc.length})`;
  else desc_ok = 'yes';

  // 3. Canonical
  const canonical = extract(content, /<link\s+rel=["']canonical["']\s+href=["']([^"']+)["']/i)
    || extract(content, /<link\s+href=["']([^"']+)["']\s+rel=["']canonical["']/i);
  const canonical_ok = canonical ? 'yes' : 'MISSING';

  // 4. hreflang
  const isEN = rel.startsWith('/en/');
  const hreflangMatches = [...content.matchAll(/hreflang=["']([^"']+)["']\s+href=["']([^"']+)["']/gi)];
  const hreflangMatches2 = [...content.matchAll(/href=["']([^"']+)["'][^>]*hreflang=["']([^"']+)["']/gi)];
  const allHreflang = [
    ...hreflangMatches.map(m => ({ lang: m[1], href: m[2] })),
    ...hreflangMatches2.map(m => ({ lang: m[2], href: m[1] })),
  ];
  // Deduplicate by lang
  const hreflangMap = {};
  for (const h of allHreflang) hreflangMap[h.lang] = h.href;

  let hreflang_ok;
  if (Object.keys(hreflangMap).length === 0) {
    hreflang_ok = 'MISSING';
  } else {
    const hasSV = 'sv' in hreflangMap;
    const hasEN = 'en' in hreflangMap;
    if (!hasSV || !hasEN) {
      hreflang_ok = `PARTIAL(${Object.keys(hreflangMap).join(',')})`;
    } else {
      // Check cross-linking makes sense
      const svHref = hreflangMap['sv'];
      const enHref = hreflangMap['en'];
      // EN pages should link to /en/... for EN href
      // SV pages should link to / ... (not /en/) for SV href
      const svOk = svHref && !svHref.includes('/en/');
      const enOk = enHref && enHref.includes('/en/');
      hreflang_ok = (svOk && enOk) ? 'yes' : `CHECK(sv:${svHref},en:${enHref})`;
    }
  }

  // 5. Schema JSON-LD
  const schema_ok = content.includes('application/ld+json') ? 'yes' : 'none';

  // 6. H1 count
  const h1matches = [...content.matchAll(/<h1[^>]*>/gi)];
  const h1count = h1matches.length;
  const h1_ok = h1count === 1 ? 'yes' : h1count === 0 ? 'MISSING' : `MULTI(${h1count})`;

  // 7. Alt text — find all <img> tags and check for alt attribute
  const imgTags = [...content.matchAll(/<img\b[^>]*>/gi)];
  const imgsMissingAlt = imgTags.filter(m => {
    const tag = m[0];
    return !(/\balt\s*=/i.test(tag));
  });
  const alt_ok = imgsMissingAlt.length === 0
    ? (imgTags.length === 0 ? 'no-imgs' : 'yes')
    : `MISSING(${imgsMissingAlt.length}/${imgTags.length})`;

  // 8. Broken/old internal links
  const brokenFound = [];
  for (const pat of BROKEN_PATTERNS) {
    if (content.includes(pat)) brokenFound.push(pat);
  }
  const broken_links = brokenFound.length > 0 ? brokenFound.join('; ') : 'ok';

  return {
    filename,
    title: title ? title.substring(0, 60) + (title.length > 60 ? '...' : '') : 'MISSING',
    title_ok,
    desc_ok,
    canonical_ok,
    hreflang_ok,
    schema_ok,
    h1_ok,
    alt_ok,
    broken_links,
  };
}

const files = walk(ROOT).sort();
const results = files.map(f => auditFile(f)).filter(Boolean);

// CSV header
const fields = ['filename','title_ok','desc_ok','canonical_ok','hreflang_ok','schema_ok','h1_ok','alt_ok','broken_links'];
console.log(fields.join(','));

for (const r of results) {
  const row = fields.map(f => {
    const v = String(r[f] || '');
    // Quote if contains comma
    return v.includes(',') ? `"${v}"` : v;
  });
  console.log(row.join(','));
}

// Summary
console.log('\n--- SUMMARY ---');
const total = results.length;
const counts = {
  title_missing: results.filter(r => r.title_ok !== 'yes').length,
  desc_missing_or_long: results.filter(r => r.desc_ok !== 'yes').length,
  canonical_missing: results.filter(r => r.canonical_ok !== 'yes').length,
  hreflang_issues: results.filter(r => r.hreflang_ok !== 'yes').length,
  schema_none: results.filter(r => r.schema_ok === 'none').length,
  h1_issues: results.filter(r => r.h1_ok !== 'yes').length,
  alt_issues: results.filter(r => !['yes','no-imgs'].includes(r.alt_ok)).length,
  broken_links: results.filter(r => r.broken_links !== 'ok').length,
};

console.log(`Total pages audited: ${total}`);
for (const [k, v] of Object.entries(counts)) {
  if (v > 0) console.log(`  ${k}: ${v} pages`);
}
if (Object.values(counts).every(v => v === 0)) {
  console.log('  All checks pass.');
}

// Detail for any failures
const failures = results.filter(r =>
  r.title_ok !== 'yes' ||
  r.desc_ok !== 'yes' ||
  r.canonical_ok !== 'yes' ||
  r.hreflang_ok !== 'yes' ||
  r.h1_ok !== 'yes' ||
  !['yes','no-imgs'].includes(r.alt_ok) ||
  r.broken_links !== 'ok'
);
if (failures.length > 0) {
  console.log('\n--- ISSUES DETAIL ---');
  for (const r of failures) {
    const issues = [];
    if (r.title_ok !== 'yes') issues.push(`title:${r.title_ok}`);
    if (r.desc_ok !== 'yes') issues.push(`desc:${r.desc_ok}`);
    if (r.canonical_ok !== 'yes') issues.push(`canonical:${r.canonical_ok}`);
    if (r.hreflang_ok !== 'yes') issues.push(`hreflang:${r.hreflang_ok}`);
    if (r.h1_ok !== 'yes') issues.push(`h1:${r.h1_ok}`);
    if (!['yes','no-imgs'].includes(r.alt_ok)) issues.push(`alt:${r.alt_ok}`);
    if (r.broken_links !== 'ok') issues.push(`broken:${r.broken_links}`);
    console.log(`  ${r.filename}: ${issues.join(' | ')}`);
  }
}
