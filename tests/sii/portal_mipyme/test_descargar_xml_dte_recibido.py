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

class TestDescargarXmlDteRecibido(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.identificador = getenv('TEST_USUARIO_IDENTIFICADOR', '').strip()
        clave = getenv('TEST_USUARIO_CLAVE', '').strip()
        cls.client = DteRecibidos(cls.identificador, clave)
        cls.contribuyente_rut = getenv('TEST_PORTAL_MIPYME_CONTRIBUYENTE_RUT', '').strip()
        anio = getenv('TEST_ANIO', datetime.now().strftime("%Y")).strip()
        cls.fecha_desde = '%(anio)s-01-01' % {'anio', anio}
        cls.fecha_hasta = '%(anio)s-01-31' % {'anio', anio}

    # CASO 7: bajar XML de un DTE recibido (muy similar a caso de PDF)
    def test_descargar_xml_dte_recibido(self):
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
            emisor = str(documentos[0]['rut']) + '-' + documentos[0]['dv']
            dte = documentos[0]['dte']
            folio = documentos[0]['folio']
            xml = self.client.xml(self.contribuyente_rut, emisor, dte, folio)

            # Retrocede dos niveles para salir de 'dte_facturacion' y entrar en 'tests'
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

            # Define la carpeta de destino correcta
            output_dir = os.path.join(base_dir, 'archivos', 'sii', 'mipyme_dte_recibido_xml')

            # Crear la carpeta si no existe
            os.makedirs(output_dir, exist_ok=True)

            filename = os.path.join(
                output_dir,
                'MIPYME_DTE_RECIBIDO_%(contribuyente_rut)s_%(emisor)s_T%(dte)sF%(folio)s.xml' % {
                    'contribuyente_rut': self.contribuyente_rut,
                    'emisor': emisor,
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
