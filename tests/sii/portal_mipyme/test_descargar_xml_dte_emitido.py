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
from apigatewaycl.api_client.sii.portal_mipyme import Contribuyentes, DteEmitidos, DteRecibidos

class TestDescargarXmlDteEmitido(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.identificador = getenv('TEST_USUARIO_IDENTIFICADOR', '').strip()
        clave = getenv('TEST_USUARIO_CLAVE', '').strip()
        cls.client = DteEmitidos(cls.identificador, clave)
        cls.contribuyente_rut = getenv('TEST_PORTAL_MIPYME_CONTRIBUYENTE_RUT', '').strip()
        anio = getenv('TEST_ANIO', datetime.now().strftime("%Y")).strip()
        cls.fecha_desde = f'{anio}-01-01'
        cls.fecha_hasta = f'{anio}-01-31'

    # CASO 4: bajar XML de un DTE emitido (muy similar a caso de PDF)
    def test_descargar_xml_dte_emitido(self):
        try:
            documentos = self.client.documentos(
                self.contribuyente_rut,
                {
                    'FEC_DESDE': self.fecha_desde,
                    'FEC_HASTA': self.fecha_hasta,
                }
            )
            if len(documentos) == 0:
                print('test_xml(): no probó funcionalidad.')
                return
            dte = documentos[0]['dte']
            folio = documentos[0]['folio']
            xml = self.client.xml(
                self.contribuyente_rut,
                documentos[0]['dte'],
                documentos[0]['folio']
            )

            # Retrocede dos niveles para salir de 'dte_facturacion' y entrar en 'tests'
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

            # Define la carpeta de destino correcta
            output_dir = os.path.join(base_dir, 'archivos', 'sii', 'mipyme_dte_emitido_xml')

            # Crear la carpeta si no existe
            os.makedirs(output_dir, exist_ok=True)

            filename = os.path.join(
                output_dir,
                'MIPYME_DTE_EMITIDO_%(contribuyente_rut)s_T%(dte)sF%(folio)s.xml' % {
                    'contribuyente_rut': self.contribuyente_rut,
                    'dte': dte,
                    'folio': folio
                }
            )

            with open(filename, 'wb') as f:
                f.write(xml)

            self.assertIsNotNone(folio)

            if self.verbose:
                print('test_xml(): filename', filename)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
