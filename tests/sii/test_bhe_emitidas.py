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

class TestSiiBheEmitidas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.identificador = getenv('TEST_USUARIO_IDENTIFICADOR', '').strip()
        clave = getenv('TEST_USUARIO_CLAVE', '').strip()
        cls.client = BheEmitidas(cls.identificador, clave)
        cls.periodo = getenv('TEST_PERIODO', datetime.now().strftime("%Y%m")).strip()
        cls.receptor_rut = getenv('TEST_BHE_EMITIDAS_RECEPTOR_RUT', '').strip()
        cls.contribuyente_rut = getenv('TEST_USUARIO_RUT', '').strip()

    # CASO 1: boletas del periodo
    def test_documentos(self):
        try:
            documentos = self.client.documentos(self.contribuyente_rut, self.periodo)
            if self.verbose:
                print('test_documentos(): documentos', documentos)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 2: bajar PDF de una boleta
    def test_pdf(self):
        try:
            documentos = self.client.documentos(self.contribuyente_rut, self.periodo)
            if len(documentos) == 0:
                print('test_pdf(): no probó funcionalidad.')
                return
            boleta_codigo = documentos[0]['codigo']
            html = self.client.pdf(boleta_codigo)
            filename = 'bhe_emitidas_test_pdf_%(contribuyente_rut)s_%(periodo)ss_%(boleta_codigo)s.pdf' % {
                'contribuyente_rut': self.contribuyente_rut, 'periodo': self.periodo, 'boleta_codigo': boleta_codigo
            }
            with open(filename, 'wb') as f:
                f.write(html)
            file_remove(filename) # se borra el archivo inmediatamente (sólo se crea como ejemplo)
            if self.verbose:
                print('test_pdf(): filename', filename)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 3: emitir una boleta
    def test_emitir(self):
        if self.receptor_rut == '':
            print('test_emitir(): no probó funcionalidad.')
            return
        fecha_emision = getenv('TEST_BHE_EMITIDAS_FECHA_EMISION', datetime.now().strftime("%Y-%m-%d")).strip()
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
            if self.verbose:
                print('test_emitir(): emitir', emitir)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 4: enviar por email
    def test_email(self):
        boleta_codigo = getenv('TEST_BHE_EMITIDAS_BOLETA_CODIGO', '').strip()
        receptor_email = getenv('TEST_BHE_EMITIDAS_RECEPTOR_EMAIL', '').strip()
        if boleta_codigo == '' or receptor_email == '':
            print('test_email(): no probó funcionalidad.')
            return
        try:
            email = self.client.email(boleta_codigo, receptor_email)
            if self.verbose:
                print('test_email(): email', email)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 5: anular
    def test_anular(self):
        boleta_numero = getenv('TEST_BHE_EMITIDAS_BOLETA_NUMERO', '').strip()
        if boleta_numero == '':
            print('test_anular(): no probó funcionalidad.')
            return
        try:
            anular = self.client.anular(
                self.contribuyente_rut,
                boleta_numero,
                BheEmitidas.ANULACION_CAUSA_ERROR_DIGITACION
            )
            if self.verbose:
                print('test_anular(): anular', anular)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
