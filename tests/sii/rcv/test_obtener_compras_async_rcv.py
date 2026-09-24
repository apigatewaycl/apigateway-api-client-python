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

import time
import unittest
from datetime import datetime
from os import getenv
from zoneinfo import ZoneInfo

import pytest

from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.rcv import Rcv

pytestmark = pytest.mark.readonly


class TestObtenerComprasAsyncRcv(unittest.TestCase):
    # El SII procesa la solicitud en segundo plano: se consulta el estado
    # hasta que termine, con un tope para no dejar el test colgado.
    INTENTOS_ESTADO = 10
    ESPERA_ESTADO = 3

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        identificador = getenv('TEST_CONTRIBUYENTE_IDENTIFICADOR', '').strip()
        clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        cls.client = Rcv(identificador, clave)
        # El receptor puede ser una empresa distinta de quien autentica.
        cls.receptor = (
            getenv('TEST_CONTRIBUYENTE_RUT', '').strip() or identificador
        )
        cls.periodo = getenv(
            'TEST_PERIODO',
            datetime.now(ZoneInfo('America/Santiago')).strftime('%Y%m'),
        ).strip()
        cls.dte = int(getenv('TEST_RCV_COMPRAS_DTE', '0'))
        # Sin `TEST_CERTIFICACION` se consulta producción.
        cls.certificacion = getenv('TEST_CERTIFICACION', '').strip() or None

    # CASO 1: descarga diferida de compras: solicitar, esperar a que el
    # SII la termine y bajar el detalle. `estado` y `detalle` necesitan el
    # `id` que entrega `solicitar`, por eso van en un mismo flujo.
    def test_obtener_compras_async_rcv(self):
        try:
            solicitud = self.client.compras_async_solicitar(
                self.receptor,
                self.periodo,
                self.dte,
                certificacion=self.certificacion,
            )['data']
            if self.verbose:
                print('test_compras_async(): solicitud', solicitud)
            self.assertIn('id', solicitud)
            id_solicitud = str(solicitud['id'])

            for _intento in range(self.INTENTOS_ESTADO):
                estado = self.client.compras_async_estado(
                    self.receptor,
                    self.periodo,
                    id_solicitud,
                    self.dte,
                    certificacion=self.certificacion,
                )['data']
                if self.verbose:
                    print('test_compras_async(): estado', estado)
                self.assertEqual(str(estado['id']), id_solicitud)
                if estado['estado'] == 'TERMINADO':
                    break
                time.sleep(self.ESPERA_ESTADO)
            else:
                self.skipTest(
                    'el SII no terminó la solicitud %(id)s a tiempo.'
                    % {'id': id_solicitud},
                )

            detalle = self.client.compras_async_detalle(
                self.receptor,
                self.periodo,
                id_solicitud,
                self.dte,
                certificacion=self.certificacion,
            )['data']
            if self.verbose:
                print('test_compras_async(): detalle', detalle)
            self.assertIsInstance(detalle, list)
            self.assertEqual(len(detalle), estado['registros'])
        except ApiException as e:
            self.fail('ApiException: %(e)s' % {'e': e})
