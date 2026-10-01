// Service worker: app werkt offline na de eerste laadbeurt.
// Verhoog VERSION bij elke release zodat telefoons de nieuwe versie ophalen.
const VERSION = 'jdb-v1';
const SHELL = [
  './', 'index.html', 'manifest.json',
  'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png', 'icons/apple-touch-icon.png'
];
const PLAYERS = {
  1: ['stefen', 'arie', 'hanna-g', 'juliette', 'joost', 'gordon'],
  2: ['bert', 'renata', 'niels', 'gert', 'marcel', 'emil', 'pieter-jan'],
  3: ['myrna', 'roos', 'roxanne', 'bartjan', 'louis', 'ronnie', 'annika'],
  4: ['ardin', 'mark', 'johan', 'hanna-k', 'bart', 'abby']
};
const PHOTOS = Object.entries(PLAYERS).flatMap(([b, ns]) => ns.map(n => `players/baan${b}/${n}.jpg`));

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(VERSION);
    await c.addAll(SHELL);
    // Foto's die (nog) niet bestaan geven een 404; die slaan we gewoon over.
    await Promise.all(PHOTOS.map(u => fetch(u).then(r => r.ok && c.put(u, r)).catch(() => {})));
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== VERSION) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  e.respondWith((async () => {
    const c = await caches.open(VERSION);
    const nav = req.mode === 'navigate';
    const key = nav ? 'index.html' : req;
    const hit = await c.match(key, { ignoreSearch: true });
    const net = fetch(req).then(r => { if (r.ok) c.put(key, r.clone()); return r; }).catch(() => null);
    if (nav) {
      // De pagina zelf: liefst vers (max 3 s wachten op slechte dekking), anders uit cache.
      const quick = await Promise.race([net, new Promise(r => setTimeout(() => r(null), 3000))]);
      if (quick && quick.ok) return quick;
      if (hit) { e.waitUntil(net); return hit; }
      return (await net) || new Response('Offline', { status: 503 });
    }
    // Overige bestanden: direct uit cache, op de achtergrond verversen.
    if (hit) { e.waitUntil(net); return hit; }
    return (await net) || new Response('', { status: 404, statusText: 'offline' });
  })());
});
