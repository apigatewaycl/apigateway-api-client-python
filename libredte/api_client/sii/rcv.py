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


class Rcv(LibreDTEApiBase):

    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super(Rcv, self).__init__(
            usuario_rut = usuario_rut,
            usuario_clave = usuario_clave,
            **kwargs
        )

    def compras_resumen(self, receptor, periodo, estado = 'REGISTRO'):
        """
        Args:
            estado (str): REGISTRO, PENDIENTE, NO_INCLUIR o RECLAMADO
        """
        body = {
            'auth': self.auth
        }
        r = self.client.post('/sii/rcv/compras/resumen/%(receptor)s/%(periodo)s/%(estado)s' % {
            'receptor': str(receptor),
            'periodo': str(periodo),
            'estado': str(estado),
        }, body)
        datos = r.json()
        return datos['data'] if 'data' in datos else datos

    def compras_detalle(self, receptor, periodo, dte = 0, estado = 'REGISTRO', tipo = None):
        """
        Args:
            estado (str): REGISTRO, PENDIENTE, NO_INCLUIR o RECLAMADO
        """
        if tipo is None:
            tipo = 'rcv_csv' if dte == 0 and estado == 'REGISTRO' else 'rcv'
        body = {
            'auth': self.auth
        }
        r = self.client.post('/sii/rcv/compras/detalle/%(receptor)s/%(periodo)s/%(dte)s/%(estado)s?tipo=%(tipo)s' % {
            'receptor': str(receptor),
            'periodo': str(periodo),
            'dte': str(dte),
            'estado': str(estado),
            'tipo': str(tipo),
        }, body)
        datos = r.json()
        return datos['data'] if 'data' in datos else datos

    def ventas_resumen(self, emisor, periodo):
        body = {
            'auth': self.auth
        }
        r = self.client.post('/sii/rcv/ventas/resumen/%(emisor)s/%(periodo)s' % {
            'emisor': str(emisor),
            'periodo': str(periodo),
        }, body)
        datos = r.json()
        return datos['data'] if 'data' in datos else datos

    def ventas_detalle(self, emisor, periodo, dte = 0, tipo = None):
        if tipo is None:
            tipo = 'rcv_csv' if dte == 0 else 'rcv'
        body = {
            'auth': self.auth
        }
        r = self.client.post('/sii/rcv/ventas/detalle/%(emisor)s/%(periodo)s/%(dte)s?tipo=%(tipo)s' % {
            'emisor': str(emisor),
            'periodo': str(periodo),
            'dte': str(dte),
            'tipo': str(tipo),
        }, body)
        datos = r.json()
        return datos['data'] if 'data' in datos else datos
