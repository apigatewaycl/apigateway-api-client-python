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


class BteEmitidas(LibreDTEApiBase):

    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super(BteEmitidas, self).__init__(
            usuario_rut = usuario_rut,
            usuario_clave = usuario_clave,
            **kwargs
        )

    def documentos(self, emisor, periodo):
        body = {
            'auth': self.get_auth_pass()
        }
        r = self.client.post('/sii/bte/emitidas/documentos/%(emisor)s/%(periodo)s' % {
            'emisor': str(emisor),
            'periodo': str(periodo),
        }, body)
        return r.json()

    def html(self, codigo):
        body = {
            'auth': self.get_auth_pass()
        }
        r = self.client.post('/sii/bte/emitidas/html/%(codigo)s' % {
            'codigo': str(codigo),
        }, body)
        return r.content
