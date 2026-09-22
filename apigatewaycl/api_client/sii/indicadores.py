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
<https://www.apigateway.cl/docs>`_.
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
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, los valores de la UF del año, con el año como
            clave.
        :rtype: dict
        """
        url = '/sii/indicadores/uf/anual/%(anio)s' % {'anio': anio}
        response = self.client.get(url)
        return response.json()

    def mensual(self, periodo: str) -> Any:
        """
        Obtiene los valores de la UF para un mes específico.

        :param str periodo: Período en formato AAAAMM (año y mes).
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, los valores de la UF del mes, con el período
            (AAAAMM) como clave.
        :rtype: dict
        """
        url = '/sii/indicadores/uf/mensual/%(periodo)s' % {
            'periodo': periodo,
        }
        response = self.client.get(url)
        return response.json()

    def diario(self, dia: str) -> Any:
        """
        Obtiene el valor de la UF para un día específico.

        :param str dia: Fecha en formato AAAA-MM-DD o AAAAMMDD.
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, el valor de la UF del día, con la fecha
            normalizada a AAAAMMDD como clave. Para una fecha sin
            valor publicado la clave viene presente pero en `null`.
        :rtype: dict
        """
        url = '/sii/indicadores/uf/diario/%(dia)s' % {'dia': dia}
        response = self.client.get(url)
        return response.json()


class CorreccionMonetaria(ApiBase):
    """
    Cliente para los factores de corrección monetaria del SII.

    Recurso público — solo requiere el token de la plataforma, no
    credenciales de un contribuyente.
    """

    def anual(self, anio: int) -> Any:
        """
        Factores de corrección monetaria de un año.

        :param int anio: Año a consultar.
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, los factores del año, con el año como clave y un
            factor por cada mes (`'1'` a `'12'`).
        :rtype: dict
        """
        url = '/sii/indicadores/correccion_monetaria/anual/%(anio)s' % {
            'anio': anio,
        }
        response = self.client.get(url)
        return response.json()


class ImpuestoSegundaCategoria(ApiBase):
    """
    Cliente para el impuesto único de segunda categoría del SII.

    Recurso público — solo requiere el token de la plataforma, no
    credenciales de un contribuyente.
    """

    def anual(self, anio: int) -> Any:
        """
        Tramos del impuesto de segunda categoría de un año.

        :param int anio: Año a consultar.
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, los tramos del año, con el año como clave. Cada
            tramo trae `desde`, `hasta`, `tasa`, `rebaja` y `maximo`.
        :rtype: dict
        """
        url = '/sii/indicadores/impuesto_segunda_categoria/anual/%(anio)s' % {
            'anio': anio
        }
        response = self.client.get(url)
        return response.json()

    def mensual(self, periodo: str) -> Any:
        """
        Tramos del impuesto de segunda categoría de un mes.

        :param str periodo: Período en formato AAAAMM (año y mes).
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, los tramos del período, con el período (AAAAMM)
            como clave. Cada tramo trae `desde`, `hasta`, `tasa`,
            `rebaja` y `maximo`.
        :rtype: dict
        """
        url = (
            '/sii/indicadores/impuesto_segunda_categoria/mensual/%(periodo)s'
            % {'periodo': periodo}
        )
        response = self.client.get(url)
        return response.json()
