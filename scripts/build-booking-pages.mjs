/**
 * Generates the per-service booking pages under /boka/<slug>/.
 *
 * Each bookable service needs its own marketing URL — a campaign can point at
 * /boka/konsultation-digitalt and land a patient on a page that books exactly
 * that, rather than dropping them on the home page next to an iframe offering
 * every appointment type the clinic has.
 *
 * The shell — head assets, nav, footer, and the whole stylesheet — is lifted
 * from an existing page rather than reimplemented, so these pages inherit the
 * site's design, its analytics, its chat widget and its nav automatically. When
 * the site's nav changes, re-run this and the booking pages follow.
 *
 *   node scripts/build-booking-pages.mjs
 *
 * Idempotent. Safe to re-run.
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const TEMPLATE = join(ROOT, "hrv-analys", "index.html");

// Must mirror app/lib/bookableServices.js in the meet-mario repo. The server
// re-resolves every slug against its own allow-list, so a mistake here produces
// a page that refuses to book rather than one that books the wrong thing.
const SERVICES = [
  {
    slug: "konsultation",
    dir: "boka/konsultation",
    title: "Boka initial konsultation — MediBalans Stockholm",
    h1: "Boka din <em>initiala konsultation</em>",
    eyebrow: "Banérgatan 10, Stockholm · Ingen remiss",
    description:
      "Boka 45 minuter med legitimerad läkare på Banérgatan 10, Stockholm. Genomgång av sjukdomshistorik, symptombild och relevanta mätningar. Ingen remiss krävs.",
    lead:
      "45 minuter med läkare på Banérgatan 10. Vi går igenom din sjukdomshistorik, din symptombild och vad som redan utretts — och vilka mätningar som faktiskt är relevanta för dig. Ingen remiss krävs.",
    answer:
      "MediBalans initiala konsultation är 45 minuter med legitimerad läkare på Banérgatan 10 i Stockholm. Ingen remiss krävs. Bokning sker direkt online.",
    canonical: "https://www.medibalans.com/boka/konsultation/",
  },
  {
    slug: "konsultation-digitalt",
    dir: "boka/konsultation-digitalt",
    title: "Boka digital konsultation — MediBalans",
    h1: "Boka din <em>digitala konsultation</em>",
    eyebrow: "Videosamtal · Hela Sverige och internationellt",
    description:
      "Boka 45 minuter med legitimerad läkare som videosamtal. Vi tar emot patienter från hela Sverige och internationellt — provtagning kan ske nära dig.",
    lead:
      "Samma 45 minuter med läkare, som videosamtal. Vi tar emot patienter från hela Sverige och internationellt, och provtagningen kan ske nära dig. Ingen remiss krävs.",
    answer:
      "MediBalans digitala konsultation är 45 minuter med legitimerad läkare via videosamtal, tillgänglig i hela Sverige och internationellt. Ingen remiss krävs.",
    canonical: "https://www.medibalans.com/boka/konsultation-digitalt/",
  },
];

const src = readFileSync(TEMPLATE, "utf8");

/** Everything from <!doctype> to the end of </head>, minus page-specific tags. */
function shellHead() {
  const head = src.slice(0, src.indexOf("</head>"));
  return (
    head
      // Drop the template's own SEO — every one of these is rewritten below.
      .replace(/<title>[\s\S]*?<\/title>/g, "")
      .replace(/<meta name="(description|keywords|answer)"[\s\S]*?>/g, "")
      .replace(/<link rel="canonical"[\s\S]*?>/g, "")
      .replace(/<link rel="alternate"[\s\S]*?>/g, "")
      .replace(/<meta property="og:(url|title|description)"[\s\S]*?>/g, "")
      // Drop the template's structured data — a booking page is not a MedicalTest.
      .replace(/<script type="application\/ld\+json">[\s\S]*?<\/script>/g, "")
  );
}

function slice(open, close) {
  const a = src.indexOf(open);
  const b = src.indexOf(close, a);
  return a === -1 || b === -1 ? "" : src.slice(a, b + close.length);
}

const NAV = slice("<nav", "</nav>");
const FOOTER = slice("<footer", "</footer>");
// Scripts after the footer: analytics, reveal observers, the chat widget.
const TAIL = src.slice(src.indexOf("</footer>") + "</footer>".length, src.indexOf("</body>"));

function page(s) {
  return `<!DOCTYPE html>
<html lang="sv">
${shellHead()}
<title>${s.title}</title>
<meta name="description" content="${s.description}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="${s.canonical}">
<meta name="answer" content="${s.answer}">
<meta property="og:type" content="website">
<meta property="og:url" content="${s.canonical}">
<meta property="og:title" content="${s.title}">
<meta property="og:description" content="${s.description}">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MedicalClinic",
  "name": "MediBalans",
  "url": "${s.canonical}",
  "telephone": "+46723195070",
  "email": "info@medibalans.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Banérgatan 10, 1 tr",
    "postalCode": "115 23",
    "addressLocality": "Stockholm",
    "addressCountry": "SE"
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "08:00",
    "closes": "17:00"
  },
  "potentialAction": {
    "@type": "ReserveAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "${s.canonical}",
      "actionPlatform": ["http://schema.org/DesktopWebPlatform","http://schema.org/MobileWebPlatform"]
    },
    "result": { "@type": "Reservation", "name": "${s.title}" }
  }
}
</script>
</head>
<body>
${NAV}

<section class="booking-section" id="booking" style="padding-top:7rem;">
  <div class="container">
    <div class="reveal">
      <div class="section-eyebrow" style="color:rgba(216,234,245,0.5);margin-bottom:1rem;">${s.eyebrow}</div>
      <h2>${s.h1}</h2>
      <p>${s.lead}</p>
    </div>
  </div>
</section>

<section id="boka" style="padding:4rem 0;">
  <div class="container" style="max-width:720px;">
    <div class="reveal" data-mb-booking data-service="${s.slug}"></div>
    <p style="margin-top:2rem;font-size:.82rem;color:var(--text-light);line-height:1.7;">
      Föredrar du att prata med oss? Ring <a href="tel:+46723195070">072-319 50 70</a>
      eller mejla <a href="mailto:info@medibalans.com">info@medibalans.com</a>.
      Vi svarar måndag–fredag 08:00–17:00.
    </p>
  </div>
</section>

${FOOTER}
${TAIL}
<script src="/assets/booking.js" defer></script>
</body>
</html>
`;
}

let n = 0;
for (const s of SERVICES) {
  const dir = join(ROOT, s.dir);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "index.html"), page(s), "utf8");
  console.log("wrote", join(s.dir, "index.html"));
  n++;
}
console.log(`\n${n} booking pages generated from ${TEMPLATE.replace(ROOT + "/", "")}`);
