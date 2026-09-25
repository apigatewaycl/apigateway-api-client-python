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


class TestBuscarTasacionVehiculo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.client = Vehiculos()
        cls.categoria = int(getenv('TEST_VEHICULOS_CATEGORIA', '1'))
        # 6 = SUV. `categoria` y `tipo` son obligatorios para la API.
        cls.tipo = int(getenv('TEST_VEHICULOS_TIPO', '6'))
        # `marca` y `anio` no son obligatorios, pero la búsqueda sólo
        # con categoría y tipo es inestable: el SII responde
        # intermitentemente "No fue posible obtener la tasación", y a
        # veces HTML en vez de JSON. Acotándola es reproducible.
        cls.marca = int(getenv('TEST_VEHICULOS_MARCA', '229'))
        cls.anio = int(getenv('TEST_VEHICULOS_ANIO', '2020'))

    def test_buscar_tasacion_vehiculo(self):
        try:
            respuesta = self.client.buscar(
                categoria=self.categoria,
                tipo=self.tipo,
                marca=self.marca,
                anio=self.anio,
            )
            self.assertIn('data', respuesta)
            self.assertIn('metadata', respuesta)
            vehiculos = respuesta['data']

            self.assertIsNotNone(vehiculos)
            self.assertGreater(len(vehiculos), 0)
            self.assertIn('marca', vehiculos[0])
            self.assertIn('montoTasa', vehiculos[0])

            if self.verbose:
                print('test_buscar(): cantidad', len(vehiculos))
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})

    # Sin `categoria` ni `tipo` la API rechaza la búsqueda: se
    # comprueba que el error llegue como ApiException y no como algo
    # más raro.
    def test_buscar_tasacion_vehiculo_sin_filtros_obligatorios(self):
        with self.assertRaises(ApiException):
            self.client.buscar()
