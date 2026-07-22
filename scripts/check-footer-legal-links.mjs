#!/usr/bin/env node
// check-footer-legal-links.mjs
// Guards against legal-link regressions across the static site.
// Flags: (a) a known legal label whose href is NOT its canonical page
//        (placeholder "#", "/#", "/en/#", or wrong path); and
//        (b) any legal-ish anchor text we don't have a canonical mapping for
//        (so a new/renamed label can't silently slip through unlinked).
// Exit code 1 if any issue is found — usable in CI / pre-deploy.
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url))); // repo root (scripts/..)

// Exact label -> canonical href. Extend when a new legal page is added.
const CANONICAL = {
  'Villkor': '/villkor/',
  'Integritetspolicy': '/integritetspolicy/',
  'Terms': '/en/terms/',
  'Privacy Policy': '/en/privacy-policy/',
};
// Anchor text that LOOKS legal — anything matching this but not in CANONICAL
// is reported as "unmapped" so it gets a home before it ships.
const LEGALISH = /\b(villkor|användarvillkor|integritetspolicy|dataskydd|personuppgift|terms|privacy|cookies?|gdpr)\b/i;

function* walk(dir) {
  for (const e of readdirSync(dir)) {
    if (e === 'node_modules' || e === '.git' || e === '.vercel') continue;
    const p = `${dir}/${e}`;
    const s = statSync(p);
    if (s.isDirectory()) yield* walk(p);
    else if (e.endsWith('.html')) yield p;
  }
}

const anchor = /<a\s+[^>]*href="([^"]*)"[^>]*>([^<]*)<\/a>/gi;
const mismatches = [], unmapped = [];

for (const file of walk(ROOT)) {
  const src = readFileSync(file, 'utf8');
  const rel = file.slice(ROOT.length + 1);
  let m;
  while ((m = anchor.exec(src)) !== null) {
    const href = m[1].trim();
    const text = m[2].trim();
    if (!text) continue;
    const line = src.slice(0, m.index).split('\n').length;
    if (CANONICAL[text] !== undefined) {
      if (href !== CANONICAL[text]) mismatches.push({ rel, line, text, href, expected: CANONICAL[text] });
    } else if (LEGALISH.test(text)) {
      unmapped.push({ rel, line, text, href });
    }
  }
}

if (mismatches.length) {
  console.log(`\n✗ ${mismatches.length} legal link(s) point to the wrong href:`);
  for (const x of mismatches) console.log(`  ${x.rel}:${x.line}  "${x.text}" -> ${x.href}  (expected ${x.expected})`);
}
if (unmapped.length) {
  console.log(`\n⚠ ${unmapped.length} legal-ish label(s) with no canonical mapping (add to CANONICAL or fix text):`);
  for (const x of unmapped) console.log(`  ${x.rel}:${x.line}  "${x.text}" -> ${x.href}`);
}
if (!mismatches.length && !unmapped.length) {
  console.log('✓ all legal links point to their canonical page; no unmapped legal-ish labels.');
  process.exit(0);
}
process.exit(1);
