// Host-conditional robots.txt: production hosts get the static file (allow + sitemap);
// every other host (calm, *.pages.dev previews) is disallowed.
const PROD = new Set(["themarginwars.com", "www.themarginwars.com"]);
export async function onRequest({ request, env }) {
  const host = new URL(request.url).hostname;
  if (PROD.has(host)) return env.ASSETS.fetch(request);
  return new Response("User-agent: *\nDisallow: /\n", { headers: { "content-type": "text/plain; charset=utf-8", "x-robots-tag": "noindex", "cache-control": "public, max-age=300" } });
}
