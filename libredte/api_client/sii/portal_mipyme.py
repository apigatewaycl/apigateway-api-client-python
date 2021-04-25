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

from urllib.parse import urlencode

from ..base import LibreDTEApiBase


class PortalMipyme(LibreDTEApiBase):

    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super(PortalMipyme, self).__init__(
            usuario_rut = usuario_rut,
            usuario_clave = usuario_clave,
            **kwargs
        )

class Contribuyentes(PortalMipyme):

    def info(self, contribuyente, emisor, dte = 33):
        body = {
            'auth': self.auth
        }
        r = self.client.post('/sii/mipyme/contribuyentes/info/%(contribuyente)s/%(emisor)s/%(dte)s' % {
            'contribuyente': str(contribuyente),
            'emisor': str(emisor),
            'dte': str(dte),
        }, body)
        return r.json()

class Dte(PortalMipyme):

    ESTADO_EMITIDO = 'EMI' # Documento emitido
    ESTADO_BORRADOR = 'PRV' # Borrador (pre-view) de documento
    ESTADO_CERTIFICADO_RECHAZADO = 'DCD' # Certificado rechazado
    ESTADO_EMISOR_INVALIDO = 'DEI' # RUT emisor inválido
    ESTADO_FOLIO_INVALIDO = 'DFI' # Folio DTE inválido
    ESTADO_INCOMPLETO = 'DIN' # Incompleto
    ESTADO_FIRMA_SIN_PERMISO = 'DPF' # Sin permiso de firma
    ESTADO_FIRMA_RECHAZADA = 'DRF' # DTE rechazado por firma
    ESTADO_RECEPTOR_INVALIDO = 'DRI' # RUT receptor inválido
    ESTADO_REPETIDO = 'DRR' # Rechazado por repetido
    ESTADO_INICIALIZADO = 'INI' # DTE inicializado
    ESTADO_ACEPTADO = 'RAC' # DTE aceptado por receptor
    ESTADO_DISCREPANCIAS = 'RAD' # DTE aceptado con discrepancias
    ESTADO_NO_RECIBIDO = 'RNR' # DTE no recibido por receptor
    ESTADO_RECIBIDO = 'RRC' # DTE recibido por receptor
    ESTADO_ACEPTADO_LEY_19983 = 'RAL' # DTE aceptado Ley 19.983
    ESTADO_RECHAZADO_RECEPTOR = 'RRH' # DTE rechazado por receptor
    ESTADO_SIN_REPAROS = 'RSR' # Recibido sin reparos

    def get_codigo_dte(self, tipo):
        return self.DTE_TIPOS[tipo] if tipo in self.DTE_TIPOS else tipo.replace(' ', '-')

class DteEmitidos(Dte):

    def documentos(self, emisor, filtros = {}):
        body = {
            'auth': self.auth,
            'filtros': filtros
        }
        r = self.client.post('/sii/mipyme/emitidos/documentos/%(emisor)s' % {
            'emisor': str(emisor),
        }, body)
        return r.json()

    def pdf(self, emisor, dte, folio = None):
        body = {
            'auth': self.auth
        }
        if folio is not None:
            resource = '/sii/mipyme/emitidos/pdf/%(emisor)s/%(dte)s/%(folio)s' % {
                'emisor': str(emisor),
                'dte': str(dte),
                'folio': str(folio),
            }
        else:
            resource = '/sii/mipyme/emitidos/pdf/%(emisor)s/%(dte)s' % {
                'emisor': str(emisor),
                'dte': str(dte),
            }
        r = self.client.post(resource, body)
        return r.content

    def xml(self, emisor, dte, folio):
        body = {
            'auth': self.auth
        }
        r = self.client.post('/sii/mipyme/emitidos/xml/%(emisor)s/%(dte)s/%(folio)s' % {
            'emisor': str(emisor),
            'dte': str(dte),
            'folio': str(folio),
        }, body)
        return r.text

class DteRecibidos(Dte):

    def documentos(self, receptor, filtros = {}):
        body = {
            'auth': self.auth,
            'filtros': filtros
        }
        r = self.client.post('/sii/mipyme/recibidos/documentos/%(receptor)s' % {
            'receptor': str(receptor),
        }, body)
        return r.json()

    def pdf(self, receptor, emisor, dte, folio = None):
        body = {
            'auth': self.auth
        }
        if folio is not None:
            resource = '/sii/mipyme/recibidos/pdf/%(receptor)s/%(emisor)s/%(dte)s/%(folio)s' % {
                'receptor': str(receptor),
                'emisor': str(emisor),
                'dte': str(dte),
                'folio': str(folio),
            }
        else:
            resource = '/sii/mipyme/recibidos/pdf/%(receptor)s/%(emisor)s/%(dte)s' % {
                'receptor': str(receptor),
                'emisor': str(emisor),
                'dte': str(dte),
            }
        r = self.client.post(resource, body)
        return r.content

    def xml(self, receptor, emisor, dte, folio):
        body = {
            'auth': self.auth
        }
        r = self.client.post('/sii/mipyme/recibidos/xml/%(receptor)s/%(emisor)s/%(dte)s/%(folio)s' % {
            'receptor': str(receptor),
            'emisor': str(emisor),
            'dte': str(dte),
            'folio': str(folio),
        }, body)
        return r.text
