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
from os import getenv

import pytest

from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.dte import Iecv

pytestmark = pytest.mark.readonly


class TestObtenerCodigoReemplazoIecv(unittest.TestCase):
    # Sólo aplica a períodos de 201707 hacia atrás, y necesita el
    # track id del envío del libro que se quiere reemplazar.
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
        cls.periodo = getenv('TEST_IECV_PERIODO', '').strip()
        cls.track_id = getenv('TEST_IECV_TRACK_ID', '').strip()
        if not (cls.periodo and cls.track_id):
            raise unittest.SkipTest(
                'Se requieren TEST_IECV_PERIODO (AAAAMM, 201707 o '
                'anterior) y TEST_IECV_TRACK_ID del libro a reemplazar.'
            )
        cls.operacion = getenv('TEST_IECV_OPERACION', 'VENTA').strip()
        cls.tipo = getenv('TEST_IECV_TIPO', 'MENSUAL').strip()
        cls.client = Iecv(cls.contribuyente_rut, contribuyente_clave)

    def test_obtener_codigo_reemplazo_iecv(self):
        try:
            codigo = self.client.codigo_reemplazo(
                self.contribuyente_rut,
                self.periodo,
                self.operacion,
                self.tipo,
                int(self.track_id),
            )['data']

            self.assertIsNotNone(codigo)

            if self.verbose:
                print('test_codigo_reemplazo(): codigo', codigo)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
