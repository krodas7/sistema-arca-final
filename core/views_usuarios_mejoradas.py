from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)
from .models import (
    Rol, PerfilUsuario, Modulo, Permiso, RolPermiso, LogActividad
)
import json

# ==================== GESTIÓN DE ROLES MEJORADA ====================

@login_required
def roles_lista_mejorada(request):
    """Lista mejorada de roles con funcionalidades avanzadas"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    # Búsqueda y filtros
    search = request.GET.get('search', '')
    roles = Rol.objects.all().order_by('nombre')
    
    if search:
        roles = roles.filter(nombre__icontains=search)
    
    # Obtener estadísticas por rol
    roles_con_estadisticas = []
    for rol in roles:
        permisos_count = RolPermiso.objects.filter(rol=rol, activo=True).count()
        usuarios_count = PerfilUsuario.objects.filter(rol=rol).count()
        modulos_count = RolPermiso.objects.filter(
            rol=rol, activo=True
        ).values('permiso__modulo').distinct().count()
        
        roles_con_estadisticas.append({
            'rol': rol,
            'permisos_count': permisos_count,
            'usuarios_count': usuarios_count,
            'modulos_count': modulos_count
        })
    
    # Paginación
    paginator = Paginator(roles_con_estadisticas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'total_roles': roles.count(),
    }
    
    return render(request, 'core/roles/lista_mejorada.html', context)


@login_required
def rol_crear_mejorado(request):
    """Crear nuevo rol con interfaz mejorada"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Crear rol
                rol = Rol.objects.create(
                    nombre=request.POST.get('nombre'),
                    descripcion=request.POST.get('descripcion', '')
                )
                
                # Asignar permisos si se proporcionan
                permisos_ids = request.POST.getlist('permisos')
                for permiso_id in permisos_ids:
                    permiso = get_object_or_404(Permiso, id=permiso_id)
                    RolPermiso.objects.create(rol=rol, permiso=permiso)
                
                # Log de actividad
                LogActividad.objects.create(
                    usuario=request.user,
                    accion='Crear Rol',
                    modulo='Usuarios',
                    descripcion=f'Rol creado: {rol.nombre}',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                messages.success(request, f'Rol "{rol.nombre}" creado exitosamente')
                return redirect('roles_lista_mejorada')
                
        except Exception as e:
            logger.error(f"Error creando rol: {e}")
            messages.error(request, f'Error al crear el rol: {str(e)}')
    
    # Obtener módulos y permisos para el formulario
    modulos = Modulo.objects.filter(activo=True).order_by('nombre')
    permisos_por_modulo = {}
    
    for modulo in modulos:
        permisos_por_modulo[modulo] = Permiso.objects.filter(modulo=modulo).order_by('tipo', 'nombre')
    
    context = {
        'modulos': modulos,
        'permisos_por_modulo': permisos_por_modulo,
    }
    
    return render(request, 'core/roles/crear_mejorado.html', context)


@login_required
def rol_editar_mejorado(request, rol_id):
    """Editar rol con interfaz mejorada"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    rol = get_object_or_404(Rol, id=rol_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Actualizar datos del rol
                rol.nombre = request.POST.get('nombre')
                rol.descripcion = request.POST.get('descripcion', '')
                rol.save()
                
                # Actualizar permisos
                permisos_ids = request.POST.getlist('permisos')
                
                # Desactivar todos los permisos actuales
                RolPermiso.objects.filter(rol=rol).update(activo=False)
                
                # Activar los permisos seleccionados
                for permiso_id in permisos_ids:
                    permiso = get_object_or_404(Permiso, id=permiso_id)
                    rol_permiso, created = RolPermiso.objects.get_or_create(
                        rol=rol, 
                        permiso=permiso,
                        defaults={'activo': True}
                    )
                    if not created:
                        rol_permiso.activo = True
                        rol_permiso.save()
                
                # Log de actividad
                LogActividad.objects.create(
                    usuario=request.user,
                    accion='Editar Rol',
                    modulo='Usuarios',
                    descripcion=f'Rol editado: {rol.nombre}',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                messages.success(request, f'Rol "{rol.nombre}" actualizado exitosamente')
                return redirect('roles_lista_mejorada')
                
        except Exception as e:
            logger.error(f"Error editando rol: {e}")
            messages.error(request, f'Error al actualizar el rol: {str(e)}')
    
    # Obtener permisos actuales del rol
    permisos_actuales = RolPermiso.objects.filter(rol=rol, activo=True).values_list('permiso_id', flat=True)
    
    # Obtener módulos y permisos para el formulario
    modulos = Modulo.objects.filter(activo=True).order_by('nombre')
    permisos_por_modulo = {}
    
    for modulo in modulos:
        permisos_por_modulo[modulo] = Permiso.objects.filter(modulo=modulo).order_by('tipo', 'nombre')
    
    context = {
        'rol': rol,
        'modulos': modulos,
        'permisos_por_modulo': permisos_por_modulo,
        'permisos_actuales': list(permisos_actuales),
    }
    
    return render(request, 'core/roles/editar_mejorado.html', context)


@login_required
def rol_eliminar_mejorado(request, rol_id):
    """Eliminar rol con confirmación mejorada"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    rol = get_object_or_404(Rol, id=rol_id)
    
    # Verificar si hay usuarios con este rol
    usuarios_con_rol = PerfilUsuario.objects.filter(rol=rol).count()
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Desasignar rol de todos los usuarios
                PerfilUsuario.objects.filter(rol=rol).update(rol=None)
                
                # Eliminar permisos del rol
                RolPermiso.objects.filter(rol=rol).delete()
                
                # Eliminar el rol
                rol_nombre = rol.nombre
                rol.delete()
                
                # Log de actividad
                LogActividad.objects.create(
                    usuario=request.user,
                    accion='Eliminar Rol',
                    modulo='Usuarios',
                    descripcion=f'Rol eliminado: {rol_nombre}',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                messages.success(request, f'Rol "{rol_nombre}" eliminado exitosamente')
                return redirect('roles_lista_mejorada')
                
        except Exception as e:
            logger.error(f"Error eliminando rol: {e}")
            messages.error(request, f'Error al eliminar el rol: {str(e)}')
    
    context = {
        'rol': rol,
        'usuarios_con_rol': usuarios_con_rol,
    }
    
    return render(request, 'core/roles/eliminar_mejorado.html', context)


# ==================== GESTIÓN DE USUARIOS MEJORADA ====================

@login_required
def usuarios_lista_mejorada(request):
    """Lista mejorada de usuarios con funcionalidades avanzadas"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    # Búsqueda y filtros
    search = request.GET.get('search', '')
    rol_filter = request.GET.get('rol', '')
    estado_filter = request.GET.get('estado', '')
    
    usuarios = User.objects.all().order_by('-date_joined')
    
    if search:
        usuarios = usuarios.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    if rol_filter:
        usuarios = usuarios.filter(perfilusuario__rol_id=rol_filter)
    
    if estado_filter == 'activo':
        usuarios = usuarios.filter(is_active=True)
    elif estado_filter == 'inactivo':
        usuarios = usuarios.filter(is_active=False)
    
    # Obtener estadísticas
    total_usuarios = usuarios.count()
    usuarios_activos = usuarios.filter(is_active=True).count()
    superusuarios = usuarios.filter(is_superuser=True).count()
    
    # Paginación
    paginator = Paginator(usuarios, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener roles para el filtro
    roles = Rol.objects.all().order_by('nombre')
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'rol_filter': rol_filter,
        'estado_filter': estado_filter,
        'roles': roles,
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'superusuarios': superusuarios,
    }
    
    return render(request, 'core/usuarios/lista_mejorada.html', context)


@login_required
def usuario_crear_mejorado(request):
    """Crear usuario con interfaz mejorada"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Datos básicos del usuario
                username = request.POST.get('username')
                email = request.POST.get('email')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                password = request.POST.get('password')
                rol_id = request.POST.get('rol')
                is_superuser = request.POST.get('is_superuser') == 'on'
                is_staff = request.POST.get('is_staff') == 'on'
                
                # Validaciones
                if not username or not password:
                    messages.error(request, 'Usuario y contraseña son obligatorios')
                    return redirect('usuario_crear_mejorado')
                
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Ya existe un usuario con ese nombre')
                    return redirect('usuario_crear_mejorado')
                
                # Crear usuario
                usuario = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    is_superuser=is_superuser,
                    is_staff=is_staff
                )
                
                # Crear perfil y asignar rol
                perfil, created = PerfilUsuario.objects.get_or_create(usuario=usuario)
                if rol_id:
                    perfil.rol = Rol.objects.get(id=rol_id)
                    perfil.telefono = request.POST.get('telefono', '')
                    perfil.direccion = request.POST.get('direccion', '')
                    perfil.save()
                
                # Log de actividad
                LogActividad.objects.create(
                    usuario=request.user,
                    accion='Crear Usuario',
                    modulo='Usuarios',
                    descripcion=f'Usuario creado: {usuario.username}',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                messages.success(request, f'Usuario "{usuario.username}" creado exitosamente')
                return redirect('usuarios_lista_mejorada')
                
        except Exception as e:
            logger.error(f"Error creando usuario: {e}")
            messages.error(request, f'Error al crear el usuario: {str(e)}')
    
    # Obtener roles para el formulario
    roles = Rol.objects.all().order_by('nombre')
    
    context = {
        'roles': roles,
    }
    
    return render(request, 'core/usuarios/crear_mejorado.html', context)


@login_required
def usuario_editar_mejorado(request, usuario_id):
    """Editar usuario con interfaz mejorada"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    usuario = get_object_or_404(User, id=usuario_id)
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=usuario)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Actualizar datos básicos
                usuario.first_name = request.POST.get('first_name', '')
                usuario.last_name = request.POST.get('last_name', '')
                usuario.email = request.POST.get('email', '')
                usuario.is_active = request.POST.get('is_active') == 'on'
                usuario.is_superuser = request.POST.get('is_superuser') == 'on'
                usuario.is_staff = request.POST.get('is_staff') == 'on'
                usuario.save()
                
                # Actualizar perfil
                rol_id = request.POST.get('rol')
                if rol_id:
                    perfil.rol = Rol.objects.get(id=rol_id)
                else:
                    perfil.rol = None
                
                perfil.telefono = request.POST.get('telefono', '')
                perfil.direccion = request.POST.get('direccion', '')
                perfil.activo = request.POST.get('activo') == 'on'
                perfil.save()
                
                # Cambiar contraseña si se proporciona
                nueva_password = request.POST.get('password')
                if nueva_password:
                    usuario.set_password(nueva_password)
                    usuario.save()
                
                # Log de actividad
                LogActividad.objects.create(
                    usuario=request.user,
                    accion='Editar Usuario',
                    modulo='Usuarios',
                    descripcion=f'Usuario editado: {usuario.username}',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                messages.success(request, f'Usuario "{usuario.username}" actualizado exitosamente')
                return redirect('usuarios_lista_mejorada')
                
        except Exception as e:
            logger.error(f"Error editando usuario: {e}")
            messages.error(request, f'Error al actualizar el usuario: {str(e)}')
    
    # Obtener roles para el formulario
    roles = Rol.objects.all().order_by('nombre')
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
        'roles': roles,
    }
    
    return render(request, 'core/usuarios/editar_mejorado.html', context)


# ==================== GESTIÓN DE PERMISOS ====================

@login_required
def permisos_gestor(request):
    """Gestor visual de permisos por módulos completos - Vista independiente"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    # Obtener módulos activos
    modulos = Modulo.objects.filter(activo=True).order_by('nombre')
    
    # Obtener roles
    roles = Rol.objects.all().order_by('nombre')
    
    # Obtener matriz de módulos (rol x módulo)
    matriz_modulos = {}
    for rol in roles:
        modulos_rol = rol.modulos_activos.values_list('id', flat=True)
        matriz_modulos[rol.id] = list(modulos_rol)
    
    context = {
        'modulos': modulos,
        'roles': roles,
        'matriz_modulos': matriz_modulos,
    }
    
    return render(request, 'core/permisos/gestor_simplificado.html', context)


def usuarios_gestor_permisos(request):
    """Gestor de permisos integrado en el módulo de usuarios"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    # Obtener módulos activos
    modulos = Modulo.objects.filter(activo=True).order_by('nombre')
    
    # Obtener roles
    roles = Rol.objects.all().order_by('nombre')
    
    # Obtener matriz de módulos (rol x módulo)
    matriz_modulos = {}
    for rol in roles:
        modulos_rol = rol.modulos_activos.values_list('id', flat=True)
        matriz_modulos[rol.id] = list(modulos_rol)
    
    context = {
        'modulos': modulos,
        'roles': roles,
        'matriz_modulos': matriz_modulos,
    }
    
    return render(request, 'core/usuarios/gestor_permisos.html', context)


@login_required
def usuarios_gestor_permisos_intuitivo(request):
    """Gestor de permisos intuitivo y visual"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    # Obtener todos los roles y módulos
    roles = Rol.objects.all().order_by('nombre')
    modulos = Modulo.objects.filter(activo=True).order_by('nombre')
    
    context = {
        'roles': roles,
        'modulos': modulos,
    }
    
    return render(request, 'core/usuarios/gestor_permisos_intuitivo.html', context)


@login_required
def permisos_actualizar_masivo(request):
    """Actualizar permisos de forma masiva"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Sin permisos'})
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rol_id = data.get('rol_id')
            permisos_ids = data.get('permisos_ids', [])
            
            rol = get_object_or_404(Rol, id=rol_id)
            
            with transaction.atomic():
                # Desactivar todos los permisos actuales
                RolPermiso.objects.filter(rol=rol).update(activo=False)
                
                # Activar los permisos seleccionados
                for permiso_id in permisos_ids:
                    permiso = get_object_or_404(Permiso, id=permiso_id)
                    rol_permiso, created = RolPermiso.objects.get_or_create(
                        rol=rol, 
                        permiso=permiso,
                        defaults={'activo': True}
                    )
                    if not created:
                        rol_permiso.activo = True
                        rol_permiso.save()
                
                # Log de actividad
                LogActividad.objects.create(
                    usuario=request.user,
                    accion='Actualizar Permisos',
                    modulo='Usuarios',
                    descripcion=f'Permisos actualizados para rol: {rol.nombre}',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
            
            return JsonResponse({'success': True, 'message': 'Permisos actualizados exitosamente'})
            
        except Exception as e:
            logger.error(f"Error actualizando permisos: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


# ==================== DASHBOARD DE USUARIOS ====================

@login_required
def usuarios_dashboard(request):
    """Dashboard con estadísticas de usuarios y permisos"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    # Estadísticas generales
    total_usuarios = User.objects.count()
    usuarios_activos = User.objects.filter(is_active=True).count()
    superusuarios = User.objects.filter(is_superuser=True).count()
    total_roles = Rol.objects.count()
    total_permisos = Permiso.objects.count()
    
    # Usuarios por rol
    usuarios_por_rol = []
    for rol in Rol.objects.all():
        count = PerfilUsuario.objects.filter(rol=rol).count()
        if count > 0:
            usuarios_por_rol.append({
                'rol': rol.nombre,
                'count': count,
                'porcentaje': round((count / total_usuarios) * 100, 1) if total_usuarios > 0 else 0
            })
    
    # Usuarios recientes
    usuarios_recientes = User.objects.order_by('-date_joined')[:5]
    
    # Actividad reciente
    actividad_reciente = LogActividad.objects.filter(
        modulo__in=['Usuarios', 'Roles', 'Permisos']
    ).order_by('-fecha_actividad')[:10]
    
    context = {
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'superusuarios': superusuarios,
        'total_roles': total_roles,
        'total_permisos': total_permisos,
        'usuarios_por_rol': usuarios_por_rol,
        'usuarios_recientes': usuarios_recientes,
        'actividad_reciente': actividad_reciente,
    }
    
    return render(request, 'core/usuarios/dashboard.html', context)


# ==================== API PARA GESTIÓN DE MÓDULOS ====================

@login_required
def permisos_rol_modulos(request, rol_id):
    """API para obtener módulos de un rol específico"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'No tienes permisos'})
    
    try:
        rol = Rol.objects.get(id=rol_id)
        modulos = Modulo.objects.filter(activo=True).order_by('nombre')
        modulos_activos = rol.modulos_activos.values_list('id', flat=True)
        
        modulos_data = []
        for modulo in modulos:
            modulos_data.append({
                'id': modulo.id,
                'nombre': modulo.nombre,
                'descripcion': modulo.descripcion,
                'icono': modulo.icono,
            })
        
        return JsonResponse({
            'success': True,
            'modulos': modulos_data,
            'modulos_activos': list(modulos_activos)
        })
        
    except Rol.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Rol no encontrado'})
    except Exception as e:
        logger.error(f"Error obteniendo módulos del rol: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def permisos_actualizar_modulos(request):
    """Actualizar módulos de un rol de forma masiva"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'No tienes permisos'})
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rol_id = data.get('rol_id')
            modulos_ids = data.get('modulos_ids', [])
            
            if not rol_id:
                return JsonResponse({'success': False, 'error': 'ID de rol requerido'})
            
            rol = Rol.objects.get(id=rol_id)
            
            with transaction.atomic():
                # Obtener módulos seleccionados
                modulos_seleccionados = Modulo.objects.filter(id__in=modulos_ids)
                
                # Limpiar módulos actuales del rol
                rol.modulos_activos.clear()
                
                # Asignar nuevos módulos
                rol.modulos_activos.set(modulos_seleccionados)
                
                # Crear/actualizar permisos automáticamente para cada módulo
                for modulo in modulos_seleccionados:
                    # Obtener todos los permisos del módulo
                    permisos_modulo = Permiso.objects.filter(modulo=modulo)
                    
                    # Eliminar permisos actuales del rol para este módulo
                    RolPermiso.objects.filter(rol=rol, permiso__modulo=modulo).delete()
                    
                    # Crear nuevos permisos
                    for permiso in permisos_modulo:
                        RolPermiso.objects.create(rol=rol, permiso=permiso, activo=True)
                
                # Log de actividad
                LogActividad.objects.create(
                    usuario=request.user,
                    accion='Actualizar Módulos',
                    modulo='Usuarios',
                    descripcion=f'Módulos actualizados para rol: {rol.nombre} ({len(modulos_seleccionados)} módulos)',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
            
            return JsonResponse({'success': True, 'message': 'Módulos actualizados correctamente'})
            
        except Rol.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Rol no encontrado'})
        except Exception as e:
            logger.error(f"Error actualizando módulos: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
