#!/usr/bin/env node
// gen_sitemap.mjs — regenerate sitemap.xml from all index.html files

import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { resolve, join } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname);
const BASE = 'https://medibalans.com';

// Pages to exclude from sitemap
const SKIP_DIRS = new Set([
  'node_modules',
]);

// Pages that are utility/orphan — include but at low priority
const LOW_PRIORITY = new Set([
  'en-clinical-notes',    // orphan folder (en/clinical-notes is canonical)
  'clinical-notes',
  'en/clinical-notes',
]);

// Pages to omit entirely (redirect stubs, verifications)
const OMIT = new Set([
  // none for index.html files — forskning.html handled separately
]);

function walk(dir, results = []) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      if (!SKIP_DIRS.has(entry)) walk(full, results);
    } else if (entry === 'index.html') {
      results.push(full);
    }
  }
  return results;
}

// Collect all index.html paths
const allFiles = walk(ROOT).sort();

// Convert to URL paths
function toUrlPath(filePath) {
  const rel = filePath.replace(ROOT, '').replace(/\\/g, '/').replace(/^\//, '');
  // rel is like "alcat/index.html" or "en/alcat-test/index.html"
  if (rel === 'index.html') return '/';
  return '/' + rel.replace(/index\.html$/, '');
}

// Priority assignment
function priority(urlPath) {
  if (urlPath === '/' || urlPath === '/en/') return '1.0';
  const dir = urlPath.replace(/\//g, '');
  if (LOW_PRIORITY.has(dir) || LOW_PRIORITY.has(urlPath.replace(/^\//, '').replace(/\/$/, ''))) return '0.6';
  return '0.8';
}

// Changefreq
function changefreq(urlPath) {
  if (urlPath === '/' || urlPath === '/en/') return 'weekly';
  const p = urlPath.replace(/\//g, '');
  if (p === 'clinicalnotes' || p === 'enclinicalnotes') return 'weekly';
  return 'monthly';
}

// Collect URLs
const urls = [];

// Add forskning.html separately (not an index.html)
urls.push({
  loc: `${BASE}/forskning.html`,
  changefreq: 'monthly',
  priority: '0.8',
});

for (const filePath of allFiles) {
  const urlPath = toUrlPath(filePath);
  urls.push({
    loc: `${BASE}${urlPath}`,
    changefreq: changefreq(urlPath),
    priority: priority(urlPath),
  });
}

// Sort: homepages first, SV before EN, alphabetical within groups
urls.sort((a, b) => {
  const pa = a.loc.replace(BASE, '');
  const pb = b.loc.replace(BASE, '');
  // homepages first
  if (pa === '/') return -1;
  if (pb === '/') return 1;
  if (pa === '/en/') return -1;
  if (pb === '/en/') return 1;
  // forskning.html
  if (pa.includes('forskning')) return -1;
  if (pb.includes('forskning')) return 1;
  // SV before EN
  const aIsEN = pa.startsWith('/en/');
  const bIsEN = pb.startsWith('/en/');
  if (!aIsEN && bIsEN) return -1;
  if (aIsEN && !bIsEN) return 1;
  return pa.localeCompare(pb);
});

// Build XML
const lines = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  '',
];

for (const { loc, changefreq: cf, priority: pri } of urls) {
  lines.push('  <url>');
  lines.push(`    <loc>${loc}</loc>`);
  lines.push(`    <changefreq>${cf}</changefreq>`);
  lines.push(`    <priority>${pri}</priority>`);
  lines.push('  </url>');
  lines.push('');
}

lines.push('</urlset>');

const xml = lines.join('\n');
writeFileSync(resolve(ROOT, 'sitemap.xml'), xml, 'utf8');

console.log(`Generated sitemap.xml with ${urls.length} URLs`);
for (const { loc } of urls) {
  console.log(`  ${loc}`);
}
