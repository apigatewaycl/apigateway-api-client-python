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

from .. import ApiBase, ApiResponse


class Uf(ApiBase):
    """
    Cliente para los valores de UF (Unidad de Fomento) de la API.

    Provee métodos para obtener valores de UF anuales, mensuales y
    diarios.
    """

    def anual(self, anio: int) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene los valores de la UF para un año específico.

        Respuesta (ejemplo)::

            {
              "data": {
                "2026": {
                  "1": {
                    "1": 39731.79,
                    "2": 39735.63,
                    "3": 39739.47,
                    "4": 39743.31,
                    "5": 39747.15,
                    "...": "..."
                  },
                  "2": {
                    "1": 39703.5,
                    "2": 39700.94,
                    "3": 39698.37,
                    "4": 39695.81,
                    "5": 39693.25,
                    "...": "..."
                  },
                  "3": {
                    "1": 39796.31,
                    "2": 39801.98,
                    "3": 39807.65,
                    "4": 39813.33,
                    "5": 39819.01,
                    "...": "..."
                  }
                }
              },
              "metadata": {"timestamp": "..."}
            }

        :param int anio: Año para el cual se quieren los valores de UF.
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, los valores de la UF del año, con el año como
            clave.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/indicadores/uf/anual/%(anio)s' % {'anio': anio}
        response = self.client.get(url)
        return self._json(response)

    def mensual(self, periodo: str) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene los valores de la UF para un mes específico.

        Respuesta (ejemplo)::

            {
              "data": {
                "202603": {
                  "1": 39796.31,
                  "2": 39801.98,
                  "3": 39807.65,
                  "4": 39813.33,
                  "5": 39819.01,
                  "6": 39824.68,
                  "7": 39830.36,
                  "8": 39836.04,
                  "...": "..."
                }
              },
              "metadata": {"timestamp": "..."}
            }

        :param str periodo: Período en formato AAAAMM (año y mes).
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, los valores de la UF del mes, con el período
            (AAAAMM) como clave.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/indicadores/uf/mensual/%(periodo)s' % {
            'periodo': periodo,
        }
        response = self.client.get(url)
        return self._json(response)

    def diario(self, dia: str) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene el valor de la UF para un día específico.

        Respuesta (ejemplo)::

            {"data": {"20241015": 37987.65}, "metadata": {"timestamp": "..."}}

        :param str dia: Fecha en formato AAAA-MM-DD o AAAAMMDD.
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, el valor de la UF del día, con la fecha
            normalizada a AAAAMMDD como clave. Para una fecha sin
            valor publicado la clave viene presente pero en `null`.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/indicadores/uf/diario/%(dia)s' % {'dia': dia}
        response = self.client.get(url)
        return self._json(response)


class CorreccionMonetaria(ApiBase):
    """
    Cliente para los factores de corrección monetaria del SII.

    Recurso público — solo requiere el token de la plataforma, no
    credenciales de un contribuyente.
    """

    def anual(self, anio: int) -> ApiResponse[dict[str, Any]]:
        """
        Factores de corrección monetaria de un año.

        Respuesta (ejemplo)::

            {
              "data": {
                "2024": [
                  {
                    "1": 0.2,
                    "2": 0.5,
                    "3": 0.8,
                    "4": 1.0,
                    "5": 1.2,
                    "...": "..."
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param int anio: Año a consultar.
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, los factores del año, con el año como clave y un
            factor por cada mes (`'1'` a `'12'`).
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/indicadores/correccion_monetaria/anual/%(anio)s' % {
            'anio': anio,
        }
        response = self.client.get(url)
        return self._json(response)


class ImpuestoSegundaCategoria(ApiBase):
    """
    Cliente para el impuesto único de segunda categoría del SII.

    Recurso público — solo requiere el token de la plataforma, no
    credenciales de un contribuyente.
    """

    def anual(self, anio: int) -> ApiResponse[dict[str, Any]]:
        """
        Tramos del impuesto de segunda categoría de un año.

        Respuesta (ejemplo)::

            {
              "data": {
                "2024": [
                  {
                    "desde": 0,
                    "hasta": 866310,
                    "tasa": 0,
                    "rebaja": 0,
                    "maximo": null
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param int anio: Año a consultar.
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, los tramos del año, con el año como clave. Cada
            tramo trae `desde`, `hasta`, `tasa`, `rebaja` y `maximo`.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/indicadores/impuesto_segunda_categoria/anual/%(anio)s' % {
            'anio': anio
        }
        response = self.client.get(url)
        return self._json(response)

    def mensual(self, periodo: str) -> ApiResponse[dict[str, Any]]:
        """
        Tramos del impuesto de segunda categoría de un mes.

        Respuesta (ejemplo)::

            {
              "data": {
                "202410": [
                  {
                    "desde": 0,
                    "hasta": 866310,
                    "tasa": 0,
                    "rebaja": 0,
                    "maximo": null
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param str periodo: Período en formato AAAAMM (año y mes).
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, los tramos del período, con el período (AAAAMM)
            como clave. Cada tramo trae `desde`, `hasta`, `tasa`,
            `rebaja` y `maximo`.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = (
            '/sii/indicadores/impuesto_segunda_categoria/mensual/%(periodo)s'
            % {'periodo': periodo}
        )
        response = self.client.get(url)
        return self._json(response)
