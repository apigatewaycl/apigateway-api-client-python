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
from apigatewaycl.api_client.sii.caf import Caf

pytestmark = pytest.mark.readonly


class TestObtenerXmlCaf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.emisor = getenv('TEST_CONTRIBUYENTE_RUT', '').strip()
        firma = getenv('TEST_FIRMA_ELECTRONICA', '').strip()
        firma_clave = getenv('TEST_FIRMA_CLAVE', '').strip()
        if not (cls.emisor and firma and firma_clave):
            raise unittest.SkipTest(
                'Se requieren TEST_CONTRIBUYENTE_RUT, '
                'TEST_FIRMA_ELECTRONICA y TEST_FIRMA_CLAVE: el CAF '
                'exige certificado digital.'
            )
        cls.dte = int(getenv('TEST_CAF_DTE', '33'))
        folio_inicial = getenv('TEST_CAF_FOLIO_INICIAL', '').strip()
        folio_final = getenv('TEST_CAF_FOLIO_FINAL', '').strip()
        cls.fecha_autorizacion = getenv(
            'TEST_CAF_FECHA_AUTORIZACION',
            '',
        ).strip()
        if not (folio_inicial and folio_final and cls.fecha_autorizacion):
            raise unittest.SkipTest(
                'Se requieren TEST_CAF_FOLIO_INICIAL, '
                'TEST_CAF_FOLIO_FINAL y TEST_CAF_FECHA_AUTORIZACION de '
                'un CAF ya solicitado.'
            )
        cls.folio_inicial = int(folio_inicial)
        cls.folio_final = int(folio_final)
        cls.client = Caf(firma, firma_clave)

    def test_obtener_xml_caf(self):
        try:
            xml = self.client.xml(
                self.emisor,
                self.dte,
                self.folio_inicial,
                self.folio_final,
                self.fecha_autorizacion,
            )

            self.assertIsNotNone(xml)
            self.assertIn('<AUTORIZACION>', xml)

            if self.verbose:
                print('test_xml(): xml', xml)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
