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
from apigatewaycl.api_client.sii.vehiculos import Vehiculos

pytestmark = [pytest.mark.readonly, pytest.mark.dummy]


class TestListarMarcasVehiculos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.client = Vehiculos()
        # Categoría 1 = livianos. Es un recurso público y estable.
        cls.categoria = getenv('TEST_VEHICULOS_CATEGORIA', '1').strip()

    def test_listar_marcas_vehiculos(self):
        try:
            respuesta = self.client.categorias_marcas(self.categoria)
            self.assertIn('data', respuesta)
            self.assertIn('metadata', respuesta)
            resultado = respuesta['data']

            self.assertIsNotNone(resultado)
            self.assertGreater(len(resultado), 0)
            self.assertIn('id', resultado[0])
            self.assertIn('name', resultado[0])

            if self.verbose:
                print('test_categorias_marcas(): resultado', resultado)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
