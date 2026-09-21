"""Configuración común de los tests.

Hace dos cosas antes de que corra cualquier test:

1. Carga `tests/test.env` (no versionado). `tests/run.py` (el runner
   viejo) llamaba `load_dotenv()` a mano — con `pytest` como runner
   nadie lo hacía, así que el token y los RUT de prueba no llegaban.

2. Omite la suite completa si las credenciales no sirven. Todos los
   tests consultan la API real: sin un token aceptado no prueban nada
   del código, y fallarían con un 401 que solo genera ruido. El motivo
   queda explícito en el reporte para quien administre el repositorio.
"""

from os import getenv
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv

from apigatewaycl.api_client import ApiClient

load_dotenv(Path(__file__).parent / 'test.env')

_TOKEN = 'APIGATEWAY_API_TOKEN'

# Recurso liviano y de solo lectura, disponible tanto en v1 como en v2,
# que no depende de los datos de ninguna cuenta en particular.
_SONDEO = '/sii/indicadores/uf/anual/2025'

_HTTP_SIN_AUTORIZACION = (401, 403)


def _motivo_omision() -> str | None:
    """Motivo por el cual omitir la suite, o `None` si puede correr."""
    if not getenv(_TOKEN, '').strip():
        return '%(var)s no configurado: los tests consultan la API real.' % {
            'var': _TOKEN
        }
    try:
        respuesta = ApiClient(raise_for_status=False).get(_SONDEO)
    except requests.RequestException as error:
        return 'no se pudo contactar la API: %(error)s' % {'error': error}
    if respuesta.status_code in _HTTP_SIN_AUTORIZACION:
        return (
            'la API rechazó %(var)s con HTTP %(codigo)s: es un problema '
            'de credenciales del repositorio, no del código.'
            % {'var': _TOKEN, 'codigo': respuesta.status_code}
        )
    return None


def pytest_collection_modifyitems(items):
    """Marca toda la suite como omitida si no hay credenciales usables."""
    if not items:
        return
    motivo = _motivo_omision()
    if motivo is None:
        return
    omitir = pytest.mark.skip(reason=motivo)
    for item in items:
        item.add_marker(omitir)
