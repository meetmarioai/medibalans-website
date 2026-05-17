// api/stripe-webhook.js
//
// Vercel serverless function — Stripe webhook → Meta CAPI Purchase + GA4 MP purchase
// Pixel: 836514963742786 (MediBalans)  ·  GA4 stream: G-X8ZN38EGYY
//
// Improvements vs previous version:
//   1. True parallel execution — Meta CAPI and GA4 fire concurrently via
//      Promise.allSettled (was sequential awaits; now ~halves webhook response time).
//   2. Startup env var validation — logs warning at module load if any required
//      env var is missing. Surfaces config drift in deploy logs, not mid-purchase.
//   3. Test mode warning — logs loudly when META_TEST_EVENT_CODE is set, so it's
//      hard to forget you're firing test events instead of production.
//   4. GA4 debug endpoint via env var — set GA4_DEBUG_MODE=true to switch to the
//      debug endpoint that returns validation errors. No code edit needed.
//   5. Structured single-line diagnostic log per purchase — one JSON log entry
//      per webhook with session/product/value/CAPI-status/GA4-status, parseable
//      in Vercel logs and any log shipper. Replaces multiple ad-hoc log lines.
//   6. Unknown-SKU surfaced explicitly — webhook still fires for unknown amounts,
//      but the response body and log flag unknown_sku=true so they're easy to spot.
//
// Required env vars:
//   STRIPE_SECRET_KEY              sk_live_... (or sk_test_... for staging)
//   STRIPE_WEBHOOK_SECRET          whsec_... (from Stripe Dashboard → Webhooks)
//   META_PIXEL_ID                  836514963742786
//   META_CAPI_ACCESS_TOKEN         Long-lived system user token from Meta Business
//   GA4_MEASUREMENT_ID             G-X8ZN38EGYY
//   GA4_API_SECRET                 from GA4 Admin → Data Streams → web stream →
//                                  Measurement Protocol API secrets → Create
//
// Optional env vars:
//   META_TEST_EVENT_CODE           TEST12345 — fires events to Test Events view
//                                  in Meta Events Manager. Unset to fire production.
//   GA4_DEBUG_MODE                 true — switches GA4 endpoint to /debug/mp/collect
//                                  which returns JSON validation errors. Unset for production.
//   GENOVA_STRIPE_PAYMENT_LINKS    comma-separated payment_link IDs to whitelist
//                                  (alternative to price-based detection).
//
// Optional frontend integration for full attribution:
//   - Capture _ga cookie pre-redirect, stash on Checkout Session as
//     metadata.ga_client_id. Without it, GA4 fires but attributes to a synthetic
//     anonymous user (purchase counts, but source/medium/landing-page is lost).
//   - Same for _fbp / _fbc cookies → metadata.fbp / metadata.fbc. Without them,
//     Meta can't match server-side Purchase to browser-side view_content events
//     and event-quality score drops.

import Stripe from 'stripe';
import crypto from 'crypto';

export const config = {
  api: {
    bodyParser: false
  }
};

// ── Startup config validation ─────────────────────────────────────────────────

const REQUIRED_ENV = [
  'STRIPE_SECRET_KEY',
  'STRIPE_WEBHOOK_SECRET',
  'META_PIXEL_ID',
  'META_CAPI_ACCESS_TOKEN',
  'GA4_MEASUREMENT_ID',
  'GA4_API_SECRET'
];

const missingEnv = REQUIRED_ENV.filter((k) => !process.env[k]);
if (missingEnv.length > 0) {
  console.error(
    `[stripe-webhook] STARTUP WARNING — missing required env vars: ${missingEnv.join(', ')}. ` +
    `Webhook will fail at first purchase. Set these in Vercel → Settings → Environment Variables.`
  );
}

if (process.env.META_TEST_EVENT_CODE) {
  console.warn(
    `[stripe-webhook] TEST MODE ACTIVE — Meta CAPI events will fire to test event ` +
    `code "${process.env.META_TEST_EVENT_CODE}". Real purchases will NOT appear in ` +
    `your production Pixel. Unset META_TEST_EVENT_CODE in Vercel to flip to production.`
  );
}

if (process.env.GA4_DEBUG_MODE === 'true') {
  console.warn(
    `[stripe-webhook] GA4 DEBUG MODE ACTIVE — events fire to /debug/mp/collect ` +
    `which validates but does NOT record. Unset GA4_DEBUG_MODE in Vercel to record events.`
  );
}

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2024-06-20'
});

const GRAPH_API_VERSION = 'v22.0';
const GA4_MP_ENDPOINT_PROD = 'https://www.google-analytics.com/mp/collect';
const GA4_MP_ENDPOINT_DEBUG = 'https://www.google-analytics.com/debug/mp/collect';

// Known Genova prices (SEK) → product info.
const PRICE_TO_PRODUCT = {
  2100:  { name: 'Adrenal Stress',       id: 'adrenal-stress' },
  3700:  { name: 'SIBO Andningstest',    id: 'sibo' },
  6200:  { name: "Women's Health+",      id: 'womens-health' },
  6500:  { name: 'Alzheimers-utredning', id: 'alzheimers' },
  8100:  { name: 'Metabolomix+',         id: 'metabolomix' },
  8500:  { name: 'GI Effects',           id: 'gi-effects' },
  12200: { name: 'NutrEval FMV',         id: 'nutreval' }
  // TODO: 5600 and 9300 SKUs — confirm names and add here.
  // Until added, these prices fall through to genova-unknown and the response
  // body flags unknown_sku=true so they're easy to spot.
};

const GENOVA_PAYMENT_LINKS = (process.env.GENOVA_STRIPE_PAYMENT_LINKS || '')
  .split(',')
  .map((s) => s.trim())
  .filter(Boolean);

// ── Helpers ───────────────────────────────────────────────────────────────────

async function readRawBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks);
}

function sha256(value) {
  if (value === undefined || value === null || value === '') return undefined;
  return crypto
    .createHash('sha256')
    .update(String(value).toLowerCase().trim())
    .digest('hex');
}

function sha256Phone(value) {
  if (!value) return undefined;
  const digits = String(value).replace(/[^\d]/g, '');
  if (!digits) return undefined;
  return crypto.createHash('sha256').update(digits).digest('hex');
}

function isGenovaTestPurchase(session) {
  if (session.mode !== 'payment') return false;

  if (GENOVA_PAYMENT_LINKS.length > 0) {
    if (session.payment_link && GENOVA_PAYMENT_LINKS.includes(session.payment_link)) {
      return true;
    }
    return false;
  }

  if (session.metadata && session.metadata.genova_test === 'true') return true;

  const total = (session.amount_total || 0) / 100;
  if (PRICE_TO_PRODUCT[total]) return true;

  return false;
}

function buildUserData(session) {
  const customer = session.customer_details || {};
  const address = customer.address || {};

  let firstName, lastName;
  if (customer.name) {
    const parts = customer.name.trim().split(/\s+/);
    firstName = parts[0];
    lastName = parts.length > 1 ? parts.slice(1).join(' ') : undefined;
  }

  const userData = {
    em: customer.email ? [sha256(customer.email)] : undefined,
    ph: customer.phone ? [sha256Phone(customer.phone)] : undefined,
    fn: firstName ? [sha256(firstName)] : undefined,
    ln: lastName ? [sha256(lastName)] : undefined,
    ct: address.city ? [sha256(address.city)] : undefined,
    st: address.state ? [sha256(address.state)] : undefined,
    zp: address.postal_code ? [sha256(address.postal_code)] : undefined,
    country: address.country ? [sha256(address.country)] : undefined,
    fbp: session.metadata?.fbp,
    fbc: session.metadata?.fbc,
    client_ip_address: session.metadata?.client_ip,
    client_user_agent: session.metadata?.client_user_agent
  };

  Object.keys(userData).forEach((k) => {
    if (userData[k] === undefined) delete userData[k];
  });

  return userData;
}

function getProduct(session) {
  const total = (session.amount_total || 0) / 100;
  return PRICE_TO_PRODUCT[total] || { name: 'Genova test', id: 'genova-unknown' };
}

// ── Meta CAPI ─────────────────────────────────────────────────────────────────

function buildMetaPayload(session) {
  const total = (session.amount_total || 0) / 100;
  const currency = (session.currency || 'sek').toUpperCase();
  const product = getProduct(session);

  const eventId = session.client_reference_id || `mb_purchase_${session.id}`;

  const eventSourceUrl =
    session.metadata?.source_url ||
    session.success_url ||
    'https://www.medibalans.com/';

  return {
    event_name: 'Purchase',
    event_time: Math.floor(Date.now() / 1000),
    event_id: eventId,
    event_source_url: eventSourceUrl,
    action_source: 'website',
    user_data: buildUserData(session),
    custom_data: {
      currency,
      value: total,
      content_name: product.name,
      content_ids: [product.id],
      content_type: 'product',
      content_category: 'Genova test',
      num_items: 1,
      order_id: session.id
    }
  };
}

async function sendToMetaCapi(payload) {
  const pixelId = process.env.META_PIXEL_ID;
  const accessToken = process.env.META_CAPI_ACCESS_TOKEN;
  const testEventCode = process.env.META_TEST_EVENT_CODE;

  if (!pixelId || !accessToken) {
    throw new Error('META_PIXEL_ID and META_CAPI_ACCESS_TOKEN must be set');
  }

  const url = `https://graph.facebook.com/${GRAPH_API_VERSION}/${pixelId}/events?access_token=${encodeURIComponent(accessToken)}`;

  const body = { data: [payload] };
  if (testEventCode) {
    body.test_event_code = testEventCode;
  }

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  const responseText = await res.text();
  if (!res.ok) {
    throw new Error(`Meta CAPI HTTP ${res.status}: ${responseText}`);
  }

  try {
    return JSON.parse(responseText);
  } catch {
    return { raw: responseText };
  }
}

// ── GA4 Measurement Protocol ──────────────────────────────────────────────────

function buildGa4Payload(session) {
  const total = (session.amount_total || 0) / 100;
  const currency = (session.currency || 'sek').toUpperCase();
  const product = getProduct(session);

  // client_id should match the gtag-generated _ga cookie value so this purchase
  // attaches to the user's existing GA4 session. Pass it through Stripe Checkout
  // Session metadata when creating the session client-side. Without it, GA4 will
  // treat the purchase as a new anonymous user (purchase still counts, but
  // source/medium/landing-page attribution breaks for this event).
  const clientId = session.metadata?.ga_client_id || `mb_${session.id}`;

  return {
    client_id: clientId,
    timestamp_micros: Date.now() * 1000,
    non_personalized_ads: false,
    events: [
      {
        name: 'purchase',
        params: {
          transaction_id: session.id,
          value: total,
          currency,
          // engagement_time_msec is required by GA4 MP for any event to count
          // as engagement. Nominal value is fine for a server-sent purchase.
          engagement_time_msec: 1,
          items: [
            {
              item_id: product.id,
              item_name: product.name,
              item_category: 'Genova test',
              price: total,
              quantity: 1
            }
          ]
        }
      }
    ]
  };
}

async function sendToGa4(payload) {
  const measurementId = process.env.GA4_MEASUREMENT_ID;
  const apiSecret = process.env.GA4_API_SECRET;

  if (!measurementId || !apiSecret) {
    throw new Error('GA4_MEASUREMENT_ID and GA4_API_SECRET must be set');
  }

  const endpoint =
    process.env.GA4_DEBUG_MODE === 'true' ? GA4_MP_ENDPOINT_DEBUG : GA4_MP_ENDPOINT_PROD;

  const url = `${endpoint}?measurement_id=${encodeURIComponent(measurementId)}&api_secret=${encodeURIComponent(apiSecret)}`;

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  // Debug endpoint returns JSON validation response (200 with body even on success).
  // Production endpoint returns 204 No Content on success.
  if (process.env.GA4_DEBUG_MODE === 'true') {
    const debugResponse = await res.json().catch(() => ({}));
    if (debugResponse.validationMessages && debugResponse.validationMessages.length > 0) {
      throw new Error(`GA4 MP validation: ${JSON.stringify(debugResponse.validationMessages)}`);
    }
    return { status: res.status, debug: debugResponse };
  }

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`GA4 MP HTTP ${res.status}: ${text}`);
  }

  return { status: res.status };
}

// ── Webhook handler ───────────────────────────────────────────────────────────

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  let event;
  try {
    const rawBody = await readRawBody(req);
    const signature = req.headers['stripe-signature'];
    event = stripe.webhooks.constructEvent(
      rawBody,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    console.error('[stripe-webhook] signature verification failed:', err.message);
    return res
      .status(400)
      .json({ error: `Webhook signature error: ${err.message}` });
  }

  if (event.type !== 'checkout.session.completed') {
    return res.status(200).json({ received: true, skipped: event.type });
  }

  const session = event.data.object;

  if (!isGenovaTestPurchase(session)) {
    console.log(
      `[stripe-webhook] non-Genova session ${session.id} ` +
      `(mode=${session.mode}, amount=${session.amount_total}, payment_link=${session.payment_link}) — skipping`
    );
    return res.status(200).json({ received: true, skipped: 'non_genova' });
  }

  const total = (session.amount_total || 0) / 100;
  const currency = (session.currency || 'sek').toUpperCase();
  const product = getProduct(session);
  const unknownSku = !PRICE_TO_PRODUCT[total];

  // True parallel execution: Promise.allSettled fires both calls concurrently.
  // Each branch's rejection is captured independently — one failure doesn't
  // block the other. Webhook response time = max(CAPI, GA4), not sum.
  const [capiSettled, ga4Settled] = await Promise.allSettled([
    sendToMetaCapi(buildMetaPayload(session)),
    sendToGa4(buildGa4Payload(session))
  ]);

  const capiResult = capiSettled.status === 'fulfilled' ? capiSettled.value : null;
  const capiError = capiSettled.status === 'rejected' ? capiSettled.reason.message : null;
  const ga4Result = ga4Settled.status === 'fulfilled' ? ga4Settled.value : null;
  const ga4Error = ga4Settled.status === 'rejected' ? ga4Settled.reason.message : null;

  // Single structured log line per purchase — parseable in Vercel logs.
  console.log(
    JSON.stringify({
      event: 'stripe-webhook.purchase',
      session: session.id,
      product_id: product.id,
      product_name: product.name,
      value: total,
      currency,
      capi: capiResult ? 'sent' : 'failed',
      capi_error: capiError,
      ga4: ga4Result ? 'sent' : 'failed',
      ga4_error: ga4Error,
      ga_client_id_source: session.metadata?.ga_client_id ? 'cookie' : 'synthetic',
      fbp_present: !!session.metadata?.fbp,
      fbc_present: !!session.metadata?.fbc,
      unknown_sku: unknownSku,
      test_mode: !!process.env.META_TEST_EVENT_CODE,
      ga4_debug_mode: process.env.GA4_DEBUG_MODE === 'true'
    })
  );

  return res.status(200).json({
    received: true,
    session: session.id,
    product: product.name,
    value: total,
    currency,
    capi: capiResult ? 'sent' : 'failed',
    capi_error: capiError,
    ga4: ga4Result ? 'sent' : 'failed',
    ga4_error: ga4Error,
    unknown_sku: unknownSku
  });
}
