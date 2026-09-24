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
from apigatewaycl.api_client.sii.caf import Caf

pytestmark = pytest.mark.readonly


class TestObtenerEstadoTimbrajeCaf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.emisor = getenv('TEST_CONTRIBUYENTE_RUT', '').strip()
        firma = getenv('TEST_FIRMA_ELECTRONICA', '').strip()
        firma_clave = getenv('TEST_FIRMA_CLAVE', '').strip()
        if not (cls.emisor and firma and firma_clave):
            raise unittest.SkipTest(
                'Se requieren TEST_CONTRIBUYENTE_RUT, '
                'TEST_FIRMA_ELECTRONICA y TEST_FIRMA_CLAVE: el CAF '
                'exige certificado digital.'
            )
        cls.dte = int(getenv('TEST_CAF_DTE', '33'))
        cls.client = Caf(firma, firma_clave)

    def test_obtener_estado_timbraje_caf(self):
        try:
            respuesta = self.client.estado_timbraje(self.emisor, self.dte)
            timbraje = respuesta['data']

            self.assertIsNotNone(timbraje)
            self.assertIn('dte', timbraje)
            self.assertIn('contribuyente', timbraje)

            if self.verbose:
                print('test_estado_timbraje(): timbraje', timbraje)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
