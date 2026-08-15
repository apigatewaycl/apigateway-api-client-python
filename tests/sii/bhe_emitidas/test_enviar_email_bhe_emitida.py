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

class TestEnviarEmailBheEmitida(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.identificador = getenv('TEST_USUARIO_IDENTIFICADOR', '').strip()
        clave = getenv('TEST_USUARIO_CLAVE', '').strip()
        cls.client = BheEmitidas(cls.identificador, clave)
        cls.periodo = getenv('TEST_PERIODO', datetime.now().strftime("%Y%m")).strip()
        cls.contribuyente_rut = getenv('TEST_USUARIO_RUT', '').strip()

    # CASO 6: enviar por email
    def test_enviar_email_bhe_emitida(self):
        try:
            receptor_email = getenv('TEST_BHE_EMITIDAS_RECEPTOR_EMAIL', '').strip()
            documentos = self.client.documentos(
                self.contribuyente_rut, self.periodo
            )
            if len(documentos) == 0:
                print('test_email(): no probó funcionalidad.')
                return
            boleta_codigo = documentos[0]['codigo']

            email = self.client.email(boleta_codigo, receptor_email)

            self.assertIsNotNone(email)

            if self.verbose:
                print('test_email(): email', email)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
