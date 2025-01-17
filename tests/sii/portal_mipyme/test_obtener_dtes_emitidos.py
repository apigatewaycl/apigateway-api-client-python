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
from os import getenv, remove as file_remove
from datetime import datetime
from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.portal_mipyme import Contribuyentes, DteEmitidos, DteRecibidos

class TestObtenerDtesEmitidos(unittest.TestCase):

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

    # CASO 2: documentos emitidos
    def test_obtener_dtes_emitidos(self):
        try:
            documentos = self.client.documentos(
                self.contribuyente_rut,
                {
                    'FEC_DESDE': self.fecha_desde,
                    'FEC_HASTA': self.fecha_hasta,
                }
            )

            self.assertTrue(True)

            if self.verbose:
                print('test_documentos(): documentos', documentos)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
