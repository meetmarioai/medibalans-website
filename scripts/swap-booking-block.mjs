/**
 * Replaces the embedded Cliniko iframe with the native booking block.
 *
 *   node scripts/swap-booking-block.mjs            # dry run — shows the diff, writes nothing
 *   node scripts/swap-booking-block.mjs --apply    # writes
 *   node scripts/swap-booking-block.mjs --revert   # puts the iframe back
 *
 * Idempotent in both directions. Run it twice and nothing happens the second time.
 *
 * ── Why a script and not seven hand edits ───────────────────────────────────
 *
 * The iframe appears on seven pages, four Swedish and three English, and the
 * markup around it differs slightly on each. Editing them by hand is how one
 * page ends up with two booking widgets or none. This also makes the change
 * reversible in one command, which matters because it is a live revenue path:
 * if the block misbehaves the recovery is `--revert` and a push, not a scramble
 * through seven files at 22:00.
 *
 * The English pages get data-lang="en" via their own <html lang>, which
 * booking.js already reads — no separate handling needed here.
 */
import { readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

/**
 * The five pages carrying an EMBEDDED Cliniko iframe.
 *
 * Two further pages reference Cliniko and are deliberately not here, because
 * they are a different change:
 *
 *   kroppsskanning/index.html                — a LINK, "Öppna bokningskalendern"
 *   en/body-composition-analysis/index.html  — a LINK, "Open the booking calendar"
 *
 * Both send the visitor to Cliniko's own hosted page rather than embedding it.
 * The Swedish one can be repointed at /boka/konsultation whenever; the English
 * one has nowhere to go until an English booking page exists, since
 * /boka/konsultation is lang="sv". Repointing one and not the other would leave
 * the site inconsistent in a way a visitor would notice, so both wait.
 */
const PAGES = [
  "index.html",
  "iv-terapi/index.html",
  "baby-balans/index.html",
  "en/index.html",
  "en/iv-therapy/index.html",
];

/**
 * The iframe plus its resize listener. Matched as one block so a page cannot
 * end up with the listener still bound to an element that no longer exists.
 */
const IFRAME_RE =
  /[ \t]*<iframe id='cliniko-\d+'[\s\S]*?<\/iframe>\s*<script type='text\/javascript'>[\s\S]*?<\/script>/;

const MARKER = "data-mb-booking";

/** Slug per page. Everything currently books the in-person consultation. */
function slugFor(page) {
  return page.startsWith("en/") || page.includes("/en/")
    ? "konsultation"
    : "konsultation";
}

const blockFor = (page) =>
  `        <div ${MARKER} data-service="${slugFor(page)}"></div>
        <script src="/assets/booking.js" defer></script>`;

/**
 * Where the removed iframes are kept so --revert can restore them EXACTLY.
 *
 * The first version of this script reconstructed the iframe from a hardcoded
 * template on revert. That was wrong twice over, and both only surfaced because
 * the files were diffed against production:
 *
 *   - the English pages use a DIFFERENT Cliniko widget, cliniko-80483102 with
 *     locale=en. Reverting wrote the Swedish widget's id and locale into both,
 *     so an English visitor would have been shown a Swedish booking form.
 *   - baby-balans had no leading indentation on its iframe; the template added
 *     eight spaces.
 *
 * A revert that quietly changes the thing it restores is worse than no revert,
 * because it is trusted in exactly the moment nobody has time to check it. So
 * nothing is reconstructed now: the original block is stashed verbatim at swap
 * time and written back byte for byte.
 *
 * Kept in a sidecar rather than an HTML comment so production pages carry no
 * dead markup.
 */
const BACKUP = join(ROOT, "scripts", ".iframe-backup.json");

function readBackup() {
  try {
    return JSON.parse(readFileSync(BACKUP, "utf8"));
  } catch {
    return {};
  }
}

const args = process.argv.slice(2);
const apply = args.includes("--apply");
const revert = args.includes("--revert");

let changed = 0;
let skipped = 0;
const backup = readBackup();

for (const page of PAGES) {
  const path = join(ROOT, page);
  let html;
  try {
    html = readFileSync(path, "utf8");
  } catch {
    console.error(`  MISSING  ${page}`);
    process.exitCode = 1;
    continue;
  }

  if (revert) {
    if (!html.includes(MARKER)) {
      console.log(`  skip     ${page} — already on the iframe`);
      skipped++;
      continue;
    }
    const original = backup[page];
    if (typeof original !== "string" || !original.includes("<iframe")) {
      console.error(
        `  FAILED   ${page} — no stashed original in scripts/.iframe-backup.json. ` +
        `Restore with: git checkout -- ${page}`
      );
      process.exitCode = 1;
      continue;
    }
    const out = html.replace(
      new RegExp(`[ \\t]*<div ${MARKER}[^>]*></div>\\s*<script src="/assets/booking\\.js" defer></script>`),
      () => original // function form: $-sequences in the HTML are not substitutions
    );
    if (out === html) {
      console.error(`  FAILED   ${page} — block found but not replaced`);
      process.exitCode = 1;
      continue;
    }
    if (apply) writeFileSync(path, out, "utf8");
    console.log(`  revert   ${page} — restored verbatim from backup`);
    changed++;
    continue;
  }

  if (html.includes(MARKER)) {
    console.log(`  skip     ${page} — already swapped`);
    skipped++;
    continue;
  }
  if (!IFRAME_RE.test(html)) {
    console.error(`  FAILED   ${page} — no Cliniko iframe found. Do not push; inspect by hand.`);
    process.exitCode = 1;
    continue;
  }

  // Stash the exact bytes being removed BEFORE removing them. This is what
  // makes --revert lossless; without it the restore is a guess.
  const [originalBlock] = html.match(IFRAME_RE);
  backup[page] = originalBlock;

  const out = html.replace(IFRAME_RE, () => blockFor(page));
  if (apply) writeFileSync(path, out, "utf8");
  const id = originalBlock.match(/cliniko-(\d+)/)?.[1] ?? "?";
  const loc = originalBlock.match(/locale=([a-z]+)/)?.[1] ?? "?";
  console.log(`  swap     ${page}  → data-service="${slugFor(page)}"   (stashed cliniko-${id}, locale=${loc})`);
  changed++;
}

// Written after the loop so a partial run cannot leave a backup that claims
// more than it holds.
if (apply && !revert && changed > 0) {
  writeFileSync(BACKUP, JSON.stringify(backup, null, 2), "utf8");
  console.log(`\nstashed ${Object.keys(backup).length} original block(s) in scripts/.iframe-backup.json`);
}

console.log(
  `\n${apply ? "WROTE" : "DRY RUN"} — ${changed} page(s) ${revert ? "reverted" : "swapped"}, ${skipped} unchanged.`
);
if (!apply) console.log("Re-run with --apply to write.");
