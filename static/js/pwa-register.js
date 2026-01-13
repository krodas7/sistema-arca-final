// Script de registro de PWA para Sistema ARCA Construcción
class PWARegister {
    constructor() {
        this.serviceWorkerPath = '/service-worker.js';
        this.isRegistered = false;
        this.registration = null;
    }

    // Registrar Service Worker
    async registerServiceWorker() {
        if (!('serviceWorker' in navigator)) {
            console.error('❌ Service Worker no soportado en este navegador');
            return false;
        }

        try {
            console.log('🔧 Registrando Service Worker...');
            
            this.registration = await navigator.serviceWorker.register(this.serviceWorkerPath);

            console.log('✅ Service Worker registrado:', this.registration.scope);

            // Manejar actualizaciones
            this.registration.addEventListener('updatefound', () => {
                console.log('🔄 Nueva versión del Service Worker disponible');
                this.handleUpdate();
            });

            // Verificar si hay actualizaciones pendientes
            if (this.registration.waiting) {
                console.log('⏳ Service Worker esperando activación');
                this.handleUpdate();
            }
            
            // Escuchar mensajes del Service Worker
            navigator.serviceWorker.addEventListener('message', (event) => {
                if (event.data && event.data.action === 'SW_UPDATED') {
                    console.log('✅ Service Worker actualizado, recargando página...');
                    this.reloadPage();
                }
            });

            this.isRegistered = true;
            return true;

        } catch (error) {
            console.error('❌ Error registrando Service Worker:', error);
            return false;
        }
    }

    // Manejar actualizaciones del Service Worker
    handleUpdate() {
        const newWorker = this.registration.waiting;
        
        if (newWorker) {
            // Notificar al usuario sobre la actualización
            this.showUpdateNotification();
            
            // Escuchar mensajes del nuevo worker
            newWorker.addEventListener('statechange', () => {
                if (newWorker.state === 'activated') {
                    console.log('✅ Nueva versión del Service Worker activada');
                    this.reloadPage();
                }
            });
        }
    }

    // Mostrar notificación de actualización
    showUpdateNotification() {
        // Crear notificación personalizada
        const notification = document.createElement('div');
        notification.id = 'pwa-update-notification';
        notification.innerHTML = `
            <div style="
                position: fixed;
                top: 20px;
                right: 20px;
                background: #28a745;
                color: white;
                padding: 15px 20px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 10000;
                font-family: Arial, sans-serif;
                max-width: 300px;
            ">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 20px;">🔄</span>
                    <div>
                        <strong>Actualización disponible</strong>
                        <div style="font-size: 14px; margin-top: 5px;">
                            Hay una nueva versión de ARCA disponible
                        </div>
                    </div>
                </div>
                <div style="margin-top: 10px; display: flex; gap: 10px;">
                    <button onclick="window.pwaRegister.updateApp()" style="
                        background: white;
                        color: #28a745;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        cursor: pointer;
                        font-weight: bold;
                    ">Actualizar</button>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" style="
                        background: transparent;
                        color: white;
                        border: 1px solid white;
                        padding: 8px 16px;
                        border-radius: 4px;
                        cursor: pointer;
                    ">Después</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-ocultar después de 10 segundos
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 10000);
    }

    // Actualizar la aplicación
    async updateApp() {
        console.log('🔄 Iniciando actualización de la aplicación...');
        
        if (!this.registration) {
            console.error('❌ No hay registro de Service Worker');
            alert('Error: No se pudo actualizar. Por favor, recarga la página manualmente.');
            return;
        }

        // Si hay un service worker esperando
        if (this.registration.waiting) {
            console.log('📤 Enviando mensaje SKIP_WAITING al Service Worker...');
            
            // Enviar mensaje al Service Worker para activar la nueva versión
            this.registration.waiting.postMessage({ action: 'SKIP_WAITING' });
            
            // Escuchar cuando el nuevo worker se active
            this.registration.waiting.addEventListener('statechange', () => {
                if (this.registration.waiting.state === 'activated') {
                    console.log('✅ Nueva versión activada, recargando página...');
                    this.reloadPage();
                }
            });
            
            // También verificar periódicamente si el worker se activó
            const checkInterval = setInterval(() => {
                if (this.registration.waiting && this.registration.waiting.state === 'activated') {
                    clearInterval(checkInterval);
                    console.log('✅ Service Worker activado, recargando...');
                    this.reloadPage();
                } else if (!this.registration.waiting) {
                    // El worker ya se activó y ya no está en waiting
                    clearInterval(checkInterval);
                    console.log('✅ Service Worker actualizado, recargando...');
                    this.reloadPage();
                }
            }, 100);
            
            // Timeout de seguridad: recargar después de 2 segundos si no se activó
            setTimeout(() => {
                clearInterval(checkInterval);
                console.log('⏰ Timeout: Recargando página de todas formas...');
                this.reloadPage();
            }, 2000);
            
        } else {
            // No hay worker esperando, intentar actualizar manualmente
            console.log('🔄 No hay worker esperando, intentando actualizar manualmente...');
            try {
                await this.registration.update();
                
                // Esperar un momento y recargar
                setTimeout(() => {
                    console.log('🔄 Recargando página después de actualización...');
                    this.reloadPage();
                }, 1000);
            } catch (error) {
                console.error('❌ Error actualizando:', error);
                // Recargar de todas formas
                this.reloadPage();
            }
        }
        
        // Ocultar el modal de actualización
        const notification = document.getElementById('pwa-update-notification');
        if (notification) {
            notification.remove();
        }
    }

    // Recargar la página
    reloadPage() {
        window.location.reload();
    }

    // Verificar si la PWA está instalada
    isPWAInstalled() {
        return window.matchMedia('(display-mode: standalone)').matches ||
               window.navigator.standalone === true;
    }

    // Mostrar prompt de instalación
    async showInstallPrompt() {
        // Verificar si ya está instalada
        if (this.isPWAInstalled()) {
            console.log('✅ PWA ya está instalada');
            return;
        }

        // Verificar si el navegador soporta la instalación
        if (!('BeforeInstallPromptEvent' in window)) {
            console.log('⚠️ Instalación de PWA no soportada');
            return;
        }

        // Escuchar el evento de instalación
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            
            // Mostrar botón de instalación personalizado
            this.showInstallButton(e);
        });
    }

    // Mostrar botón de instalación personalizado
    showInstallButton(installEvent) {
        // Crear botón de instalación
        const installButton = document.createElement('button');
        installButton.id = 'pwa-install-button';
        installButton.innerHTML = '📱 Instalar ARCA';
        installButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,123,255,0.3);
            z-index: 1000;
            transition: all 0.3s ease;
        `;

        // Efecto hover
        installButton.addEventListener('mouseenter', () => {
            installButton.style.transform = 'translateY(-2px)';
            installButton.style.boxShadow = '0 6px 16px rgba(0,123,255,0.4)';
        });

        installButton.addEventListener('mouseleave', () => {
            installButton.style.transform = 'translateY(0)';
            installButton.style.boxShadow = '0 4px 12px rgba(0,123,255,0.3)';
        });

        // Manejar clic
        installButton.addEventListener('click', async () => {
            try {
                await installEvent.prompt();
                const choiceResult = await installEvent.userChoice;
                
                if (choiceResult.outcome === 'accepted') {
                    console.log('✅ PWA instalada por el usuario');
                    installButton.remove();
                } else {
                    console.log('❌ Usuario canceló la instalación');
                }
            } catch (error) {
                console.error('❌ Error durante la instalación:', error);
            }
        });

        document.body.appendChild(installButton);

        // Auto-ocultar después de 30 segundos
        setTimeout(() => {
            if (installButton.parentElement) {
                installButton.remove();
            }
        }, 30000);
    }

    // Limpiar cache
    async clearCache() {
        try {
            if (this.registration) {
                const cacheNames = await caches.keys();
                await Promise.all(
                    cacheNames.map(cacheName => caches.delete(cacheName))
                );
                console.log('✅ Cache limpiado');
                return true;
            }
        } catch (error) {
            console.error('❌ Error limpiando cache:', error);
        }
        return false;
    }

    // Obtener información del cache
    async getCacheInfo() {
        try {
            const cacheNames = await caches.keys();
            let totalSize = 0;
            let totalFiles = 0;

            for (const cacheName of cacheNames) {
                const cache = await caches.open(cacheName);
                const keys = await cache.keys();
                totalFiles += keys.length;
            }

            return {
                cacheNames,
                totalFiles,
                totalSize: `${totalFiles} archivos`
            };
        } catch (error) {
            console.error('❌ Error obteniendo info del cache:', error);
            return null;
        }
    }

    // Inicializar PWA
    async init() {
        console.log('🚀 Inicializando PWA...');
        
        // Registrar Service Worker
        const swRegistered = await this.registerServiceWorker();
        
        if (swRegistered) {
            // Mostrar prompt de instalación
            await this.showInstallPrompt();
            
            console.log('✅ PWA inicializada correctamente');
        } else {
            console.error('❌ Error inicializando PWA');
        }
    }
}

// Crear instancia global
window.pwaRegister = new PWARegister();

// Inicializar cuando se cargue la página
document.addEventListener('DOMContentLoaded', () => {
    window.pwaRegister.init();
});

// Funciones globales para debugging
window.clearPWACache = () => window.pwaRegister.clearCache();
window.getPWACacheInfo = () => window.pwaRegister.getCacheInfo();
window.updatePWA = () => window.pwaRegister.updateApp();
