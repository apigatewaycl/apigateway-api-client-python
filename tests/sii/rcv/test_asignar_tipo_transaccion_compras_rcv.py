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

import json
import unittest
from datetime import datetime
from os import getenv
from zoneinfo import ZoneInfo

import pytest

from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.rcv import Rcv

pytestmark = pytest.mark.risky


class TestAsignarTipoTransaccionComprasRcv(unittest.TestCase):
    # Los documentos van en una variable de entorno con el mismo JSON
    # que recibe la API, para no inventar folios ni tocar documentos
    # del RCV que no se hayan elegido a propósito. Ejemplo:
    # [{"emisor": "77666555-4", "dte": 33, "folio": 1,
    #   "tipo_transaccion": 1, "codigo_iva": 1}]
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        cls.contribuyente_rut = getenv(
            'TEST_CONTRIBUYENTE_IDENTIFICADOR',
            '',
        ).strip()
        contribuyente_clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        cls.periodo = getenv(
            'TEST_PERIODO',
            datetime.now(ZoneInfo('America/Santiago')).strftime('%Y%m'),
        ).strip()
        documentos = getenv('TEST_RCV_COMPRAS_DOCUMENTOS', '').strip()
        if not documentos:
            raise unittest.SkipTest(
                'TEST_RCV_COMPRAS_DOCUMENTOS no configurado: este test '
                'le cambia el tipo de transacción a documentos reales '
                'del RCV.'
            )
        cls.documentos = json.loads(documentos)
        cls.client = Rcv(cls.contribuyente_rut, contribuyente_clave)

    def test_asignar_tipo_transaccion_compras_rcv(self):
        try:
            resultado = self.client.compras_set_tipo_transaccion(
                self.contribuyente_rut,
                self.periodo,
                self.documentos,
            )['data']

            if self.verbose:
                print(
                    'test_compras_set_tipo_transaccion(): resultado',
                    resultado,
                )
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
