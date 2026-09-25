#
# API Gateway: Cliente de API en Python - Pruebas Unitarias.
# Copyright (C) API Gateway <https://www.apigateway.cl>
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la GNU Lesser General Public License (LGPL) publicada
# por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
# o (a su elección) cualquier versión posterior de la misma.
#
# Este programa se distribuye con la esperanza de que sea útil, pero SIN
# GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
# PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
# Public License (LGPL) para obtener una información más detallada.
#
# Debería haber recibido una copia de la GNU Lesser General Public License
# (LGPL) junto a este programa. En caso contrario, consulte
# <http://www.gnu.org/licenses/lgpl.html>.
#

import unittest
from datetime import datetime
from os import getenv
from zoneinfo import ZoneInfo

import pytest

from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.bte import BteRecibidas

pytestmark = pytest.mark.readonly


class TestListarBteRecibidas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.contribuyente_rut = getenv(
            'TEST_CONTRIBUYENTE_IDENTIFICADOR',
            '',
        ).strip()
        contribuyente_clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        if not (cls.contribuyente_rut and contribuyente_clave):
            raise unittest.SkipTest(
                'Se requieren TEST_CONTRIBUYENTE_IDENTIFICADOR y '
                'TEST_CONTRIBUYENTE_CLAVE.'
            )
        cls.client = BteRecibidas(cls.contribuyente_rut, contribuyente_clave)
        cls.periodo = getenv(
            'TEST_PERIODO',
            datetime.now(ZoneInfo('America/Santiago')).strftime('%Y%m'),
        ).strip()

    # `periodo` acepta AAAAMM (mensual) o AAAAMMDD (diario), y la
    # respuesta es paginada: `pagina` parte en 1.
    def test_listar_bte_recibidas(self):
        try:
            recibidas = self.client.documentos(
                self.contribuyente_rut,
                self.periodo,
                1,
            )['data']

            self.assertIsNotNone(recibidas)
            # Con resultados la API responde
            # {'boletas': [...], 'metadata': {...}}; sin resultados
            # responde una lista vacía, no ese dict.
            if recibidas:
                self.assertIn('metadata', recibidas)
                self.assertIn('boletas', recibidas)

            if self.verbose:
                print('test_documentos(): recibidas', recibidas)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
