// Service Worker para Sistema ARCA Construcción
// Versión: 2.0.0
// Fecha: 2024

const CACHE_NAME = 'arca-construccion-v2.0.0';
const STATIC_CACHE = 'arca-static-v2.0.0';
const DYNAMIC_CACHE = 'arca-dynamic-v2.0.0';

// Archivos estáticos para cachear
const STATIC_FILES = [
    '/',
    '/dashboard/',
    '/static/css/global-styles.css',
    '/static/css/neostructure-theme.css',
    '/static/css/sidebar-layout.css',
    '/static/css/mobile-styles.css',
    '/static/css/neostructure-enhanced.css',
    '/static/css/user-menu.css',
    '/static/css/toast-notifications.css',
    '/static/js/pwa-diagnostic.js',
    '/static/js/pwa-register.js',
    '/static/js/dashboard-charts.js',
    '/static/manifest.json',
    '/static/images/icon-192x192-v2.png',
    '/static/images/icon-512x512-v2.png',
    '/static/images/icon-32x32.png',
    '/static/images/icon-16x16.png'
];

// URLs de la API para cachear
const API_URLS = [
    '/api/dashboard-data/',
    '/api/dashboard-intelligent-data/',
    '/api/login/'
];

// Instalar Service Worker
self.addEventListener('install', (event) => {
    console.log('🔧 Service Worker: Instalando...');
    
    event.waitUntil((async () => {
        try {
            const cache = await caches.open(STATIC_CACHE);
            console.log('📦 Service Worker: Cacheando archivos estáticos...');

            await Promise.all(
                STATIC_FILES.map(async (file) => {
                    try {
                        const response = await fetch(file, { cache: 'no-cache' });
                        if (response.ok) {
                            await cache.put(file, response.clone());
                            console.log('✅ Cacheado:', file);
                        } else {
                            console.warn('⚠️ No se pudo cachear (status):', file, response.status);
                        }
                    } catch (err) {
                        console.warn('⚠️ No se pudo cachear (fetch error):', file, err.message);
                    }
                })
            );

            console.log('✅ Service Worker: Instalación completada');
            await self.skipWaiting();
        } catch (error) {
            console.error('❌ Service Worker: Error en instalación:', error);
        }
    })());
});

// Activar Service Worker
self.addEventListener('activate', (event) => {
    console.log('🚀 Service Worker: Activando...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        // Eliminar caches antiguos
                        if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                            console.log('🗑️ Service Worker: Eliminando cache antiguo:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('✅ Service Worker: Activación completada');
                return self.clients.claim();
            })
    );
});

// Interceptar requests
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Estrategia de cache para diferentes tipos de recursos
    if (request.method === 'GET') {
        // Archivos estáticos - Cache First
        if (STATIC_FILES.includes(url.pathname) || url.pathname.startsWith('/static/')) {
            event.respondWith(cacheFirst(request, STATIC_CACHE));
        }
        // API calls - Network First
        else if (API_URLS.some(apiUrl => url.pathname.startsWith(apiUrl))) {
            event.respondWith(networkFirst(request, DYNAMIC_CACHE));
        }
        // Páginas HTML - Network First con fallback
        else if (request.headers.get('accept').includes('text/html')) {
            event.respondWith(networkFirstWithFallback(request, DYNAMIC_CACHE));
        }
        // Otros recursos - Stale While Revalidate
        else {
            event.respondWith(staleWhileRevalidate(request, DYNAMIC_CACHE));
        }
    }
});

// Estrategia: Cache First
async function cacheFirst(request, cacheName) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            console.log('📦 Service Worker: Sirviendo desde cache:', request.url);
            return cachedResponse;
        }
        
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(cacheName);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('❌ Service Worker: Error en cacheFirst:', error);
        return new Response('Error de conexión', { status: 503 });
    }
}

// Estrategia: Network First
async function networkFirst(request, cacheName) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(cacheName);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.log('📦 Service Worker: Red no disponible, sirviendo desde cache:', request.url);
        const cachedResponse = await caches.match(request);
        return cachedResponse || new Response('Contenido no disponible offline', { status: 503 });
    }
}

// Estrategia: Network First con fallback
async function networkFirstWithFallback(request, cacheName) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(cacheName);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.log('📦 Service Worker: Red no disponible, intentando cache:', request.url);
        const cachedResponse = await caches.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Fallback a página offline
        if (request.headers.get('accept').includes('text/html')) {
            return caches.match('/offline/') || new Response(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>ARCA - Sin conexión</title>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                        .offline { color: #dc3545; }
                        .retry { margin-top: 20px; }
                        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
                    </style>
                </head>
                <body>
                    <h1 class="offline">🔌 Sin conexión</h1>
                    <p>No se pudo conectar al servidor. Verifica tu conexión a internet.</p>
                    <div class="retry">
                        <button onclick="window.location.reload()">🔄 Reintentar</button>
                    </div>
                </body>
                </html>
            `, {
                headers: { 'Content-Type': 'text/html' }
            });
        }
        
        return new Response('Contenido no disponible', { status: 503 });
    }
}

// Estrategia: Stale While Revalidate
async function staleWhileRevalidate(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);
    
    const fetchPromise = fetch(request).then((networkResponse) => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    }).catch(() => cachedResponse);
    
    return cachedResponse || fetchPromise;
}

// Manejar mensajes del cliente
self.addEventListener('message', (event) => {
    const { action, data } = event.data;
    
    switch (action) {
        case 'SKIP_WAITING':
            self.skipWaiting();
            break;
            
        case 'CLEAR_CACHE':
            clearAllCaches();
            break;
            
        case 'GET_CACHE_SIZE':
            getCacheSize().then(size => {
                event.ports[0].postMessage({ cacheSize: size });
            });
            break;
            
        case 'CACHE_URLS':
            cacheUrls(data.urls);
            break;
    }
});

// Limpiar todos los caches
async function clearAllCaches() {
    console.log('🧹 Service Worker: Limpiando todos los caches...');
    const cacheNames = await caches.keys();
    await Promise.all(
        cacheNames.map(cacheName => caches.delete(cacheName))
    );
    console.log('✅ Service Worker: Caches limpiados');
}

// Obtener tamaño del cache
async function getCacheSize() {
    const cacheNames = await caches.keys();
    let totalSize = 0;
    
    for (const cacheName of cacheNames) {
        const cache = await caches.open(cacheName);
        const keys = await cache.keys();
        totalSize += keys.length;
    }
    
    return totalSize;
}

// Cachear URLs específicas
async function cacheUrls(urls) {
    console.log('📦 Service Worker: Cacheando URLs:', urls);
    const cache = await caches.open(DYNAMIC_CACHE);
    
    for (const url of urls) {
        try {
            const response = await fetch(url);
            if (response.ok) {
                await cache.put(url, response);
                console.log('✅ Service Worker: URL cacheada:', url);
            }
        } catch (error) {
            console.error('❌ Service Worker: Error cacheando URL:', url, error);
        }
    }
}

// Sincronización en segundo plano
self.addEventListener('sync', (event) => {
    console.log('🔄 Service Worker: Sincronización en segundo plano:', event.tag);
    
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

// Realizar sincronización en segundo plano
async function doBackgroundSync() {
    try {
        // Aquí puedes implementar lógica de sincronización
        // Por ejemplo, enviar datos pendientes, actualizar cache, etc.
        console.log('🔄 Service Worker: Ejecutando sincronización...');
        
        // Ejemplo: actualizar datos del dashboard
        const response = await fetch('/api/dashboard-data/');
        if (response.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            await cache.put('/api/dashboard-data/', response);
            console.log('✅ Service Worker: Datos sincronizados');
        }
    } catch (error) {
        console.error('❌ Service Worker: Error en sincronización:', error);
    }
}

// Notificaciones push (si se implementan en el futuro)
self.addEventListener('push', (event) => {
    console.log('📱 Service Worker: Notificación push recibida');
    
    const options = {
        body: event.data ? event.data.text() : 'Nueva notificación de ARCA',
        icon: '/static/images/icon-192x192-v2.png',
        badge: '/static/images/icon-32x32.png',
        vibrate: [200, 100, 200],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'Ver detalles',
                icon: '/static/images/icon-32x32.png'
            },
            {
                action: 'close',
                title: 'Cerrar',
                icon: '/static/images/icon-32x32.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('Sistema ARCA', options)
    );
});

// Manejar clics en notificaciones
self.addEventListener('notificationclick', (event) => {
    console.log('👆 Service Worker: Clic en notificación');
    
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/dashboard/')
        );
    }
});

console.log('🚀 Service Worker: Cargado y listo');
