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

class TestSiiRcv(unittest.TestCase):

    estados = ['REGISTRO', 'PENDIENTE', 'NO_INCLUIR', 'RECLAMADO']

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('TEST_CONTRIBUYENTE_IDENTIFICADOR', '').strip()
        contribuyente_clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        cls.client = Rcv(cls.contribuyente_rut, contribuyente_clave)
        cls.periodo = getenv('TEST_PERIODO', datetime.now().strftime("%Y%m")).strip()

    # CASO 1: resumen de compras y detalle de compras con tipo "rcv"
    # En este caso el detalle de los documentos se trae por tipo
    def test_compras_detalle_rcv(self):
        try:
            for estado in self.estados:
                compras_resumen = self.client.compras_resumen(
                    self.contribuyente_rut,
                    self.periodo,
                    estado
                )
                if self.verbose:
                    print('test_compras_detalle_rcv(): compras_resumen', compras_resumen)
                if compras_resumen['data'] is not None:
                    for resumen in compras_resumen['data']:
                        if resumen['dcvTipoIngresoDoc'] != 'DET_ELE' or resumen['rsmnTotDoc'] == 0:
                            continue
                        compras_detalle = self.client.compras_detalle(
                            self.contribuyente_rut,
                            self.periodo,
                            resumen['rsmnTipoDocInteger'],
                            estado
                        )
                        if self.verbose:
                            print('test_compras_detalle_rcv(): compras_detalle', compras_detalle)
                        break # sólo se obtiene un detalle para probar la API más rápido
                else:
                    print('test_compras_detalle_rcv(): compras_resumen: Libro compras RCV vacío.')
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 2: detalle de compras con tipo "rcv_csv"
    # En este caso se trae el detalle de los documentos en una llamada
    def test_compras_detalle_rcv_csv(self):
        try:
            compras_detalle = self.client.compras_detalle(
                self.contribuyente_rut,
                self.periodo
            )
            if self.verbose:
                print('test_compras_detalle_rcv_csv(): compras_detalle', compras_detalle)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 3: resumen de ventas y detalle de ventas con tipo "rcv"
    # En este caso el detalle de los documentos se trae por tipo
    def test_ventas_detalle_rcv(self):
        try:
            ventas_resumen = self.client.ventas_resumen(
                self.contribuyente_rut,
                self.periodo
            )
            if self.verbose:
                print('test_ventas_detalle_rcv(): ventas_resumen', ventas_resumen)
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
                        print('test_ventas_detalle_rcv(): ventas_detalle', ventas_detalle)
                    break # sólo se obtiene un detalle para probar la API más rápido
            else:
                print('test_ventas_detalle_rcv(): ventas_resumen: Libro ventas RCV vacío.')
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 4: detalle de ventas con tipo "rcv_csv"
    # En este caso se trae el detalle de los documentos en una llamada
    def test_ventas_detalle_rcv_csv(self):
        try:
            ventas_detalle = self.client.ventas_detalle(
                self.contribuyente_rut,
                self.periodo
            )
            if self.verbose:
                print('test_ventas_detalle_rcv_csv(): ventas_detalle', ventas_detalle)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
