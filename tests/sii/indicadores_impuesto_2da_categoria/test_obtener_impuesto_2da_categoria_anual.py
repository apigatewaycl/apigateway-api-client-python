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
from apigatewaycl.api_client.sii.indicadores import ImpuestoSegundaCategoria

pytestmark = [pytest.mark.readonly, pytest.mark.dummy]


class TestObtenerImpuesto2daCategoriaAnual(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.client = ImpuestoSegundaCategoria()
        cls.anio = int(getenv('TEST_IMPUESTO_2DA_ANIO', '2024'))

    def test_obtener_impuesto_2da_categoria_anual(self):
        try:
            respuesta = self.client.anual(self.anio)
            self.assertIn('data', respuesta)
            self.assertIn('metadata', respuesta)
            anual = respuesta['data']

            self.assertIsNotNone(anual)

            if self.verbose:
                print('test_impuesto_2da_anual(): anual', anual)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
