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


class Uf(LibreDTEApiBase):

    def anual(self, anio):
        anio = str(anio)
        r = self.client.get('/sii/indicadores/uf/anual/%(anio)s' % {
            'anio': anio,
        })
        datos = r.json()
        return datos[anio] if anio in datos else {}

    def mensual(self, periodo):
        periodo = str(periodo)
        anio = periodo[0:4]
        mes = periodo[4:6]
        r = self.client.get('/sii/indicadores/uf/anual/%(anio)s/%(mes)s' % {
            'anio': str(anio),
            'mes': str(mes),
        })
        datos = r.json()
        return datos[periodo] if periodo in datos else {}

    def diario(self, dia):
        anio, mes, dia = str(dia).split('-')
        r = self.client.get('/sii/indicadores/uf/anual/%(anio)s/%(mes)s/%(dia)s' % {
            'anio': str(anio),
            'mes': str(mes),
            'dia': str(dia),
        })
        datos = r.json()
        key = str(anio) + str(mes) + str(dia)
        return float(datos[key]) if key in datos else 0
