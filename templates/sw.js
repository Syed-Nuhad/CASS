const CACHE_NAME = 'cass-cache-v6';
const urlsToCache = [
  'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap'
];

self.addEventListener('install', event => {
  self.skipWaiting(); // Force activation immediately
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching public static assets...');
        return cache.addAll(urlsToCache);
      })
      .catch(err => console.warn('Pre-cache warning (non-fatal):', err))
  );
});

self.addEventListener('activate', event => {
  // Purge older caches to prevent stale collisions
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting stale cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  // Only cache GET requests
  if (event.request.method !== 'GET') return;
  
  // Ignore non-http protocols (like chrome-extension://, ws://, etc.)
  if (!event.request.url.startsWith('http')) return;

  // FIX: Resolve Chrome 'only-if-cached' bug
  if (event.request.cache === 'only-if-cached' && event.request.mode !== 'same-origin') {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Cache ANY successful 200 response
        if (response && response.status === 200) {
          const resClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, resClone).catch(err => {
              console.warn('Failed to cache response in background:', event.request.url, err);
            });
          });
        }
        return response;
      })
      .catch(() => {
        // If network fails (Offline), serve from cache
        // FIX: Add { ignoreVary: true } to bypass Django's Vary: Cookie matching constraint!
        return caches.match(event.request, { ignoreSearch: true, ignoreVary: true }).then(cachedResponse => {
          if (cachedResponse) {
            return cachedResponse;
          }
          // Generic offline fallback response with status 200 (Chrome hides 503 responses with its own dino)
          return new Response('<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Offline Mode</title><style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#f8fafc;color:#64748b;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;margin:0;padding:20px;box-sizing:border-box;text-align:center}h1{color:#0f172a;margin:0 0 10px 0;font-size:24px}p{margin:0;font-size:16px}</style></head><body><h1>Connection Lost</h1><p>This portal is not available offline yet. Please load it once while online first.</p></body></html>', {
            status: 200,
            headers: new Headers({ 'Content-Type': 'text/html' })
          });
        });
      })
  );
});
