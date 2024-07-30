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
from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.actividades_economicas import ActividadesEconomicas

class TestSiiActividadesEconomicas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.client = ActividadesEconomicas()

    def test_listado(self):
        try:
            listado = self.client.listado()
            if self.verbose:
                print('test_listado(): listado', listado)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    def test_listado_primera_categoria(self):
        try:
            listado_primera_categoria = self.client.listado_primera_categoria()
            if self.verbose:
                print('test_listado_primera_categoria(): listado_primera_categoria', listado_primera_categoria)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    def test_listado_segunda_categoria(self):
        try:
            listado_segunda_categoria = self.client.listado_segunda_categoria()
            if self.verbose:
                print('test_listado_segunda_categoria(): listado_segunda_categoria', listado_segunda_categoria)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
