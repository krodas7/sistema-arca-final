"""
Servicio de integración entre Django y la API AWS de asistencias.
Centraliza todas las llamadas HTTP a la API Gateway de AWS.
"""
import hashlib
import json
import logging
import uuid
import urllib.request
import urllib.error
from datetime import datetime, timezone

from django.conf import settings

logger = logging.getLogger(__name__)

BASE_URL = getattr(settings, 'AWS_API_BASE_URL', '').rstrip('/')
TIMEOUT = getattr(settings, 'AWS_API_TIMEOUT', 10)


def _request(method: str, path: str, body: dict = None) -> dict:
    """Ejecuta una petición HTTP a la API de AWS. Retorna dict con keys: ok, status, data, error."""
    if not BASE_URL:
        return {'ok': False, 'status': 0, 'data': None, 'error': 'AWS_API_BASE_URL no configurado'}

    url = f"{BASE_URL}{path}"
    payload = json.dumps(body).encode('utf-8') if body is not None else None

    req = urllib.request.Request(
        url,
        data=payload,
        method=method,
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode('utf-8')
            data = json.loads(raw) if raw else {}
            logger.info(f'AWS API {method} {path} → {resp.status}')
            return {'ok': True, 'status': resp.status, 'data': data, 'error': None}
    except urllib.error.HTTPError as e:
        raw = e.read().decode('utf-8') if e.fp else ''
        logger.warning(f'AWS API {method} {path} → HTTP {e.code}: {raw[:200]}')
        try:
            data = json.loads(raw)
        except Exception:
            data = {'raw': raw}
        return {'ok': False, 'status': e.code, 'data': data, 'error': f'HTTP {e.code}'}
    except urllib.error.URLError as e:
        logger.error(f'AWS API {method} {path} → URLError: {e.reason}')
        return {'ok': False, 'status': 0, 'data': None, 'error': str(e.reason)}
    except Exception as e:
        logger.error(f'AWS API {method} {path} → Error inesperado: {e}')
        return {'ok': False, 'status': 0, 'data': None, 'error': str(e)}


# ==================== GEOCERCAS ====================

def guardar_geocerca_circulo(project_id: int, lat: float, lng: float, radio_metros: float) -> dict:
    """Guarda o actualiza una geocerca circular para un proyecto en AWS."""
    return _request('PUT', f'/projects/{project_id}/geofence', {
        'type': 'circle',
        'center': {'lat': lat, 'lng': lng},
        'radiusMeters': radio_metros,
    })


def guardar_geocerca_poligono(project_id: int, coordenadas: list) -> dict:
    """Guarda o actualiza una geocerca poligonal para un proyecto en AWS.
    coordenadas: lista de [lat, lng] con al menos 3 puntos.
    """
    return _request('PUT', f'/projects/{project_id}/geofence', {
        'type': 'polygon',
        'coordinates': coordenadas,
    })


def eliminar_geocerca(project_id: int) -> dict:
    """Elimina la geocerca de un proyecto enviando coordenadas vacías (no soportado nativamente; usa PUT con radio=0)."""
    return _request('PUT', f'/projects/{project_id}/geofence', {
        'type': 'circle',
        'center': {'lat': 0, 'lng': 0},
        'radiusMeters': 0,
    })


def obtener_geocerca_proyecto(project_id: int) -> dict | None:
    """Obtiene la geocerca activa de un proyecto desde Django DB (fuente local de verdad)."""
    try:
        from core.models import GeocercaProyecto
        g = GeocercaProyecto.objects.select_related('proyecto').get(
            proyecto_id=project_id, activa=True
        )
        lat, lng = g.centro
        return {
            'tipo': g.tipo,
            'configuracion': g.configuracion,
            'resumen': g.resumen,
            'centro': [lat, lng],
            'centro_lat': lat,
            'centro_lng': lng,
            'actualizado_en': g.actualizado_en,
        }
    except Exception:
        return None


# ==================== ASISTENCIAS ====================

def obtener_asistencias_proyecto(project_id: int) -> list:
    """Retorna lista de asistencias de un proyecto desde AWS. Vacío si hay error."""
    result = _request('GET', f'/attendance?projectId={project_id}')
    if result['ok'] and isinstance(result['data'], dict):
        registros = result['data'].get('data', [])
        return _procesar_registros(registros)
    logger.warning(f'No se pudieron obtener asistencias para proyecto {project_id}: {result.get("error")}')
    return []


def obtener_todas_asistencias_dynamo() -> list:
    """Escanea directamente DynamoDB para obtener TODOS los registros de asistencia
    sin filtrar por proyecto. Útil para el dashboard global."""
    try:
        import boto3
        from django.conf import settings as dj_settings
        client = boto3.client(
            'dynamodb',
            region_name=getattr(dj_settings, 'AWS_DEFAULT_REGION', 'us-east-2'),
            aws_access_key_id=getattr(dj_settings, 'AWS_ACCESS_KEY_ID', None),
            aws_secret_access_key=getattr(dj_settings, 'AWS_SECRET_ACCESS_KEY', None),
        )
        items = []
        kwargs = {'TableName': 'AsistenciaRecords'}
        while True:
            resp = client.scan(**kwargs)
            for item in resp.get('Items', []):
                flat = {k: list(v.values())[0] for k, v in item.items()}
                # Normalizar tipos
                for campo in ('timestamp',):
                    if campo in flat:
                        try:
                            flat[campo] = int(flat[campo])
                        except (ValueError, TypeError):
                            pass
                for campo in ('verified',):
                    if campo in flat:
                        flat[campo] = flat[campo] in (True, 'true', 'True', '1')
                items.append(flat)
            last = resp.get('LastEvaluatedKey')
            if not last:
                break
            kwargs['ExclusiveStartKey'] = last
        return _procesar_registros(items)
    except Exception as e:
        logger.error(f'obtener_todas_asistencias_dynamo: {e}')
        return []


def obtener_asistencias_usuario(user_id: str) -> list:
    """Retorna asistencias de un usuario específico desde AWS."""
    result = _request('GET', f'/attendance/{user_id}')
    if result['ok'] and isinstance(result['data'], dict):
        registros = result['data'].get('data', [])
        return _procesar_registros(registros)
    return []


def _procesar_registros(registros: list) -> list:
    """Convierte timestamps de milisegundos a datetime legible y añade campos útiles."""
    TIPOS = {
        'entry': 'Entrada',
        'exit': 'Salida',
        'lunch_out': 'Salida Almuerzo',
        'lunch_in': 'Retorno Almuerzo',
    }
    processed = []
    for r in registros:
        ts = r.get('timestamp', 0)
        if ts:
            try:
                r['datetime_obj'] = datetime.fromtimestamp(ts / 1000)
                r['fecha_str'] = r['datetime_obj'].strftime('%d/%m/%Y')
                r['hora_str'] = r['datetime_obj'].strftime('%H:%M:%S')
            except Exception:
                r['fecha_str'] = '-'
                r['hora_str'] = '-'
        r['tipo_display'] = TIPOS.get(r.get('type', ''), r.get('type', '-'))
        r['similitud_pct'] = f"{r.get('similarity', 0):.1f}%" if r.get('similarity') else '-'
        processed.append(r)
    return processed


# ==================== USUARIOS ====================

def obtener_usuarios_proyecto(project_id: int) -> list:
    """Retorna usuarios registrados para un proyecto desde AWS."""
    result = _request('GET', '/users')
    if result['ok'] and isinstance(result['data'], dict):
        usuarios = result['data'].get('data', [])
        pid_str = str(project_id)
        return [u for u in usuarios if str(u.get('projectId', '')) == pid_str]
    return []


def obtener_todos_usuarios() -> list:
    """Retorna todos los usuarios registrados en AWS."""
    result = _request('GET', '/users')
    if result['ok'] and isinstance(result['data'], dict):
        return result['data'].get('data', [])
    return []


def registrar_usuario_rekognition(nombre: str, project_id: int, foto_base64: str, email: str = '') -> dict:
    """
    Registra un trabajador en AWS Rekognition + DynamoDB.
    foto_base64: imagen en base64 (sin prefijo data:image/...;base64,)
    """
    body = {
        'name': nombre,
        'projectId': str(project_id),
        'photoBase64': foto_base64,
    }
    if email:
        body['email'] = email
    return _request('POST', '/registerUser', body)


def eliminar_usuario_rekognition(user_id: str) -> dict:
    """Elimina un usuario de AWS Rekognition + DynamoDB."""
    return _request('DELETE', f'/users/{user_id}')


def obtener_usuarios_aws_por_proyecto(project_id: int) -> list:
    """Retorna usuarios registrados en AWS para un proyecto específico."""
    return obtener_usuarios_proyecto(project_id)


# ===========================================================================
# Gestión de Usuarios App Móvil (AsistenciaAppUsers en DynamoDB)
# Operaciones directas a DynamoDB — no pasan por API Gateway.
# ===========================================================================

def _dynamo_resource():
    """Retorna un recurso DynamoDB de boto3 con la región configurada."""
    try:
        import boto3
        return boto3.resource('dynamodb', region_name='us-east-2')
    except ImportError:
        logger.error('boto3 no está instalado.')
        return None


def listar_usuarios_app() -> list:
    """Retorna todos los usuarios de la app desde AsistenciaAppUsers."""
    dynamodb = _dynamo_resource()
    if not dynamodb:
        return []
    try:
        table = dynamodb.Table('AsistenciaAppUsers')
        response = table.scan()
        usuarios = response.get('Items', [])
        # Ordenar por nombre
        return sorted(usuarios, key=lambda u: u.get('name', '').lower())
    except Exception as e:
        logger.error(f'Error listando usuarios app: {e}')
        return []


def crear_usuario_app(nombre: str, email: str, password: str, project_id: str) -> dict:
    """
    Crea un nuevo usuario en AsistenciaAppUsers.
    La contraseña se almacena como SHA-256 (igual que el Lambda de login).
    """
    dynamodb = _dynamo_resource()
    if not dynamodb:
        return {'ok': False, 'error': 'boto3 no disponible'}
    try:
        table = dynamodb.Table('AsistenciaAppUsers')

        # Verificar que el email no exista ya
        response = table.scan(
            FilterExpression='email = :e',
            ExpressionAttributeValues={':e': email.strip().lower()}
        )
        if response.get('Items'):
            return {'ok': False, 'error': f'Ya existe un usuario con el email {email}'}

        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        new_id = str(uuid.uuid4())
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        item = {
            'userId': new_id,
            'email': email.strip().lower(),
            'name': nombre.strip(),
            'passwordHash': password_hash,
            'projectId': str(project_id),
            'isActive': True,
            'createdAt': now_ms,
            'updatedAt': now_ms,
        }
        table.put_item(Item=item)
        logger.info(f'Usuario app creado: email={email} projectId={project_id}')
        return {'ok': True, 'userId': new_id}

    except Exception as e:
        logger.error(f'Error creando usuario app: {e}')
        return {'ok': False, 'error': str(e)}


def actualizar_password_usuario_app(user_id: str, nueva_password: str) -> dict:
    """Actualiza la contraseña de un usuario app."""
    dynamodb = _dynamo_resource()
    if not dynamodb:
        return {'ok': False, 'error': 'boto3 no disponible'}
    try:
        table = dynamodb.Table('AsistenciaAppUsers')
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        password_hash = hashlib.sha256(nueva_password.encode('utf-8')).hexdigest()
        table.update_item(
            Key={'userId': user_id},
            UpdateExpression='SET passwordHash = :ph, updatedAt = :ua',
            ExpressionAttributeValues={':ph': password_hash, ':ua': now_ms},
        )
        return {'ok': True}
    except Exception as e:
        logger.error(f'Error actualizando password usuario app {user_id}: {e}')
        return {'ok': False, 'error': str(e)}


def toggle_activo_usuario_app(user_id: str, activo: bool) -> dict:
    """Activa o desactiva un usuario app."""
    dynamodb = _dynamo_resource()
    if not dynamodb:
        return {'ok': False, 'error': 'boto3 no disponible'}
    try:
        table = dynamodb.Table('AsistenciaAppUsers')
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        table.update_item(
            Key={'userId': user_id},
            UpdateExpression='SET isActive = :ia, updatedAt = :ua',
            ExpressionAttributeValues={':ia': activo, ':ua': now_ms},
        )
        return {'ok': True}
    except Exception as e:
        logger.error(f'Error actualizando estado usuario app {user_id}: {e}')
        return {'ok': False, 'error': str(e)}


def eliminar_usuario_app(user_id: str) -> dict:
    """Elimina permanentemente un usuario app de DynamoDB."""
    dynamodb = _dynamo_resource()
    if not dynamodb:
        return {'ok': False, 'error': 'boto3 no disponible'}
    try:
        table = dynamodb.Table('AsistenciaAppUsers')
        table.delete_item(Key={'userId': user_id})
        logger.info(f'Usuario app eliminado: userId={user_id}')
        return {'ok': True}
    except Exception as e:
        logger.error(f'Error eliminando usuario app {user_id}: {e}')
        return {'ok': False, 'error': str(e)}
