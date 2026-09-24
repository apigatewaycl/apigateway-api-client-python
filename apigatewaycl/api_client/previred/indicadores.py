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
Módulo para los Indicadores Previsionales de Previred.

Para más información sobre la API, consulte la `documentación completa
de Previred <https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase, Respuesta


class Indicadores(ApiBase):
    """Cliente para los indicadores previsionales de Previred."""

    def periodos(self) -> Respuesta[list[dict[str, Any]]]:
        """
        Listado de URLs del PDF de los indicadores previsionales.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "url": "https://www.previred.com/wp-content/u...",
                  "periodo": "202501"
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de indicadores con su URL de PDF y período.
        :rtype: dict
        """
        response = self.client.get('/previred/indicadores/periodos')
        return self._json(response)

    def pdf(self, periodo: str) -> bytes:
        """
        PDF de un indicador previsional.

        :param str periodo: Período del indicador (AAAAMM).
        :return: Contenido del PDF del indicador.
        :rtype: bytes
        """
        url = '/previred/indicadores/pdf/%(periodo)s' % {'periodo': periodo}
        response = self.client.get(url)
        return response.content

    def data(self, periodo: str) -> Respuesta[dict[str, Any]]:
        """
        Datos de un indicador previsional.

        Las tasas se entregan como fracción (`0.0144` equivale a
        `1,44%`) y los montos en pesos.

        Respuesta (ejemplo)::

            {
              "data": {
                "indicadores": {
                  "moneda": {
                    "CLF": 40873.77,
                    "UTM": 71649,
                    "UTA": 859788,
                    "periodo_anterior": {"CLF": 40844.79}
                  },
                  "afc": {
                    "plazo_indefinido_empleador": 0.024,
                    "plazo_indefinido_trabajador": 0.006,
                    "plazo_fijo_empleador": 0.03,
                    "plazo_fijo_trabajador": 0,
                    "superior_11_anios_empleador": 0.008,
                    "...": "..."
                  },
                  "afp": {
                    "empleador": 0.001,
                    "trabajador": 0.1,
                    "comision": {
                      "03": 0.0144,
                      "05": 0.0127,
                      "08": 0.0145,
                      "29": 0.0116,
                      "33": 0.0144,
                      "...": "..."
                    },
                    "sis": 0.0178
                  },
                  "apv": {"tope_mensual": 2043689, "tope_anual": 24524262},
                  "asignacion_familiar": {
                    "tramo_a_hasta": 649039,
                    "tramo_a_monto": 22601,
                    "tramo_b_hasta": 947990,
                    "tramo_b_monto": 13870,
                    "tramo_c_hasta": 1478539,
                    "...": "..."
                  },
                  "deposito_convenido": {"tope_anual": 36786393},
                  "renta_imponible_minima": {
                    "general": 553553,
                    "menores_18_mayores_65": 412938,
                    "casa_particular": 553553,
                    "fines_no_remuneracionales": 356815
                  },
                  "renta_imponible_tope": {
                    "afp": 3678639,
                    "inp": 2450687,
                    "afc": 5526134
                  },
                  "...": "..."
                },
                "periodo": "202608",
                "periodo_anterior": "202607",
                "periodo_siguiente": "202609"
              },
              "metadata": {"timestamp": "..."}
            }

        :param str periodo: Período del indicador (AAAAMM).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, períodos, moneda (UF/UTM/UTA), renta imponible, AFP,
            seguro de cesantía, seguro social, otras cotizaciones, ahorro
            previsional y asignación familiar.
        :rtype: dict
        """
        url = '/previred/indicadores/data/%(periodo)s' % {'periodo': periodo}
        response = self.client.get(url)
        return self._json(response)
