const CACHE_NAME = 'cass-cache-v1';
const urlsToCache = [
  '/',
  '/app/',
  '/driver/',
  'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  // Only cache GET requests (HTML pages and static assets)
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    fetch(event.request).then(response => {
      // Clone and cache the new response on success
      const resClone = response.clone();
      caches.open(CACHE_NAME).then(cache => cache.put(event.request, resClone));
      return response;
    }).catch(() => {
      // If network fails (Offline), serve from cache
      return caches.match(event.request);
    })
  );
});
