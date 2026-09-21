#
# API Gateway: Cliente de API en Python.
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

"""
Módulo para obtener indicadores desde el SII.

Para más información sobre la API, consulte la `documentación completa
de Indicadores
<https://developers.apigateway.cl/#65aa568c-4c5a-448b-9f3b-95c3d9153e4d>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class Uf(ApiBase):
    """
    Cliente para los valores de UF (Unidad de Fomento) de la API.

    Provee métodos para obtener valores de UF anuales, mensuales y
    diarios.
    """

    def anual(self, anio: int) -> Any:
        """
        Obtiene los valores de la UF para un año específico.

        :param int anio: Año para el cual se quieren los valores de UF.
        :return: Respuesta JSON con los valores de la UF del año.
        :rtype: dict
        """
        anio_str = str(anio)
        url = '/sii/indicadores/uf/anual/%(anio)s' % {'anio': anio_str}
        response = self.client.get(url)
        datos = response.json()
        return datos[anio_str] if anio_str in datos else {}

    def mensual(self, periodo: str) -> Any:
        """
        Obtiene los valores de la UF para un mes específico.

        Endpoint propio (`/uf/mensual/{periodo}`), no anidado bajo
        `/uf/anual/` — son recursos separados en la API real.

        :param str periodo: Período en formato AAAAMM (año y mes).
        :return: Respuesta JSON con los valores de la UF del mes.
        :rtype: dict
        """
        url = '/sii/indicadores/uf/mensual/%(periodo)s' % {'periodo': periodo}
        response = self.client.get(url)
        datos = response.json()
        return datos[periodo] if periodo in datos else {}

    def diario(self, dia: str) -> float:
        """
        Obtiene el valor de la UF para un día específico.

        Endpoint propio (`/uf/diario/{dia}`), no anidado bajo
        `/uf/anual/` — son recursos separados en la API real, y la
        respuesta es plana (el valor directo, sin anidar por mes/día).

        :param str dia: Fecha en formato AAAA-MM-DD o AAAAMMDD.
        :return: Valor de la UF para el día especificado.
        :rtype: float
        """
        url = '/sii/indicadores/uf/diario/%(dia)s' % {'dia': dia}
        response = self.client.get(url)
        datos = response.json()
        # La respuesta siempre normaliza la clave a AAAAMMDD (sin guiones),
        # sin importar el formato con el que se haya pedido `dia`.
        key = dia.replace('-', '')
        return float(datos[key]) if key in datos else 0.0
