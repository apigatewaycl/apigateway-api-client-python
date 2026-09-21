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

import requests

from .. import ApiBase


class Uf(ApiBase):
    """
    Cliente para los valores de UF (Unidad de Fomento) de la API.

    Provee métodos para obtener valores de UF anuales, mensuales y
    diarios.
    """

    @staticmethod
    def _datos(response: requests.Response) -> dict[str, Any]:
        """
        Cuerpo de la respuesta como diccionario.

        Cuando no hay datos para el recurso pedido, v1 responde 200 con
        el cuerpo vacío, que no es JSON válido. Se trata como si no
        hubiera datos en vez de propagar el error de decodificación.

        :param requests.Response response: Respuesta de la API.
        :return: Cuerpo decodificado, o un diccionario vacío.
        :rtype: dict
        """
        try:
            datos = response.json()
        except ValueError:
            return {}
        return datos if isinstance(datos, dict) else {}

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
        return self._datos(response).get(anio_str) or {}

    def mensual(self, periodo: str) -> Any:
        """
        Obtiene los valores de la UF para un mes específico.

        En v2 es un recurso propio (`/uf/mensual/{periodo}`). En v1 no
        existe: el mes está anidado bajo `/uf/anual/{anio}/{mes}`. La
        respuesta es equivalente en ambas, con el período (AAAAMM) como
        clave.

        :param str periodo: Período en formato AAAAMM (año y mes).
        :return: Respuesta JSON con los valores de la UF del mes.
        :rtype: dict
        """
        if self.client.version == 'v1':
            url = '/sii/indicadores/uf/anual/%(anio)s/%(mes)s' % {
                'anio': periodo[:4],
                'mes': periodo[4:6],
            }
        else:
            url = '/sii/indicadores/uf/mensual/%(periodo)s' % {
                'periodo': periodo,
            }
        response = self.client.get(url)
        return self._datos(response).get(periodo) or {}

    def diario(self, dia: str) -> float:
        """
        Obtiene el valor de la UF para un día específico.

        En v2 es un recurso propio (`/uf/diario/{dia}`) y la respuesta
        es plana (el valor directo). En v1 no existe: el día está
        anidado bajo `/uf/anual/{anio}/{mes}/{dia}`, pero la respuesta
        es equivalente.

        :param str dia: Fecha en formato AAAA-MM-DD o AAAAMMDD.
        :return: Valor de la UF para el día especificado.
        :rtype: float
        """
        # La respuesta siempre normaliza la clave a AAAAMMDD (sin
        # guiones), sin importar el formato con el que se pidió `dia`.
        key = dia.replace('-', '')
        if self.client.version == 'v1':
            url = '/sii/indicadores/uf/anual/%(anio)s/%(mes)s/%(dia)s' % {
                'anio': key[:4],
                'mes': key[4:6],
                'dia': key[6:8],
            }
        else:
            url = '/sii/indicadores/uf/diario/%(dia)s' % {'dia': dia}
        response = self.client.get(url)
        # Para una fecha sin valor publicado la API responde con la
        # clave presente pero en `null`, así que no basta con mirar si
        # la clave existe.
        valor = self._datos(response).get(key)
        return float(valor) if valor is not None else 0.0
