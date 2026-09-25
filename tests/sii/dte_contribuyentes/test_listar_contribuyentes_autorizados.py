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
from apigatewaycl.api_client.sii.dte import Contribuyentes

pytestmark = pytest.mark.readonly


class TestListarContribuyentesAutorizados(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.contribuyente_rut = getenv(
            'TEST_CONTRIBUYENTE_RUT',
            '',
        ).strip()
        firma = getenv('TEST_FIRMA_ELECTRONICA', '').strip()
        firma_clave = getenv('TEST_FIRMA_CLAVE', '').strip()
        if not (cls.contribuyente_rut and firma and firma_clave):
            raise unittest.SkipTest(
                'Se requieren TEST_CONTRIBUYENTE_RUT, '
                'TEST_FIRMA_ELECTRONICA y TEST_FIRMA_CLAVE: este '
                'recurso exige certificado digital.'
            )
        # La descarga masiva son cientos de MB y puede tardar hasta 15
        # minutos, así que no corre ni siquiera con `-m readonly` salvo
        # que se pida explícitamente.
        if getenv('TEST_DTE_AUTORIZADOS', '').strip() != '1':
            raise unittest.SkipTest(
                'TEST_DTE_AUTORIZADOS distinto de 1: la descarga masiva '
                'son cientos de MB y puede tardar hasta 15 minutos.'
            )
        cls.client = Contribuyentes(firma, firma_clave)

    def test_listar_contribuyentes_autorizados(self):
        try:
            autorizados = self.client.autorizados(formato='json')['data']

            self.assertIsNotNone(autorizados)

            if self.verbose:
                print(
                    'test_autorizados(): cantidad',
                    len(autorizados),
                )
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
