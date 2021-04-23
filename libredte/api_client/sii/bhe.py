# -*- coding: utf-8 -*-

"""
LibreDTE API Client
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
<http://www.gnu.org/licenses/lgpl.html>.
"""

from ..base import LibreDTEApiBase


class BheEmitidas(LibreDTEApiBase):

    # quien debe hacer la retención asociada al honorario para pagar al SII
    RETENCION_RECEPTOR = 1
    RETENCION_EMISOR = 2

    # posibles motivos de anulación de una BHE
    ANULACION_CAUSA_SIN_PAGO = 1
    ANULACION_CAUSA_SIN_PRESTACION = 2
    ANULACION_CAUSA_ERROR_DIGITACION = 3

    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super(BheEmitidas, self).__init__(
            usuario_rut = usuario_rut,
            usuario_clave = usuario_clave,
            **kwargs
        )

    def documentos(self, emisor, periodo):
        body = {
            'auth': self.get_auth_pass()
        }
        r = self.client.post('/sii/bhe/emitidas/documentos/%(emisor)s/%(periodo)s' % {
            'emisor': str(emisor),
            'periodo': str(periodo),
        }, body)
        return r.json()

    def emitir(self, boleta):
        body = {
            'auth': self.get_auth_pass(),
            'boleta': boleta
        }
        r = self.client.post('/sii/bhe/emitidas/emitir', body)
        return r.json()

    def pdf(self, codigo):
        body = {
            'auth': self.get_auth_pass()
        }
        r = self.client.post('/sii/bhe/emitidas/pdf/%(codigo)s' % {
            'codigo': str(codigo)
        }, body)
        return r.content

    def email(self, codigo, email):
        body = {
            'auth': self.get_auth_pass(),
            'destinatario': {
                'email': email
            }
        }
        r = self.client.post('/sii/bhe/emitidas/email/%(codigo)s' % {
            'codigo': str(codigo)
        }, body)
        return r.json()

    def anular(self, emisor, folio, causa = ANULACION_CAUSA_ERROR_DIGITACION):
        body = {
            'auth': self.get_auth_pass()
        }
        r = self.client.post('/sii/bhe/emitidas/anular/%(emisor)s/%(folio)s?causa=%(causa)s' % {
            'emisor': str(emisor),
            'folio': str(folio),
            'causa': str(causa),
        }, body)
        return r.json()

class BheRecibidas(LibreDTEApiBase):

    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super(BheRecibidas, self).__init__(
            usuario_rut = usuario_rut,
            usuario_clave = usuario_clave,
            **kwargs
        )

    def documentos(self, receptor, periodo):
        body = {
            'auth': self.get_auth_pass()
        }
        r = self.client.post('/sii/bhe/recibidas/documentos/%(receptor)s/%(periodo)s' % {
            'receptor': str(receptor),
            'periodo': str(periodo),
        }, body)
        return r.json()

    def pdf(self, codigo):
        body = {
            'auth': self.get_auth_pass()
        }
        r = self.client.post('/sii/bhe/recibidas/pdf/%(codigo)s' % {
            'codigo': str(codigo),
        }, body)
        return r.content

    def observar(self, emisor, numero, causa = 1):
        body = {
            'auth': self.get_auth_pass()
        }
        r = self.client.post('/sii/bhe/recibidas/observar/%(emisor)s/%(numero)s?causa=%(causa)s' % {
            'emisor': str(emisor),
            'numero': str(numero),
            'causa': str(causa),
        }, body)
        return r.json()
