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
from apigatewaycl.api_client.sii.bhe import BheRecibidas

class TestSiiBheRecibidas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('TEST_CONTRIBUYENTE_RUT', '').strip()
        contribuyente_clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        cls.client = BheRecibidas(cls.contribuyente_rut, contribuyente_clave)
        cls.periodo = getenv('TEST_PERIODO', datetime.now().strftime("%Y%m")).strip()

    # CASO 1: boletas del periodo
    def test_documentos(self):
        try:
            documentos = self.client.documentos(self.contribuyente_rut, self.periodo)
            if self.verbose:
                print('test_documentos(): documentos', documentos)
        except ApiException as e:
            self.fail(f"ApiException: {e}")

    # CASO 2: bajar PDF de una boleta
    def test_pdf(self):
        try:
            documentos = self.client.documentos(self.contribuyente_rut, self.periodo)
            if len(documentos) == 0:
                print('test_pdf(): no probó funcionalidad.')
                return
            boleta_codigo = documentos[0]['codigo']
            pdf = self.client.pdf(boleta_codigo)
            filename = f'bhe_recibidas_test_pdf_{self.contribuyente_rut}_{self.periodo}_{boleta_codigo}.pdf'
            with open(filename, 'wb') as f:
                f.write(pdf)
            file_remove(filename) # se borra el archivo inmediatamente (sólo se crea como ejemplo)
            if self.verbose:
                print('test_pdf(): filename', filename)
        except ApiException as e:
            self.fail(f"ApiException: {e}")

    # CASO 3: observar una boleta
    def test_observar(self):
        observar_emisor_rut = getenv('TEST_BHE_RECIBIDAS_OBSERVAR_EMISOR_RUT', '').strip()
        observar_numero = getenv('TEST_BHE_RECIBIDAS_OBSERVAR_NUMERO', '').strip()
        if observar_emisor_rut == '' or observar_numero == '':
            print('test_observar(): no probó funcionalidad.')
            return
        observar = self.client.observar(observar_emisor_rut, observar_numero)
        if self.verbose:
            print('test_observar(): observar', observar)
