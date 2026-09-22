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
from apigatewaycl.api_client.sii.bte import BteEmitidas

pytestmark = pytest.mark.risky


class TestAnularBteEmitida(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.contribuyente_rut = getenv(
            'TEST_CONTRIBUYENTE_IDENTIFICADOR',
            '',
        ).strip()
        contribuyente_clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        cls.client = BteEmitidas(cls.contribuyente_rut, contribuyente_clave)
        cls.periodo = getenv(
            'TEST_PERIODO',
            datetime.now(ZoneInfo('America/Santiago')).strftime('%Y%m'),
        ).strip()
        # Anular es IRREVERSIBLE en el SII. Este test nunca elige una
        # boleta por su cuenta: exige el folio exacto, para que no
        # pueda dispararse sin intención explícita.
        cls.folio = getenv('TEST_BTE_ANULAR_FOLIO', '').strip()
        if not cls.folio:
            raise unittest.SkipTest(
                'TEST_BTE_ANULAR_FOLIO no configurado: este test anula '
                'de forma irreversible una BTE real en el SII.'
            )

    # CASO 4: anular boleta
    def test_anular_bte_emitida(self):
        try:
            boleta_numero = self.folio

            anular = self.client.anular(
                self.contribuyente_rut,
                boleta_numero,
            )['data']

            self.assertIsNotNone(anular)

            if self.verbose:
                print('test_anular(): anular', anular)
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
