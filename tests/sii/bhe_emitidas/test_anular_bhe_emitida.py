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
from apigatewaycl.api_client.sii.bhe import BheEmitidas

class TestAnularBheEmitida(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.identificador = getenv('TEST_USUARIO_IDENTIFICADOR', '').strip()
        clave = getenv('TEST_USUARIO_CLAVE', '').strip()
        cls.client = BheEmitidas(cls.identificador, clave)
        cls.periodo = getenv('TEST_PERIODO', datetime.now().strftime("%Y%m")).strip()
        cls.contribuyente_rut = getenv('TEST_USUARIO_RUT', '').strip()

    # CASO 7: anular
    def test_anular_bhe_emitida(self):
        try:
            documentos = self.client.documentos(
                self.contribuyente_rut, self.periodo
            )
            if len(documentos) == 0:
                print('test_anular(): no probó funcionalidad.')
                return
            boleta_numero = documentos[-1]['numero']
            anular = self.client.anular(
                self.contribuyente_rut,
                boleta_numero,
                BheEmitidas.ANULACION_CAUSA_ERROR_DIGITACION
            )

            self.assertIsNotNone(anular)

            if self.verbose:
                print('test_anular(): anular', anular)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
