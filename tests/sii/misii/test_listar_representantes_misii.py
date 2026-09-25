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
from apigatewaycl.api_client.sii.misii import Representantes

pytestmark = pytest.mark.readonly


class TestListarRepresentantesMisii(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        identificador = getenv(
            'TEST_CONTRIBUYENTE_IDENTIFICADOR',
            '',
        ).strip()
        clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        if not (identificador and clave):
            raise unittest.SkipTest(
                'Se requieren TEST_CONTRIBUYENTE_IDENTIFICADOR y '
                'TEST_CONTRIBUYENTE_CLAVE.'
            )
        cls.client = Representantes(identificador, clave)

    def test_listar_representantes_misii(self):
        try:
            listado = self.client.listado()['data']

            self.assertIsNotNone(listado)
            self.assertIn('representado', listado)

            if self.verbose:
                print('test_representantes_listado(): listado', listado)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
