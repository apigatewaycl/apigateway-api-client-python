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

class TestListarBheEmitidasPaginadasDia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.identificador = getenv('TEST_USUARIO_IDENTIFICADOR', '').strip()
        clave = getenv('TEST_USUARIO_CLAVE', '').strip()
        cls.client = BheEmitidas(cls.identificador, clave)
        cls.periodo = getenv('TEST_PERIODO', datetime.now().strftime("%Y%m")).strip()
        cls.contribuyente_rut = getenv('TEST_USUARIO_RUT', '').strip()

    # CASO 3: boletas del periodo por dia
    def test_listar_bhe_emitidas_paginadas_dia(self):
        try:
            pagina = 1
            pagina_sig_codigo = None
            while True:
                documentos = self.client.documentos(
                    self.contribuyente_rut,
                    self.periodo,
                    pagina = pagina,
                    pagina_sig_codigo = pagina_sig_codigo
                )
                print('test_documentos_paginacion_periodo_mes(): Pagina %(pagina)s documentos %(documentos)s' % {
                    'pagina': pagina,
                    'documentos': documentos,
                })
                pagina_sig_codigo = documentos['pagina_sig_codigo']
                pagina += 1
                if pagina > documentos['n_paginas']:
                    break

            self.assertTrue(True)

        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
