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
import os
from os import getenv, remove as file_remove
from datetime import datetime
from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.bte import BteEmitidas

class TestDescargarHtmlBteEmitida(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('TEST_CONTRIBUYENTE_IDENTIFICADOR', '').strip()
        contribuyente_clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        cls.client = BteEmitidas(cls.contribuyente_rut, contribuyente_clave)
        cls.periodo = getenv('TEST_PERIODO', datetime.now().strftime("%Y%m")).strip()
        cls.receptor_rut = getenv('TEST_BTE_EMITIDAS_RECEPTOR_RUT', '').strip()

    # CASO 2: bajar HTML de una boleta
    def test_descargar_html_bte_emitida(self):
        try:
            documentos = self.client.documentos(
                self.contribuyente_rut, self.periodo
            )
            if len(documentos) == 0:
                print('test_html(): no probó funcionalidad.')
                return
            boleta_codigo = documentos[0]['codigo']
            html = self.client.html(boleta_codigo)

            # Retrocede dos niveles para salir de 'dte_facturacion' y entrar en 'tests'
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

            # Define la carpeta de destino correcta
            output_dir = os.path.join(base_dir, 'archivos', 'sii', 'bte_emitidas_html')

            # Crear la carpeta si no existe
            os.makedirs(output_dir, exist_ok=True)

            filename = os.path.join(
                output_dir,
                'APIGATEWAY_BTE_EMITIDA_%(contribuyente_rut)s_%(periodo)s_%(boleta_codigo)s.html' % {
                    'contribuyente_rut': self.contribuyente_rut,
                    'periodo': self.periodo,
                    'boleta_codigo': boleta_codigo
                }
            )

            with open(filename, 'wb') as f:
                f.write(html)

            self.assertIsNotNone(boleta_codigo)

            if self.verbose:
                print('test_html(): filename', filename)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
