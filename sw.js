const CACHE_NAME = 'pwa-music-player-cache-v1';
const ASSETS_TO_CACHE = [
  '/', // Alias for index.html for the root path
  '/index.html',
  '/style.css',
  '/app.js',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
  // Removed comments about adding paths later as they are now added.
  // The comment "For now, assume icons might be linked externally or added later to cache" is also removed.
];

// Install event: Cache core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching app shell assets');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .catch(error => {
        console.error('Service Worker: Failed to cache app shell assets during install:', error);
      })
  );
});

// Activate event: Clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      // Ensure the new service worker takes control immediately once activated.
      return self.clients.claim();
    })
  );
});

// Fetch event: Serve cached assets first (Cache-First strategy for app shell)
self.addEventListener('fetch', event => {
  // We only want to cache GET requests for our app shell assets
  if (event.request.method !== 'GET') {
    return;
  }

  // For navigation requests (HTML pages), try network first, then cache, then offline page (optional)
  // For other assets (CSS, JS, images), use cache-first.
  // This example uses a simpler cache-first for specified assets.
  
  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        // Cache hit - return response from cache
        if (cachedResponse) {
          return cachedResponse;
        }

        // Not found in cache, fetch from network
        // Optionally, you could cache new requests here too, but for app shell, explicit caching on install is common.
        return fetch(event.request).then(networkResponse => {
            // Optionally cache dynamically fetched resources if needed
            // For example, if you want to cache images or other assets loaded on demand:
            /*
            if (networkResponse && networkResponse.status === 200) {
                const responseToCache = networkResponse.clone();
                caches.open(CACHE_NAME)
                    .then(cache => {
                        cache.put(event.request, responseToCache);
                    });
            }
            */
            return networkResponse;
        }).catch(error => {
            console.error('Service Worker: Fetch failed; returning offline fallback or error for:', event.request.url, error);
            // Optionally, return an offline fallback page here if one is cached:
            // if (event.request.mode === 'navigate') {
            //   return caches.match('/offline.html');
            // }
            // Or just let the browser handle the error for non-essential resources.
        });
      })
  );
});
