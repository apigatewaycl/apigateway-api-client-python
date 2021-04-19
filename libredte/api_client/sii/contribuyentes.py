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

    def situacion_tributaria(self, rut):
        r = self.client.get('/sii/contribuyentes/situacion_tributaria/tercero/%(rut)s' % {
            'rut': str(rut),
        })
        return r.json()

    def verificar_rut(self, serie):
        r = self.client.get('/sii/contribuyentes/rut/verificar/%(serie)s' % {
            'serie': str(serie),
        })
        return r.json()
