#!/usr/bin/env node
// update_nav.mjs — inserts 5 new Genova test items into nav dropdowns across all pages.
// Run from medibalans-website root: node update_nav.mjs

import { readFileSync, writeFileSync } from 'fs';
import { globSync } from 'fs';
import { join, resolve } from 'path';
import { readdirSync, statSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname);

// ── SV: items to insert after /genova-hormontest/ in desktop nav ──────────────
const SV_DESKTOP_ANCHOR = `<a href="/genova-hormontest/">Hormonpaneler</a>`;
const SV_DESKTOP_NEW = `<a href="/genova-hormontest/">Hormonpaneler</a>
          <a href="/organix/">Organix&#174;</a>
          <a href="/fettsyror/">Fettsyror</a>
          <a href="/adrenal-stress/">Adrenal Stress</a>
          <a href="/essential-ostrogen/">Essential Östrogen</a>
          <a href="/menopaus-plus/">Menopaus Plus</a>`;

// ── SV: items to insert after /genova-hormontest/ in mobile nav ───────────────
const SV_MOBILE_ANCHOR = `<a href="/genova-hormontest/" onclick="closeMobile()" class="sub">Hormonpaneler</a>`;
const SV_MOBILE_NEW = `<a href="/genova-hormontest/" onclick="closeMobile()" class="sub">Hormonpaneler</a>
  <a href="/organix/" onclick="closeMobile()" class="sub">Organix&#174;</a>
  <a href="/fettsyror/" onclick="closeMobile()" class="sub">Fettsyror</a>
  <a href="/adrenal-stress/" onclick="closeMobile()" class="sub">Adrenal Stress</a>
  <a href="/essential-ostrogen/" onclick="closeMobile()" class="sub">Essential Östrogen</a>
  <a href="/menopaus-plus/" onclick="closeMobile()" class="sub">Menopaus Plus</a>`;

// ── EN: items to insert after /en/genova-hormones/ in desktop nav ─────────────
const EN_DESKTOP_ANCHOR = `<a href="/en/genova-hormones/">Hormonal Panels</a>`;
const EN_DESKTOP_NEW = `<a href="/en/genova-hormones/">Hormonal Panels</a>
          <a href="/en/organix/">Organix&#174;</a>
          <a href="/en/fatty-acids/">Fatty Acids</a>
          <a href="/en/adrenal-stress/">Adrenal Stress</a>
          <a href="/en/essential-estrogens/">Essential Estrogens</a>
          <a href="/en/menopause-plus/">Menopause Plus</a>`;

// ── EN: items to insert after /en/genova-hormones/ in mobile nav ──────────────
const EN_MOBILE_ANCHOR = `<a href="/en/genova-hormones/" onclick="closeMobile()" class="sub">Hormonal Panels</a>`;
const EN_MOBILE_NEW = `<a href="/en/genova-hormones/" onclick="closeMobile()" class="sub">Hormonal Panels</a>
  <a href="/en/organix/" onclick="closeMobile()" class="sub">Organix&#174;</a>
  <a href="/en/fatty-acids/" onclick="closeMobile()" class="sub">Fatty Acids</a>
  <a href="/en/adrenal-stress/" onclick="closeMobile()" class="sub">Adrenal Stress</a>
  <a href="/en/essential-estrogens/" onclick="closeMobile()" class="sub">Essential Estrogens</a>
  <a href="/en/menopause-plus/" onclick="closeMobile()" class="sub">Menopause Plus</a>`;

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

const files = walk(ROOT);
let updated = 0, skipped = 0, noMatch = 0;

for (const filePath of files) {
  const rel = filePath.replace(ROOT, '').replace(/\\/g, '/');
  let content = readFileSync(filePath, 'utf8');

  // Skip if already has new items
  if (
    content.includes('href="/organix/"') ||
    content.includes('href="/en/organix/"')
  ) {
    skipped++;
    continue;
  }

  const isEN = rel.startsWith('/en/');
  let changed = false;

  if (isEN) {
    if (content.includes(EN_DESKTOP_ANCHOR)) {
      content = content.replace(EN_DESKTOP_ANCHOR, EN_DESKTOP_NEW);
      changed = true;
    }
    if (content.includes(EN_MOBILE_ANCHOR)) {
      content = content.replace(EN_MOBILE_ANCHOR, EN_MOBILE_NEW);
      changed = true;
    }
  } else {
    if (content.includes(SV_DESKTOP_ANCHOR)) {
      content = content.replace(SV_DESKTOP_ANCHOR, SV_DESKTOP_NEW);
      changed = true;
    }
    if (content.includes(SV_MOBILE_ANCHOR)) {
      content = content.replace(SV_MOBILE_ANCHOR, SV_MOBILE_NEW);
      changed = true;
    }
  }

  if (changed) {
    writeFileSync(filePath, content, 'utf8');
    console.log(`  updated  ${rel}`);
    updated++;
  } else {
    noMatch++;
  }
}

console.log(`\n${updated} updated · ${skipped} skipped (already had items) · ${noMatch} no-match`);
