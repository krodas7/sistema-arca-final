"""
Servicio de integración entre Django y la API AWS de asistencias.
Centraliza todas las llamadas HTTP a la API Gateway de AWS.
"""
import json
import logging
import urllib.request
import urllib.error
from datetime import datetime

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


# ==================== ASISTENCIAS ====================

def obtener_asistencias_proyecto(project_id: int) -> list:
    """Retorna lista de asistencias de un proyecto desde AWS. Vacío si hay error."""
    result = _request('GET', f'/attendance?projectId={project_id}')
    if result['ok'] and isinstance(result['data'], dict):
        registros = result['data'].get('data', [])
        return _procesar_registros(registros)
    logger.warning(f'No se pudieron obtener asistencias para proyecto {project_id}: {result.get("error")}')
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
