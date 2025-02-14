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
from apigatewaycl.api_client.sii.contribuyentes import Contribuyentes

class TestVerificarRut(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.client = Contribuyentes()

    # CASO2: verificación de cédula RUT mediante número de serie
    def test_verificar_rut(self):
        erut_serie = getenv('TEST_ERUT_SERIE', '').strip()
        if erut_serie == '':
            print('test_verificar_rut(): no probó funcionalidad.')
            return
        try:
            verificar_rut = self.client.verificar_rut(erut_serie)

            self.assertIsNotNone(verificar_rut)

            if self.verbose:
                print(
                    'test_verificar_rut(): verificar_rut', verificar_rut
                )
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
