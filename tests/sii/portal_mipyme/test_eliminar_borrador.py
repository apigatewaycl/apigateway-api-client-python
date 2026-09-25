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
from apigatewaycl.api_client.sii.portal_mipyme import Borradores

pytestmark = pytest.mark.risky


class TestEliminarBorrador(unittest.TestCase):
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
        cls.codigo = getenv(
            'TEST_MIPYME_BORRADOR_ELIMINAR',
            '',
        ).strip()
        if not cls.codigo:
            raise unittest.SkipTest(
                'TEST_MIPYME_BORRADOR_ELIMINAR no configurado: este test '
                'borra un borrador real del Portal MIPYME.'
            )

    def test_eliminar_borrador(self):
        try:
            eliminado = self.client.eliminar(self.emisor, self.codigo)['data']

            self.assertIsNotNone(eliminado)

            if self.verbose:
                print('test_eliminar(): eliminado', eliminado)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
