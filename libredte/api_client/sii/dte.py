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


class Contribuyentes(LibreDTEApiBase):

    def autorizacion(self, rut, certificacion = None):
        r = self.client.get('/sii/dte/contribuyentes/autorizado/%(rut)s?certificacion=%(certificacion)d' % {
            'rut': str(rut),
            'certificacion': 1 if certificacion is True else 0,
        })
        return r.json()

class Emitidos(LibreDTEApiBase):

    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super(Emitidos, self).__init__(
            usuario_rut = usuario_rut,
            usuario_clave = usuario_clave,
            **kwargs
        )

    def verificar(self, emisor, receptor, dte, folio, fecha, total, firma = None, certificacion = None):
        body = {
            'auth': self.get_auth_pass(),
            'dte': {
                'emisor': emisor,
                'receptor': receptor,
                'dte': dte,
                'folio': folio,
                'fecha': fecha,
                'total': total,
                'firma': firma
            }
        }
        r = self.client.post('/sii/dte/emitidos/verificar?certificacion=%(certificacion)d' % {
            'certificacion': 1 if certificacion is True else 0,
        }, body)
        return r.json()
