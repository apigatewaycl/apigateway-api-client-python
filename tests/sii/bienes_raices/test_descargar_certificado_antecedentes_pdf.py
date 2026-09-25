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


class TestDescargarCertificadoAntecedentesPdf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.client = BienesRaices()
        cls.comuna = int(getenv('TEST_BIENES_RAICES_COMUNA', '13101'))
        cls.manzana = int(getenv('TEST_BIENES_RAICES_MANZANA', '1'))
        cls.predio = int(getenv('TEST_BIENES_RAICES_PREDIO', '1'))
        propiedades = cls.client.propiedades_rol(
            cls.comuna,
            cls.manzana,
            cls.predio,
        )['data']
        if not propiedades:
            raise unittest.SkipTest(
                'el rol %(comuna)s-%(manzana)s-%(predio)s no devolvió '
                'propiedades con las cuales probar.'
                % {
                    'comuna': cls.comuna,
                    'manzana': cls.manzana,
                    'predio': cls.predio,
                }
            )
        cls.eac = propiedades[0]['ultimoEacAplicado']

    def test_descargar_certificado_antecedentes_pdf(self):
        try:
            pdf = self.client.certificado_antecedentes_pdf(
                self.comuna,
                self.manzana,
                self.predio,
                self.eac,
            )

            self.assertIsNotNone(pdf)
            # La API responde el archivo crudo, no JSON.
            self.assertTrue(pdf.startswith(b'%PDF'))

            if self.verbose:
                print('test_antecedentes_pdf(): bytes', len(pdf))
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
