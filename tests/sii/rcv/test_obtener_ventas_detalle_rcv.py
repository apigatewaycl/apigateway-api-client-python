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
from datetime import datetime
from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.rcv import Rcv

class TestObtenerVentasDetalleRcv(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('TEST_CONTRIBUYENTE_IDENTIFICADOR', '').strip()
        contribuyente_clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        cls.client = Rcv(cls.contribuyente_rut, contribuyente_clave)
        cls.periodo = getenv('TEST_PERIODO', datetime.now().strftime("%Y%m")).strip()

    # CASO 3: resumen de ventas y detalle de ventas con tipo "rcv"
    # En este caso el detalle de los documentos se trae por tipo
    def test_obtener_ventas_detalle_rcv(self):
        try:
            ventas_resumen = self.client.ventas_resumen(
                self.contribuyente_rut,
                self.periodo
            )
            if self.verbose:
                print(
                    'test_ventas_detalle_rcv(): ventas_resumen',
                    ventas_resumen
                )
            if ventas_resumen['data'] is not None:
                for resumen in ventas_resumen['data']:
                    if resumen['dcvTipoIngresoDoc'] != 'DET_ELE' or resumen['rsmnTotDoc'] == 0:
                        continue
                    ventas_detalle = self.client.ventas_detalle(
                        self.contribuyente_rut,
                        self.periodo,
                        resumen['rsmnTipoDocInteger']
                    )
                    if self.verbose:
                        print(
                            'test_ventas_detalle_rcv(): ventas_detalle',
                            ventas_detalle
                        )
                    break # sólo se obtiene un detalle para probar la API más rápido

                self.assertIsNotNone(ventas_detalle)
            else:
                print('test_ventas_detalle_rcv(): ventas_resumen: Libro ventas RCV vacío.')
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
