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
from apigatewaycl.api_client.sii.bhe import BheEmitidas

class TestEmitirBhe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.identificador = getenv('TEST_USUARIO_IDENTIFICADOR', '').strip()
        clave = getenv('TEST_USUARIO_CLAVE', '').strip()
        cls.client = BheEmitidas(cls.identificador, clave)
        cls.receptor_rut = getenv('TEST_BHE_EMITIDAS_RECEPTOR_RUT', '').strip()
        cls.contribuyente_rut = getenv('TEST_USUARIO_RUT', '').strip()

    # CASO 5: emitir una boleta
    def test_emitir_bhe(self):
        if self.receptor_rut == '':
            print('test_emitir(): no probó funcionalidad.')
            return
        fecha_emision = datetime.now().strftime("%Y-%m-%d")
        datos_bhe = {
            'Encabezado': {
                'IdDoc': {
                    'FchEmis': fecha_emision,
                    'TipoRetencion': BheEmitidas.RETENCION_EMISOR
                },
                'Emisor': {
                    'RUTEmisor': self.contribuyente_rut
                },
                'Receptor': {
                    'RUTRecep': self.receptor_rut,
                    'RznSocRecep': 'Receptor generico',
                    'DirRecep': 'Santa Cruz',
                    'CmnaRecep': 'Santa Cruz'
                }
            },
            'Detalle': [
                {
                    'NmbItem': 'Prueba integracion API Gateway 1',
                    'MontoItem': 50
                },
                {
                    'NmbItem': 'Prueba integracion API Gateway 2',
                    'MontoItem': 100
                }
            ]
        }
        try:
            emitir = self.client.emitir(datos_bhe)

            self.assertIsNotNone(emitir)

            if self.verbose:
                print('test_emitir(): emitir', emitir)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
