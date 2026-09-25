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
from apigatewaycl.api_client.sii.dte import Emitidos

pytestmark = pytest.mark.readonly


class TestObtenerEstadoEnvioDte(unittest.TestCase):
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
        cls.track_id = getenv('TEST_DTE_TRACK_ID', '').strip()
        if not cls.track_id:
            raise unittest.SkipTest(
                'TEST_DTE_TRACK_ID no configurado: se necesita el track '
                'id de un envío real de XML al SII.'
            )
        cls.client = Emitidos(cls.contribuyente_rut, contribuyente_clave)

    def test_obtener_estado_envio_dte(self):
        try:
            estado = self.client.estado_envio(
                self.contribuyente_rut,
                int(self.track_id),
            )['data']

            self.assertIsNotNone(estado)

            if self.verbose:
                print('test_estado_envio(): estado', estado)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
