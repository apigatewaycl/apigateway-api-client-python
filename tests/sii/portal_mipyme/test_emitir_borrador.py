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

import json
import unittest
from os import getenv

import pytest

from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.portal_mipyme import Borradores

pytestmark = pytest.mark.risky


class TestEmitirBorrador(unittest.TestCase):
    # El DTE va como JSON en una variable de entorno, con la misma
    # forma que recibe la API. Crea un borrador real en el Portal
    # MIPYME (no emite un DTE ante el SII).
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.identificador = getenv(
            'TEST_USUARIO_IDENTIFICADOR',
            '',
        ).strip()
        clave = getenv('TEST_USUARIO_CLAVE', '').strip()
        if not (cls.identificador and clave):
            raise unittest.SkipTest(
                'Se requieren TEST_USUARIO_IDENTIFICADOR y '
                'TEST_USUARIO_CLAVE de un usuario del Portal MIPYME.'
            )
        cls.emisor = getenv(
            'TEST_PORTAL_MIPYME_CONTRIBUYENTE_RUT',
            cls.identificador,
        ).strip()
        cls.client = Borradores(cls.identificador, clave)
        dte = getenv('TEST_MIPYME_BORRADOR_DTE', '').strip()
        if not dte:
            raise unittest.SkipTest(
                'TEST_MIPYME_BORRADOR_DTE no configurado: este test crea '
                'un borrador real en el Portal MIPYME.'
            )
        cls.dte = json.loads(dte)

    def test_emitir_borrador(self):
        try:
            borrador = self.client.emitir(self.dte)['data']

            self.assertIsNotNone(borrador)

            if self.verbose:
                print('test_emitir(): borrador', borrador)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
