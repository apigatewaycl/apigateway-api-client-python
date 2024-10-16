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
from apigatewaycl.api_client.sii.bte import BteEmitidas

class TestSiiBteEmitidas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', 0)))
        cls.contribuyente_rut = getenv('TEST_CONTRIBUYENTE_IDENTIFICADOR', '').strip()
        contribuyente_clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        cls.client = BteEmitidas(cls.contribuyente_rut, contribuyente_clave)
        cls.periodo = getenv('TEST_PERIODO', datetime.now().strftime("%Y%m")).strip()
        cls.receptor_rut = getenv('TEST_BTE_EMITIDAS_RECEPTOR_RUT', '').strip()

    # CASO 1: boletas del periodo
    def test_documentos(self):
        try:
            documentos = self.client.documentos(self.contribuyente_rut, self.periodo)
            if self.verbose:
                print('test_documentos(): documentos', documentos)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 2: boletas del periodo por mes
    def test_documentos_paginacion_periodo(self):
        try:
            pagina = 1
            while True:
                documentos = self.client.documentos(self.contribuyente_rut, self.periodo, pagina = pagina)
                print('test_documentos_paginacion_periodo(): Pagina %(pagina)s documentos %(documentos)s' % {
                        'pagina': pagina,
                        'documentos': documentos,
                })
                pagina += 1
                if pagina > documentos['n_paginas']:
                    break
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 2: bajar HTML de una boleta
    def test_html(self):
        try:
            documentos = self.client.documentos(self.contribuyente_rut, self.periodo)
            if len(documentos) == 0:
                print('test_html(): no probó funcionalidad.')
                return
            boleta_codigo = documentos[0]['codigo']
            html = self.client.html(boleta_codigo)
            filename = f'bte_emitidas_test_html_%(contribuyente_rut)s_%(periodo)s_%(boleta_codigo)s.html' % {
                'contribuyente_rut': self.contribuyente_rut, 'periodo': self.periodo, 'boleta_codigo': boleta_codigo
            }
            with open(filename, 'wb') as f:
                f.write(html)
            file_remove(filename) # se borra el archivo inmediatamente (sólo se crea como ejemplo)
            if self.verbose:
                print('test_html(): filename', filename)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 3: emitir boleta
    def test_emitir(self):
        if self.receptor_rut == '':
            print('test_emitir(): no probó funcionalidad.')
            return
        fecha_emision = getenv('TEST_BTE_EMITIDAS_FECHA_EMISION', datetime.now().strftime("%Y-%m-%d")).strip()
        datos_bte = {
            'Encabezado': {
                'IdDoc': {
                    'FchEmis': fecha_emision
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
            emitir = self.client.emitir(datos_bte)
            if self.verbose:
                print('test_emitir(): emitir', emitir)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 4: anular boleta
    def test_anular(self):
        boleta_numero = getenv('TEST_BTE_EMITIDAS_BOLETA_NUMERO', '').strip()
        if boleta_numero == '':
            print('test_anular(): no probó funcionalidad.')
            return
        try:
            anular = self.client.anular(self.contribuyente_rut, boleta_numero)
            if self.verbose:
                print('test_anular(): anular', anular)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})

    # CASO 5: tasa de receptor
    def test_receptor_tasa(self):
        if self.receptor_rut == '':
            print('test_receptor_tasa(): no probó funcionalidad.')
            return
        try:
            receptor_tasa = self.client.receptor_tasa(self.contribuyente_rut, self.receptor_rut)
            if self.verbose:
                    print('test_receptor_tasa(): receptor_tasa', receptor_tasa)
        except ApiException as e:
            self.fail("ApiException: %(e)s" % {'e': e})
