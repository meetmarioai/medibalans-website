// api/gone.js
//
// Vercel serverless function — returns HTTP 410 Gone for permanently
// removed URLs. Wired up via the rewrites in vercel.json.
//
// A 410 (unlike a soft 404) tells search engines the resource is
// intentionally and permanently gone, so it is dropped from the index
// faster and no ranking/association is carried onto any live page.
export default function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.status(410).end('410 Gone');
}
