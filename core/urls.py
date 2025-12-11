from django.urls import path, include
from . import views
from . import views_usuarios_mejoradas

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
    path('clientes/<int:cliente_id>/', views.cliente_detail, name='cliente_detail'),
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
    path('proyecto/<int:proyecto_id>/planilla/liquidar/', views.liquidar_y_generar_planilla, name='liquidar_y_generar_planilla'),
    path('proyecto/<int:proyecto_id>/planilla/pdf/', views.planilla_proyecto_pdf, name='planilla_proyecto_pdf'),
    path('proyecto/<int:proyecto_id>/historico-nomina/reset/', views.resetear_historico_nomina, name='resetear_historico_nomina'),
    path('proyectos/<int:proyecto_id>/administrar-anticipos/', views.administrar_anticipos_proyecto, name='administrar_anticipos_proyecto'),
    path('proyectos/<int:proyecto_id>/anticipos/<int:anticipo_id>/editar/', views.editar_anticipo, name='editar_anticipo'),
    path('proyectos/<int:proyecto_id>/anticipos/<int:anticipo_id>/eliminar/', views.eliminar_anticipo, name='eliminar_anticipo'),
    path('proyectos/<int:proyecto_id>/anticipos/<int:anticipo_id>/cambiar-estado/', views.cambiar_estado_anticipo, name='cambiar_estado_anticipo'),
    path('proyectos/<int:proyecto_id>/anticipo-masivo/', views.crear_anticipo_masivo, name='crear_anticipo_masivo'),
    path('proyectos/<int:proyecto_id>/anticipo-individual/', views.crear_anticipo_individual, name='crear_anticipo_individual'),
    path('anticipos/<int:anticipo_id>/liquidar/', views.liquidar_anticipo, name='liquidar_anticipo'),
    path('proyectos/<int:proyecto_id>/calendario-pagos/', views.calendario_pagos_proyecto, name='calendario_pagos_proyecto'),
    
    # Trabajadores Diarios - Módulo Principal
    path('trabajadores-diarios/', views.trabajadores_diarios_dashboard, name='trabajadores_diarios_dashboard'),
    path('trabajadores-diarios/gestor-planillas/', views.planillas_trabajadores_diarios_gestor, name='planillas_trabajadores_diarios_gestor'),
    path('trabajadores-diarios/crear-planilla/', views.planilla_trabajadores_diarios_create_global, name='planilla_trabajadores_diarios_create_global'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/', views.trabajadores_diarios_list, name='trabajadores_diarios_list'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/crear/', views.trabajador_diario_create, name='trabajador_diario_create'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/finalizar/', views.finalizar_planilla_trabajadores, name='finalizar_planilla_trabajadores'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/generar-pdf/', views.generar_pdf_planilla_trabajadores, name='generar_pdf_planilla_trabajadores'),
    path(
        'proyectos/<int:proyecto_id>/trabajadores-diarios/planilla/<int:planilla_id>/reabrir/',
        views.reabrir_planilla_trabajadores,
        name='reabrir_planilla_trabajadores'
    ),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/reactivar-todos/', views.reactivar_todos_trabajadores_diarios, name='reactivar_todos_trabajadores_diarios'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/<int:trabajador_id>/', views.trabajador_diario_detail, name='trabajador_diario_detail'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/<int:trabajador_id>/editar/', views.trabajador_diario_edit, name='trabajador_diario_edit'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/<int:trabajador_id>/eliminar/', views.trabajador_diario_delete, name='trabajador_diario_delete'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/<int:trabajador_id>/reactivar/', views.reactivar_trabajador_diario, name='reactivar_trabajador_diario'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/<int:trabajador_id>/registro/crear/', views.registro_trabajo_create, name='registro_trabajo_create'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/<int:trabajador_id>/registro/<int:registro_id>/editar/', views.registro_trabajo_edit, name='registro_trabajo_edit'),
    
    # ==================== PLANILLAS DE TRABAJADORES DIARIOS ====================
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/', views.planillas_trabajadores_diarios_list, name='planillas_trabajadores_diarios_list'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/crear/', views.planilla_trabajadores_diarios_create, name='planilla_trabajadores_diarios_create'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/', views.planilla_trabajadores_diarios_detail, name='planilla_trabajadores_diarios_detail'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/editar/', views.planilla_trabajadores_diarios_edit, name='planilla_trabajadores_diarios_edit'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/eliminar/', views.planilla_trabajadores_diarios_delete, name='planilla_trabajadores_diarios_delete'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/finalizar/', views.planilla_trabajadores_diarios_finalizar, name='planilla_trabajadores_diarios_finalizar'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/agregar-trabajador/', views.trabajador_diario_add_to_planilla, name='trabajador_diario_add_to_planilla'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/remover-trabajador/<int:trabajador_id>/', views.trabajador_diario_remove_from_planilla, name='trabajador_diario_remove_from_planilla'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/<int:trabajador_id>/registro/<int:registro_id>/eliminar/', views.registro_trabajo_delete, name='registro_trabajo_delete'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/<int:trabajador_id>/actualizar-dias/', views.actualizar_dias_trabajados, name='actualizar_dias_trabajados'),
    path('proyectos/<int:proyecto_id>/trabajadores-diarios/pdf/', views.trabajadores_diarios_pdf, name='trabajadores_diarios_pdf'),
    
    # Anticipos de Trabajadores Diarios
    path('proyectos/<int:proyecto_id>/anticipos-trabajadores-diarios/', views.anticipo_trabajador_diario_list, name='anticipo_trabajador_diario_list'),
    path('proyectos/<int:proyecto_id>/anticipos-trabajadores-diarios/crear/', views.anticipo_trabajador_diario_create, name='anticipo_trabajador_diario_create'),
    path('proyectos/<int:proyecto_id>/anticipos-trabajadores-diarios/<int:anticipo_id>/', views.anticipo_trabajador_diario_detail, name='anticipo_trabajador_diario_detail'),
    path('proyectos/<int:proyecto_id>/anticipos-trabajadores-diarios/<int:anticipo_id>/editar/', views.anticipo_trabajador_diario_edit, name='anticipo_trabajador_diario_edit'),
    path('proyectos/<int:proyecto_id>/anticipos-trabajadores-diarios/<int:anticipo_id>/aplicar/', views.anticipo_trabajador_diario_aplicar, name='anticipo_trabajador_diario_aplicar'),
    path('proyectos/<int:proyecto_id>/anticipos-trabajadores-diarios/<int:anticipo_id>/eliminar/', views.anticipo_trabajador_diario_delete, name='anticipo_trabajador_diario_delete'),
    
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
    path('gastos/<int:gasto_id>/', views.gasto_detail, name='gasto_detail'),
    path('gastos/<int:gasto_id>/editar/', views.gasto_edit, name='gasto_edit'),
    path('gastos/<int:gasto_id>/eliminar/', views.gasto_delete, name='gasto_delete'),
    path('gastos/<int:gasto_id>/aprobar/', views.gasto_aprobar, name='gasto_aprobar'),
    path('gastos/<int:gasto_id>/desaprobar/', views.gasto_desaprobar, name='gasto_desaprobar'),
    
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
    
    # Usuarios Mejorados - URLs principales
    path('usuarios/dashboard/', views_usuarios_mejoradas.usuarios_dashboard, name='usuarios_dashboard'),
    path('usuarios/lista-mejorada/', views_usuarios_mejoradas.usuarios_lista_mejorada, name='usuarios_lista_mejorada'),
    path('usuarios/crear-mejorado/', views_usuarios_mejoradas.usuario_crear_mejorado, name='usuario_crear_mejorado'),
    path('usuarios/<int:usuario_id>/editar-mejorado/', views_usuarios_mejoradas.usuario_editar_mejorado, name='usuario_editar_mejorado'),
    path('usuarios/gestor-permisos/', views_usuarios_mejoradas.usuarios_gestor_permisos, name='usuarios_gestor_permisos'),
    path('usuarios/gestor-permisos-intuitivo/', views_usuarios_mejoradas.usuarios_gestor_permisos_intuitivo, name='usuarios_gestor_permisos_intuitivo'),
    
    # Sistema
    path('sistema/', views.sistema_view, name='sistema'),
    path('sistema/configurar/', views.sistema_configurar, name='sistema_configurar'),
    path('sistema/logs/', views.sistema_logs, name='sistema_logs'),
    path('sistema/reset-app/', views.sistema_reset_app, name='sistema_reset_app'),
    path('sistema/crear-respaldo/', views.sistema_crear_respaldo, name='sistema_crear_respaldo'),
    path('sistema/ver-respaldos/', views.sistema_ver_respaldos, name='sistema_ver_respaldos'),
    path('sistema/restaurar-respaldo/<str:filename>/', views.sistema_restaurar_respaldo, name='sistema_restaurar_respaldo'),
    path('sistema/limpiar-logs/', views.sistema_limpiar_logs, name='sistema_limpiar_logs'),
    path('sistema/exportar-config/', views.sistema_exportar_config, name='sistema_exportar_config'),
    
    # Offline
    path('offline/', views.offline_view, name='offline'),
    path('service-worker.js', views.service_worker, name='service_worker'),
    
    # Anticipos
    path('anticipos/', views.anticipos_list, name='anticipos_list'),
    path('anticipos/crear/', views.anticipo_create, name='anticipo_create'),
    path('anticipos/<int:anticipo_id>/', views.anticipo_detail, name='anticipo_detail'),
    path('anticipos/<int:anticipo_id>/editar/', views.anticipo_edit, name='anticipo_edit'),
    path('anticipos/<int:anticipo_id>/eliminar/', views.anticipo_delete, name='anticipo_delete'),
    path('anticipos/<int:anticipo_id>/aplicar/', views.aplicar_anticipo, name='aplicar_anticipo'),
    
    # Eventos del Calendario
    path('eventos/', views.eventos_calendario_list, name='eventos_calendario_list'),
    path('eventos/crear/', views.evento_calendario_create, name='evento_calendario_create'),
    path('eventos/<int:evento_id>/editar/', views.evento_calendario_edit, name='evento_calendario_edit'),
    path('eventos/<int:evento_id>/eliminar/', views.evento_calendario_delete, name='evento_calendario_delete'),
    path('api/eventos/', views.eventos_calendario_json, name='eventos_calendario_json'),
    path('api/eventos/crear/', views.evento_calendario_create_ajax, name='evento_calendario_create_ajax'),
    path('api/eventos/<int:evento_id>/actualizar/', views.evento_calendario_update_ajax, name='evento_calendario_update_ajax'),
    path('api/eventos/<int:evento_id>/eliminar/', views.evento_calendario_delete_ajax, name='evento_calendario_delete_ajax'),

    # URLs de Archivos de Proyectos
    path('archivos/', views.archivos_proyectos_list, name='archivos_proyectos_list'),
    path('archivos/proyecto/<int:proyecto_id>/', views.archivos_proyecto_list, name='archivos_proyecto_list'),
    path('archivos/proyecto/<int:proyecto_id>/subir/', views.archivo_upload, name='archivo_upload'),
    path('archivos/carpeta/<int:carpeta_id>/subir/', views.archivo_upload_carpeta, name='archivo_upload_carpeta'),
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
    
    # URLs Mejoradas para Gestión de Usuarios y Roles (duplicadas - eliminadas)
    
    path('roles-mejorados/', views_usuarios_mejoradas.roles_lista_mejorada, name='roles_lista_mejorada'),
    path('roles-mejorados/crear/', views_usuarios_mejoradas.rol_crear_mejorado, name='rol_crear_mejorado'),
    path('roles-mejorados/<int:rol_id>/editar/', views_usuarios_mejoradas.rol_editar_mejorado, name='rol_editar_mejorado'),
    path('roles-mejorados/<int:rol_id>/eliminar/', views_usuarios_mejoradas.rol_eliminar_mejorado, name='rol_eliminar_mejorado'),
    
    path('permisos-gestor/', views_usuarios_mejoradas.permisos_gestor, name='permisos_gestor'),
    path('api/permisos/actualizar-masivo/', views_usuarios_mejoradas.permisos_actualizar_masivo, name='permisos_actualizar_masivo'),
    path('api/permisos/rol/<int:rol_id>/modulos/', views_usuarios_mejoradas.permisos_rol_modulos, name='permisos_rol_modulos'),
    path('api/permisos/actualizar-modulos/', views_usuarios_mejoradas.permisos_actualizar_modulos, name='permisos_actualizar_modulos'),
    
    # PWA Test
    path('pwa-test/', views.pwa_test, name='pwa_test'),
    
    # ==================== DASHBOARD INTELIGENTE ====================
    path('api/dashboard-intelligent-data/', views.dashboard_intelligent_data, name='dashboard_intelligent_data'),
    path('dashboard-intelligent-analytics/', views.dashboard_intelligent_analytics, name='dashboard_intelligent_analytics'),
    
    # ==================== PWA Y OFFLINE ====================
    path('offline/', views.offline_page, name='offline_page'),
    
    # ==================== URL DE PRUEBA ====================
    path('test/', views.test_view, name='test'),
    
    # ==================== NUEVAS RUTAS OPTIMIZADAS ====================
    # APIs mejoradas
    path('api/dashboard-data/', views.dashboard_data_api, name='dashboard_data_api'),
    path('api/dashboard-intelligent-data/', views.dashboard_intelligent_data, name='dashboard_intelligent_data'),
    path('api/login/', views.api_login, name='api_login'),
    
    # Vistas mejoradas
    path('dashboard-intelligent-analytics/', views.dashboard_intelligent_analytics, name='dashboard_intelligent_analytics'),
    path('clientes/<int:cliente_id>/toggle-estado/', views.cliente_toggle_estado, name='cliente_toggle_estado'),
    path('clientes/<int:cliente_id>/estadisticas/', views.cliente_estadisticas, name='cliente_estadisticas'),
    
    # PWA
    path('offline/', views.offline_page, name='offline_page'),
    
    # ==================== PLANILLAS DE TRABAJADORES DIARIOS ====================
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/', views.planillas_trabajadores_diarios_list, name='planillas_trabajadores_diarios_list'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/crear/', views.planilla_trabajadores_diarios_create, name='planilla_trabajadores_diarios_create'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/', views.planilla_trabajadores_diarios_detail, name='planilla_trabajadores_diarios_detail'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/editar/', views.planilla_trabajadores_diarios_edit, name='planilla_trabajadores_diarios_edit'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/eliminar/', views.planilla_trabajadores_diarios_delete, name='planilla_trabajadores_diarios_delete'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/finalizar/', views.planilla_trabajadores_diarios_finalizar, name='planilla_trabajadores_diarios_finalizar'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/agregar-trabajador/', views.trabajador_diario_add_to_planilla, name='trabajador_diario_add_to_planilla'),
    path('proyectos/<int:proyecto_id>/planillas-trabajadores-diarios/<int:planilla_id>/remover-trabajador/<int:trabajador_id>/', views.trabajador_diario_remove_from_planilla, name='trabajador_diario_remove_from_planilla'),
]
