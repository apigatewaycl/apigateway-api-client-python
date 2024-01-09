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
from apigatewaycl.api_client.sii.bhe import BheRecibidas

class TestSiiBheRecibidasPaginadas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('TEST_CONTRIBUYENTE_RUT', '').strip()
        contribuyente_clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        cls.client = BheRecibidas(cls.contribuyente_rut, contribuyente_clave)
        cls.periodo = getenv('TEST_PERIODO', datetime.now().strftime("%Y%m")).strip()

    # CASO 1: boletas del periodo paginadas
    def test_documentos(self):
        try:
            documentos = self._get_documentos()
            if self.verbose:
                print('test_documentos(): documentos', documentos)
                print('test_documentos(): len(documentos)', len(documentos))
        except ApiException as e:
            self.fail(f"ApiException: {e}")

    # Método privado que obtiene las boletas paginadas del CASO 1
    def _get_documentos(self):
        documentos = []
        pagina = 1
        pagina_sig_codigo = None
        while True:
            documentos_pagina = self.client.documentos(
                self.contribuyente_rut,
                self.periodo,
                pagina,
                pagina_sig_codigo
            )
            if documentos_pagina['pagina_sig_codigo'] == '00000000000000':
                break
            pagina_sig_codigo = documentos_pagina['pagina_sig_codigo']
            documentos = documentos + documentos_pagina['boletas']
            pagina += 1
        return documentos
