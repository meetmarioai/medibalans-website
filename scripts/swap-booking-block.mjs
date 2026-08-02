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

const IFRAME_HTML = (id) =>
  `        <iframe id='cliniko-${id}' src='https://medibalans.eu1.cliniko.com/bookings?embedded=true&locale=sv' frameborder='0' scrolling='auto' width='100%' height='1000' style='pointer-events: auto;'></iframe>
<script type='text/javascript'>
  window.addEventListener('message', function handleIFrameMessage (e) {
    var clinikoBookings = document.getElementById('cliniko-${id}');
    if (typeof e.data !== 'string') return;
    if (e.data.search('cliniko-bookings-resize') > -1) {
      var height = Number(e.data.split(':')[1]);
      clinikoBookings.style.height = height + 'px';
    }
    e.data.search('cliniko-bookings-page') > -1 && clinikoBookings.scrollIntoView();
  });
</script>`;

const args = process.argv.slice(2);
const apply = args.includes("--apply");
const revert = args.includes("--revert");

let changed = 0;
let skipped = 0;

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
    const out = html.replace(
      new RegExp(`[ \\t]*<div ${MARKER}[^>]*></div>\\s*<script src="/assets/booking\\.js" defer></script>`),
      IFRAME_HTML("53063409")
    );
    if (out === html) {
      console.error(`  FAILED   ${page} — block found but not replaced`);
      process.exitCode = 1;
      continue;
    }
    if (apply) writeFileSync(path, out, "utf8");
    console.log(`  revert   ${page}`);
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

  const out = html.replace(IFRAME_RE, blockFor(page));
  if (apply) writeFileSync(path, out, "utf8");
  console.log(`  swap     ${page}  → data-service="${slugFor(page)}"`);
  changed++;
}

console.log(
  `\n${apply ? "WROTE" : "DRY RUN"} — ${changed} page(s) ${revert ? "reverted" : "swapped"}, ${skipped} unchanged.`
);
if (!apply) console.log("Re-run with --apply to write.");
