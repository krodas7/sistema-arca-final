from django.urls import path, include
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Clientes
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/crear/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:cliente_id>/editar/', views.cliente_edit, name='cliente_edit'),
    path('clientes/<int:cliente_id>/eliminar/', views.cliente_delete, name='cliente_delete'),
    
    # Proyectos
    path('proyectos/', views.proyectos_list, name='proyectos_list'),
    path('proyectos/crear/', views.proyecto_create, name='proyecto_create'),
    path('proyectos/<int:proyecto_id>/', views.proyecto_dashboard, name='proyecto_dashboard'),
    path('proyectos/<int:proyecto_id>/editar/', views.proyecto_edit, name='proyecto_edit'),
    path('proyectos/<int:proyecto_id>/eliminar/', views.proyecto_delete, name='proyecto_delete'),
    path('proyectos/<int:proyecto_id>/asignar-colaboradores/', views.asignar_colaboradores_proyecto, name='asignar_colaboradores_proyecto'),
    path('proyectos/<int:proyecto_id>/planilla/', views.planilla_proyecto, name='planilla_proyecto'),
    path('proyecto/<int:proyecto_id>/planilla/pdf/', views.planilla_proyecto_pdf, name='planilla_proyecto_pdf'),
    path('proyectos/<int:proyecto_id>/administrar-anticipos/', views.administrar_anticipos_proyecto, name='administrar_anticipos_proyecto'),
    path('anticipos/<int:anticipo_id>/editar/', views.editar_anticipo, name='editar_anticipo'),
    path('anticipos/<int:anticipo_id>/eliminar/', views.eliminar_anticipo, name='eliminar_anticipo'),
    path('anticipos/<int:anticipo_id>/cambiar-estado/', views.cambiar_estado_anticipo, name='cambiar_estado_anticipo'),
    path('proyectos/<int:proyecto_id>/anticipo-masivo/', views.crear_anticipo_masivo, name='crear_anticipo_masivo'),
    path('proyectos/<int:proyecto_id>/anticipo-individual/', views.crear_anticipo_individual, name='crear_anticipo_individual'),
    path('anticipos/<int:anticipo_id>/liquidar/', views.liquidar_anticipo, name='liquidar_anticipo'),
    path('proyectos/<int:proyecto_id>/calendario-pagos/', views.calendario_pagos_proyecto, name='calendario_pagos_proyecto'),
    
    # Colaboradores
    path('colaboradores/', views.colaboradores_list, name='colaboradores_list'),
    path('colaboradores/crear/', views.colaborador_create, name='colaborador_create'),
    path('colaboradores/<int:colaborador_id>/', views.colaborador_detail, name='colaborador_detail'),
    path('colaboradores/<int:colaborador_id>/editar/', views.colaborador_edit, name='colaborador_edit'),
    path('colaboradores/<int:colaborador_id>/eliminar/', views.colaborador_delete, name='colaborador_delete'),
    
    # Facturas
    path('facturas/', views.facturas_list, name='facturas_list'),
    path('facturas/crear/', views.factura_create, name='factura_create'),
    path('facturas/<int:factura_id>/', views.factura_detail, name='factura_detail'),
    path('facturas/<int:factura_id>/editar/', views.factura_edit, name='factura_edit'),
    path('facturas/<int:factura_id>/eliminar/', views.factura_delete, name='factura_delete'),
    path('facturas/<int:factura_id>/marcar-pagada/', views.factura_marcar_pagada, name='factura_marcar_pagada'),
    
    # Reportes de Facturas
    path('facturas/reportes/', views.facturas_reporte_lista, name='facturas_reporte_lista'),
    path('facturas/reportes/pdf/', views.facturas_reporte_pdf, name='facturas_reporte_pdf'),
    path('facturas/reportes/excel/', views.facturas_reporte_excel, name='facturas_reporte_excel'),
    path('facturas/reportes/detallado/', views.facturas_reporte_detallado, name='facturas_reporte_detallado'),
    
    # Gastos
    path('gastos/dashboard/', views.gastos_dashboard, name='gastos_dashboard'),
    path('gastos/', views.gastos_list, name='gastos_list'),
    path('gastos/crear/', views.gasto_create, name='gasto_create'),
    path('gastos/<int:gasto_id>/editar/', views.gasto_edit, name='gasto_edit'),
    path('gastos/<int:gasto_id>/eliminar/', views.gasto_delete, name='gasto_delete'),
    path('gastos/<int:gasto_id>/aprobar/', views.gasto_aprobar, name='gasto_aprobar'),
    
    # Pagos
    path('pagos/', views.pagos_list, name='pagos_list'),
    path('pagos/crear/', views.pago_create, name='pago_create'),
    path('pagos/<int:pago_id>/editar/', views.pago_edit, name='pago_edit'),
    path('pagos/<int:pago_id>/eliminar/', views.pago_delete, name='pago_delete'),
    
    # Categorías de Gasto
    path('categorias-gasto/', views.categorias_gasto_list, name='categorias_gasto_list'),
    path('categorias-gasto/crear/', views.categoria_gasto_create, name='categoria_gasto_create'),
    path('categorias-gasto/<int:categoria_id>/editar/', views.categoria_gasto_edit, name='categoria_gasto_edit'),
    path('categorias-gasto/<int:categoria_id>/eliminar/', views.categoria_gasto_delete, name='categoria_gasto_delete'),
    
    # Rentabilidad
    path('rentabilidad/', views.rentabilidad_view, name='rentabilidad'),
    path('rentabilidad/exportar/pdf/', views.rentabilidad_exportar_pdf, name='rentabilidad_exportar_pdf'),
    path('rentabilidad/exportar/excel/', views.rentabilidad_exportar_excel, name='rentabilidad_exportar_excel'),
    
    # Usuarios
    path('usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('usuarios/crear/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/<int:usuario_id>/editar/', views.usuario_editar, name='usuario_editar'),
    
    # Sistema
    path('sistema/', views.sistema_view, name='sistema'),
    path('sistema/configurar/', views.sistema_configurar, name='sistema_configurar'),
    path('sistema/logs/', views.sistema_logs, name='sistema_logs'),
    path('sistema/reset-app/', views.sistema_reset_app, name='sistema_reset_app'),
    path('sistema/crear-respaldo/', views.sistema_crear_respaldo, name='sistema_crear_respaldo'),
    path('sistema/ver-respaldos/', views.sistema_ver_respaldos, name='sistema_ver_respaldos'),
    path('sistema/limpiar-logs/', views.sistema_limpiar_logs, name='sistema_limpiar_logs'),
    path('sistema/exportar-config/', views.sistema_exportar_config, name='sistema_exportar_config'),
    
    # Offline
    path('offline/', views.offline_view, name='offline'),
    
    # Anticipos
    path('anticipos/', views.anticipos_list, name='anticipos_list'),
    path('anticipos/crear/', views.anticipo_create, name='anticipo_create'),
    path('anticipos/<int:anticipo_id>/', views.anticipo_detail, name='anticipo_detail'),
    path('anticipos/<int:anticipo_id>/editar/', views.anticipo_edit, name='anticipo_edit'),
    path('anticipos/<int:anticipo_id>/eliminar/', views.anticipo_delete, name='anticipo_delete'),
    path('anticipos/<int:anticipo_id>/aplicar/', views.aplicar_anticipo, name='aplicar_anticipo'),

    # URLs de Archivos de Proyectos
    path('archivos/', views.archivos_proyectos_list, name='archivos_proyectos_list'),
    path('archivos/proyecto/<int:proyecto_id>/', views.archivos_proyecto_list, name='archivos_proyecto_list'),
    path('archivos/proyecto/<int:proyecto_id>/subir/', views.archivo_upload, name='archivo_upload'),
    path('archivos/<int:archivo_id>/descargar/', views.archivo_download, name='archivo_download'),
    path('archivos/<int:archivo_id>/eliminar/', views.archivo_delete, name='archivo_delete'),
    path('archivos/<int:archivo_id>/preview/', views.archivo_preview, name='archivo_preview'),
    
    # URLs de Carpetas de Proyectos
    path('archivos/proyecto/<int:proyecto_id>/carpeta/crear/', views.carpeta_create, name='carpeta_create'),
    path('archivos/carpeta/<int:carpeta_id>/editar/', views.carpeta_edit, name='carpeta_edit'),
    path('archivos/carpeta/<int:carpeta_id>/eliminar/', views.carpeta_delete, name='carpeta_delete'),
    path('archivos/carpeta/<int:carpeta_id>/', views.carpeta_detail, name='carpeta_detail'),

    # Presupuestos
    path('presupuestos/', views.presupuestos_list, name='presupuestos_list'),
    path('presupuestos/crear/', views.presupuesto_create, name='presupuesto_create'),
    path('presupuestos/<int:presupuesto_id>/', views.presupuesto_detail, name='presupuesto_detail'),
    path('presupuestos/<int:presupuesto_id>/editar/', views.presupuesto_edit, name='presupuesto_edit'),
    path('presupuestos/<int:presupuesto_id>/partida/crear/', views.partida_create, name='partida_create'),
    path('presupuestos/<int:presupuesto_id>/aprobar/', views.presupuesto_aprobar, name='presupuesto_aprobar'),

    # ==================== URLs DE NOTIFICACIONES ====================
    path('notificaciones/', views.notificaciones_list, name='notificaciones_list'),
    path('notificaciones/configurar/', views.notificaciones_configurar, name='notificaciones_configurar'),
    path('notificaciones/historial/', views.notificaciones_historial, name='notificaciones_historial'),
    path('notificacion/<int:notificacion_id>/marcar-leida/', views.notificacion_marcar_leida, name='notificacion_marcar_leida'),
    
    # ==================== URLs DE NOTIFICACIONES ====================
    path('notificaciones/marcar-todas-leidas/', views.notificacion_marcar_todas_leidas, name='notificacion_marcar_todas_leidas'),
    
    # API para notificaciones en tiempo real
    path('api/notificaciones/no-leidas/', views.api_notificaciones_no_leidas, name='api_notificaciones_no_leidas'),
    path('api/notificacion/<int:notificacion_id>/marcar-leida/', views.api_marcar_leida, name='api_marcar_leida'),
    
    # Administración de notificaciones (solo superusuarios)
    path('admin/notificaciones/sistema/', views.admin_notificaciones_sistema, name='admin_notificaciones_sistema'),
    path('admin/notificaciones/ejecutar-verificaciones/', views.admin_ejecutar_verificaciones, name='admin_ejecutar_verificaciones'),

    # Vista de prueba para notificaciones
    path('test-notification-email/', views.test_notification_email, name='test_notification_email'),
    
    # Notificaciones Push
    path('push-notifications/', views.push_notifications_setup, name='push_notifications_setup'),
    path('api/push-subscription/', views.api_push_subscription, name='api_push_subscription'),

    # ===== URLs DEL MÓDULO DE INVENTARIO =====
    path('inventario/', views.inventario_dashboard, name='inventario_dashboard'),
    
    # URLs para Categorías
    path('inventario/categorias/', views.categoria_list, name='categoria_list'),
    path('inventario/categorias/crear/', views.categoria_create, name='categoria_create'),
    path('inventario/categorias/<int:pk>/', views.categoria_detail, name='categoria_detail'),
    path('inventario/categorias/<int:pk>/editar/', views.categoria_edit, name='categoria_edit'),
    path('inventario/categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
    
    # URLs para Items
    path('inventario/items/', views.item_list, name='item_list'),
    path('inventario/items/crear/', views.item_create, name='item_create'),
    path('inventario/items/<int:pk>/', views.item_detail, name='item_detail'),
    path('inventario/items/<int:pk>/editar/', views.item_edit, name='item_edit'),
    path('inventario/items/<int:pk>/eliminar/', views.item_delete, name='item_delete'),
    
    # URLs para Asignaciones
    path('inventario/asignaciones/', views.asignacion_list, name='asignacion_list'),
    path('inventario/asignaciones/crear/', views.asignacion_create, name='asignacion_create'),
    path('inventario/asignaciones/<int:pk>/', views.asignacion_detail, name='asignacion_detail'),
    path('inventario/asignaciones/<int:pk>/editar/', views.asignacion_edit, name='asignacion_edit'),
    path('inventario/asignaciones/<int:pk>/eliminar/', views.asignacion_delete, name='asignacion_delete'),
    path('inventario/asignaciones/<int:pk>/devolver/', views.asignacion_devolver, name='asignacion_devolver'),
    
    # URLs para Gestión de Usuarios y Roles
    path('roles/', views.roles_lista, name='roles_lista'),
    path('roles/crear/', views.rol_crear, name='rol_crear'),
    path('roles/<int:rol_id>/editar/', views.rol_editar, name='rol_editar'),
    path('roles/<int:rol_id>/eliminar/', views.rol_eliminar, name='rol_eliminar'),
    path('roles/resumen/', views.roles_resumen, name='roles_resumen'),
    path('roles/<int:rol_id>/permisos/', views.rol_permisos, name='rol_permisos'),
    
    # PWA Test
    path('pwa-test/', views.pwa_test, name='pwa_test'),
    
    # ==================== DASHBOARD INTELIGENTE ====================
    path('api/dashboard-intelligent-data/', views.dashboard_intelligent_data, name='dashboard_intelligent_data'),
    path('dashboard-intelligent-analytics/', views.dashboard_intelligent_analytics, name='dashboard_intelligent_analytics'),
    
    # ==================== PWA Y OFFLINE ====================
    path('offline/', views.offline_page, name='offline_page'),
    
    # ==================== URL DE PRUEBA ====================
    path('test/', views.test_view, name='test'),
]
