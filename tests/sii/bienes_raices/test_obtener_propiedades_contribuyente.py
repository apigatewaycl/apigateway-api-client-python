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
from apigatewaycl.api_client.sii.bienes_raices import BienesRaices

pytestmark = pytest.mark.readonly


class TestObtenerPropiedadesContribuyente(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        firma = getenv('TEST_FIRMA_ELECTRONICA', '').strip()
        firma_clave = getenv('TEST_FIRMA_CLAVE', '').strip()
        if not (firma and firma_clave):
            raise unittest.SkipTest(
                'Se requieren TEST_FIRMA_ELECTRONICA y TEST_FIRMA_CLAVE: '
                'este recurso no admite RUT y clave, sólo certificado.'
            )
        cls.client = BienesRaices(firma, firma_clave)

    def test_obtener_propiedades_contribuyente(self):
        try:
            propiedades = self.client.propiedades_contribuyente()['data']

            self.assertIsNotNone(propiedades)

            if self.verbose:
                print(
                    'test_propiedades_contribuyente(): propiedades',
                    propiedades,
                )
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
