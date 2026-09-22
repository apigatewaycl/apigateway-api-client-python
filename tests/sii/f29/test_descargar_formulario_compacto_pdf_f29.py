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
from datetime import datetime
from os import getenv
from zoneinfo import ZoneInfo

import pytest

from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.f29 import F29

pytestmark = pytest.mark.readonly


class TestDescargarFormularioCompactoPdfF29(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        identificador = getenv(
            'TEST_CONTRIBUYENTE_IDENTIFICADOR',
            '',
        ).strip()
        clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        if not (identificador and clave):
            raise unittest.SkipTest(
                'Se requieren TEST_CONTRIBUYENTE_IDENTIFICADOR y '
                'TEST_CONTRIBUYENTE_CLAVE.'
            )
        cls.client = F29(identificador, clave)
        cls.anio = getenv(
            'TEST_F29_ANIO',
            datetime.now(ZoneInfo('America/Santiago')).strftime('%Y'),
        ).strip()

    def _primer_folio(self):
        declaraciones = self.client.declaraciones_listado(self.anio)['data']
        if not declaraciones:
            self.skipTest(
                'la API no devolvió declaraciones del %(anio)s con las '
                'cuales probar.' % {'anio': self.anio}
            )
        return declaraciones[0]['folio']

    def test_formulario_compacto_pdf(self):
        try:
            folio = self._primer_folio()
            pdf = self.client.formulario_compacto_pdf(folio)

            self.assertIsNotNone(pdf)
            # La API responde el archivo crudo, no JSON.
            self.assertTrue(pdf.startswith(b'%PDF'))

            if self.verbose:
                print('test_formulario_compacto_pdf(): bytes', len(pdf))
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
