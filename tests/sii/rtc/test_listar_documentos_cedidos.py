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
from datetime import datetime, timedelta
from os import getenv
from zoneinfo import ZoneInfo

import pytest

from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.rtc import Cesiones

pytestmark = pytest.mark.readonly


class TestListarDocumentosCedidos(unittest.TestCase):
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
        cls.client = Cesiones(cls.contribuyente_rut, contribuyente_clave)
        # El período de consulta admite un mes como máximo.
        hoy = datetime.now(ZoneInfo('America/Santiago')).date()
        cls.desde = getenv(
            'TEST_RTC_DESDE',
            (hoy - timedelta(days=30)).isoformat(),
        ).strip()
        cls.hasta = getenv('TEST_RTC_HASTA', hoy.isoformat()).strip()
        # 0 = deudor, 1 = cedente, 2 = cesionario.
        cls.consulta = getenv('TEST_RTC_CONSULTA', '0').strip()

    def test_listar_documentos_cedidos(self):
        try:
            cesiones = self.client.documentos(
                self.desde,
                self.hasta,
                self.consulta,
            )['data']

            self.assertIsNotNone(cesiones)

            if self.verbose:
                print('test_documentos(): cesiones', cesiones)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})

    # Con `formato` la API responde el archivo crudo en vez de JSON.
    def test_listar_documentos_cedidos_csv(self):
        try:
            csv = self.client.documentos(
                self.desde,
                self.hasta,
                self.consulta,
                formato='csv',
            )

            self.assertIsNotNone(csv)
            self.assertIsInstance(csv, bytes)

            if self.verbose:
                print('test_documentos_csv(): bytes', len(csv))
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
