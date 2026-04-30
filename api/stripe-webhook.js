// api/stripe-webhook.js
//
// Vercel serverless function — Stripe webhook → Meta Conversions API (Purchase)
// Pixel: 836514963742786 (MediBalans)
//
// Receives checkout.session.completed events, filters to Genova test purchases only,
// hashes PII per Meta CAPI requirements, fires server-side Purchase event.
//
// Filtering precedence (most specific wins):
//   1. mode === 'payment'         (rejects platform subscriptions — required)
//   2. payment_link in whitelist  (set GENOVA_STRIPE_PAYMENT_LINKS env var)
//   3. metadata.genova_test === 'true'
//   4. amount_total matches a known Genova price (fallback)
//
// Env vars (set in Vercel project settings → Environment Variables):
//   STRIPE_SECRET_KEY              sk_live_... or sk_test_...
//   STRIPE_WEBHOOK_SECRET          whsec_... — from Stripe Dashboard webhook endpoint
//   META_PIXEL_ID                  836514963742786
//   META_CAPI_ACCESS_TOKEN         EAA... — from Events Manager → Conversions API → Generate token
//   GENOVA_STRIPE_PAYMENT_LINKS    plink_xxx,plink_yyy,...   (optional but recommended)
//   META_TEST_EVENT_CODE           TEST12345 — TEMPORARY, remove before going live

import Stripe from 'stripe';
import crypto from 'crypto';

export const config = {
  api: {
    // Stripe signature verification needs the raw body — disable Vercel's JSON parser
    bodyParser: false
  }
};

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2024-06-20'
});

// Graph API v22.0 — v19.0 sunsets May 21, 2026
const GRAPH_API_VERSION = 'v22.0';

// Known Genova prices (SEK) → product info. Used for content_name enrichment
// and as the last-resort filter fallback when no whitelist/metadata is set.
const PRICE_TO_PRODUCT = {
  8500:  { name: 'GI Effects',           id: 'gi-effects' },
  12200: { name: 'NutrEval FMV',         id: 'nutreval' },
  8100:  { name: 'Metabolomix+',         id: 'metabolomix' },
  3700:  { name: 'SIBO Andningstest',    id: 'sibo' },
  6200:  { name: "Women's Health+",      id: 'womens-health' },
  6500:  { name: 'Alzheimers-utredning', id: 'alzheimers' }
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
  // Strip everything but digits — Meta wants E.164-style digits only
  const digits = String(value).replace(/[^\d]/g, '');
  if (!digits) return undefined;
  return crypto.createHash('sha256').update(digits).digest('hex');
}

function isGenovaTestPurchase(session) {
  // Filter 1: must be a one-time payment (rejects platform subscriptions)
  if (session.mode !== 'payment') return false;

  // Filter 2: payment-link whitelist (preferred — most reliable)
  if (GENOVA_PAYMENT_LINKS.length > 0) {
    if (session.payment_link && GENOVA_PAYMENT_LINKS.includes(session.payment_link)) {
      return true;
    }
    // Whitelist is configured but this session doesn't match → reject
    // (this is what makes the whitelist a hard gate when set)
    return false;
  }

  // Filter 3: explicit metadata flag (set on Payment Link in Stripe Dashboard)
  if (session.metadata && session.metadata.genova_test === 'true') return true;

  // Filter 4: known Genova price match (fallback when no whitelist/metadata configured)
  // Stripe amounts are in smallest currency unit (öre for SEK), so divide by 100
  const total = (session.amount_total || 0) / 100;
  if (PRICE_TO_PRODUCT[total]) return true;

  return false;
}

function buildUserData(session) {
  const customer = session.customer_details || {};
  const address = customer.address || {};

  // Split full name into first / last for Meta's fn / ln fields
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
    // fbp/fbc are Meta browser/click cookies. Currently undefined (Step 1.7 enhancement
    // adds capture via Stripe Checkout Session metadata). Match quality drops 10-25%
    // without them but funnel still works.
    fbp: session.metadata?.fbp,
    fbc: session.metadata?.fbc,
    client_ip_address: session.metadata?.client_ip,
    client_user_agent: session.metadata?.client_user_agent
  };

  // Strip undefined keys — Meta rejects payloads with explicit nulls in user_data
  Object.keys(userData).forEach((k) => {
    if (userData[k] === undefined) delete userData[k];
  });

  return userData;
}

function buildEventPayload(session) {
  const total = (session.amount_total || 0) / 100;
  const currency = (session.currency || 'sek').toUpperCase();
  const product = PRICE_TO_PRODUCT[total] || { name: 'Genova test', id: 'genova-unknown' };

  // Use the client_reference_id stamped on the Stripe URL by pixel-events.html
  // as the CAPI event_id. Lets Meta dedupe browser InitiateCheckout (same event_id)
  // against server Purchase, and traces the same user through the funnel.
  const eventId = session.client_reference_id || `mb_purchase_${session.id}`;

  // event_source_url should reflect where the conversion conceptually originated.
  // Falls back to medibalans.com root when we don't have the test-page URL stashed
  // in metadata. Step 1.7 enhancement: pass test-page URL through metadata.
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

  let parsed;
  try {
    parsed = JSON.parse(responseText);
  } catch {
    parsed = { raw: responseText };
  }

  return parsed;
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

  // Only act on completed checkouts
  if (event.type !== 'checkout.session.completed') {
    return res.status(200).json({ received: true, skipped: event.type });
  }

  const session = event.data.object;

  // Filter to Genova test purchases only — meet-mario.ai platform subscriptions
  // share this Stripe account but must not fire Purchase on the medibalans pixel
  if (!isGenovaTestPurchase(session)) {
    console.log(
      `[stripe-webhook] non-Genova session ${session.id} ` +
      `(mode=${session.mode}, amount=${session.amount_total}, payment_link=${session.payment_link}) ` +
      `— skipping CAPI`
    );
    return res.status(200).json({ received: true, skipped: 'non_genova' });
  }

  let capiResult;
  try {
    const payload = buildEventPayload(session);
    capiResult = await sendToMetaCapi(payload);
    console.log(
      `[stripe-webhook] CAPI Purchase fired for session ${session.id} ` +
      `event_id=${payload.event_id} → ${JSON.stringify(capiResult)}`
    );
  } catch (err) {
    // Log but don't 5xx — Stripe retries on 5xx and we don't want loops if Meta
    // is degraded. The webhook fired correctly; Meta-side issues are non-fatal.
    console.error(
      `[stripe-webhook] CAPI send failed for session ${session.id}:`,
      err.message
    );
  }

  return res.status(200).json({
    received: true,
    capi: capiResult ? 'sent' : 'failed',
    session: session.id
  });
}
