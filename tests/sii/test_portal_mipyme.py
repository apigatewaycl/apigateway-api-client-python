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

class TestSiiPortalMipymeContribuyentes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.identificador = getenv('TEST_USUARIO_IDENTIFICADOR', '').strip()
        clave = getenv('TEST_USUARIO_CLAVE', '').strip()
        cls.client = Contribuyentes(cls.identificador, clave)
        cls.contribuyente_rut = getenv('TEST_PORTAL_MIPYME_CONTRIBUYENTE_RUT', '').strip()

    # CASO 1: datos de un contribuyente
    def test_info(self):
        dte = getenv('TEST_PORTAL_MIPYME_DTE', '33').strip()
        try:
            info = self.client.info(self.identificador, self.contribuyente_rut, dte)
            if self.verbose:
                print('test_info(): info', info)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

class TestSiiPortalMipymeEmitidos(unittest.TestCase):

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
    def test_documentos(self):
        try:
            documentos = self.client.documentos(
                self.contribuyente_rut,
                {
                    'FEC_DESDE': self.fecha_desde,
                    'FEC_HASTA': self.fecha_hasta,
                }
            )
            if self.verbose:
                print('test_documentos(): documentos', documentos)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 3: bajar PDF de un DTE emitido
    def test_pdf(self):
        try:
            documentos = self.client.documentos(
                self.contribuyente_rut,
                {
                    'FEC_DESDE': self.fecha_desde,
                    'FEC_HASTA': self.fecha_hasta,
                }
            )
            if len(documentos) == 0:
                print('test_pdf(): no probó funcionalidad.')
                return
            dte = documentos[0]['dte']
            folio = documentos[0]['folio']
            pdf = self.client.pdf(self.contribuyente_rut, documentos[0]['codigo'])
            # usar el folio también funciona, pero es más lento porque se debe
            # buscar en el portal mipyme el código del DTE a partir del folio
            # pdf = self.client.pdf(self.contribuyente_rut, dte, folio)
            filename = 'mipyme_dte_emitido_test_pdf_%(contribuyente_rut)s_T%(dte)sF%(folio)s.pdf' % {
                'contribuyente_rut': self.contribuyente_rut, 'dte': dte, 'folio': folio
            }
            with open(filename, 'wb') as f:
                f.write(pdf)
            file_remove(filename) # se borra el archivo inmediatamente (sólo se crea como ejemplo)
            if self.verbose:
                print('test_pdf(): filename', filename)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 4: bajar XML de un DTE emitido (muy similar a caso de PDF)
    def test_xml(self):
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
            xml = self.client.xml(self.contribuyente_rut, documentos[0]['dte'], documentos[0]['folio'])
            filename = 'mipyme_dte_emitido_test_xml_%(contribuyente_rut)s_T%(dte)sF%(folio)s.xml' % {
                'contribuyente_rut': self.contribuyente_rut, 'dte': dte, 'folio': folio
            }
            with open(filename, 'w') as f:
                f.write(xml)
            file_remove(filename) # se borra el archivo inmediatamente (sólo se crea como ejemplo)
            if self.verbose:
                print('test_xml(): filename', filename)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

class TestSiiPortalMipymeRecibidos(unittest.TestCase):

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

    # CASO 5: documentos recibidos
    def test_documentos(self):
        try:
            documentos = self.client.documentos(
                self.contribuyente_rut,
                {
                    'FEC_DESDE': self.fecha_desde,
                    'FEC_HASTA': self.fecha_hasta,
                }
            )
            if self.verbose:
                print('test_documentos(): documentos', documentos)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 6: bajar PDF de un DTE recibido
    def test_pdf(self):
        try:
            documentos = self.client.documentos(
                self.contribuyente_rut,
                {
                    'FEC_DESDE': self.fecha_desde,
                    'FEC_HASTA': self.fecha_hasta,
                }
            )
            if len(documentos) == 0:
                print('test_pdf(): no probó funcionalidad.')
                return
            emisor = str(documentos[0]['rut']) + '-' + documentos[0]['dv']
            dte = documentos[0]['dte']
            folio = documentos[0]['folio']
            pdf = self.client.pdf(self.contribuyente_rut, emisor, documentos[0]['codigo'])
            # usar el folio también funciona, pero es más lento porque se debe
            # buscar en el portal mipyme el código del DTE a partir del folio
            # pdf = self.client.pdf(self.contribuyente_rut, emisor, dte, folio)
            filename = 'mipyme_dte_recibido_test_pdf_%(contribuyente_rut)s_%(emisor)s_T%(dte)sF%(folio)s.pdf' % {
                'contribuyente_rut': self.contribuyente_rut, 'emisor': emisor, 'dte': dte, 'folio': folio
            }
            with open(filename, 'wb') as f:
                f.write(pdf)
            file_remove(filename) # se borra el archivo inmediatamente (sólo se crea como ejemplo)
            if self.verbose:
                print('test_pdf(): filename', filename)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 7: bajar XML de un DTE recibido (muy similar a caso de PDF)
    def test_xml(self):
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
            filename = 'mipyme_dte_recibido_test_xml_(contribuyente_rut)s_%(emisor)s_T%(dte)sF%(folio)s.xml' % {
                'contribuyente_rut': self.contribuyente_rut, 'emisor': emisor, 'dte': dte, 'folio': folio
            }
            with open(filename, 'w') as f:
                f.write(xml)
            file_remove(filename) # se borra el archivo inmediatamente (sólo se crea como ejemplo)
            if self.verbose:
                print('test_xml(): filename', filename)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
