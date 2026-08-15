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

class TestObtenerSituacionTributaria(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.client = Contribuyentes()

    # CASO 1: situación tributaria
    def test_obtener_situacion_tributaria(self):
        contribuyente_rut = getenv('TEST_CONTRIBUYENTE_IDENTIFICADOR', '').strip()
        if contribuyente_rut == '':
            print('test_situacion_tributaria(): no probó funcionalidad.')
            return
        try:
            situacion_tributaria = self.client.situacion_tributaria(contribuyente_rut)

            self.assertIsNotNone(situacion_tributaria)

            if self.verbose:
                print(
                    'test_situacion_tributaria(): situacion_tributaria',
                    situacion_tributaria
                )
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
