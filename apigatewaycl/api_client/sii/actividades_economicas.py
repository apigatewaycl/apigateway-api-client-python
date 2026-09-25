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
Módulo para obtener las actividades económicas del SII.

Para más información sobre la API, consulte la `documentación completa
de Actividades Económicas
<https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase, ApiResponse


class ActividadesEconomicas(ApiBase):
    """
    Cliente para las actividades económicas del SII.

    Provee métodos para obtener listados de actividades económicas,
    tanto de primera como de segunda categoría.
    """

    def listado(
        self, categoria: int | None = None
    ) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene un listado de actividades económicas, filtrando por categoría.

        Respuesta (ejemplo)::

            {
              "data": {
                "Explotación de minas y canteras": {
                  "Actividades de apoyo para la extracción de petróleo y...": [
                    {
                      "codigo": "091002",
                      "actividad_economica": "Actividades de apoyo para...",
                      "afecta_iva": false,
                      "categoria": "G",
                      "internet": true
                    }
                  ],
                  "Actividades de apoyo para la explotación de otras min...": [
                    {
                      "codigo": "099002",
                      "actividad_economica": "Actividades de apoyo para...",
                      "afecta_iva": false,
                      "categoria": "G",
                      "internet": true
                    }
                  ]
                }
              },
              "metadata": {"timestamp": "..."}
            }

        :param int categoria: Categoría de las actividades económicas
            (opcional).
        :return: Respuesta de la API, con `data` y `metadata`. En `data`, el
            listado de actividades económicas.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = self._build_url(
            '/sii/contribuyentes/actividades_economicas',
            categoria=categoria,
        )
        response = self.client.get(url)
        return self._json(response)

    def listado_primera_categoria(self) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene un listado de actividades económicas de primera categoría.

        Respuesta (ejemplo)::

            {
              "data": {
                "Explotación de minas y canteras": {
                  "Actividades de apoyo para la extracción de petróleo y...": [
                    {
                      "codigo": "091002",
                      "actividad_economica": "Actividades de apoyo para...",
                      "afecta_iva": false,
                      "categoria": "G",
                      "internet": true
                    }
                  ],
                  "Actividades de apoyo para la explotación de otras min...": [
                    {
                      "codigo": "099002",
                      "actividad_economica": "Actividades de apoyo para...",
                      "afecta_iva": false,
                      "categoria": "G",
                      "internet": true
                    }
                  ]
                }
              },
              "metadata": {"timestamp": "..."}
            }

        :return: Respuesta de la API, con `data` y `metadata`. En `data`, el
            listado de primera categoría.
        :rtype: ApiResponse[dict[str, Any]]
        """
        return self.listado(1)

    def listado_segunda_categoria(self) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene un listado de actividades económicas de segunda categoría.

        Respuesta (ejemplo)::

            {
              "data": {
                "Explotación de minas y canteras": {
                  "Actividades de apoyo para la extracción de petróleo y...": [
                    {
                      "codigo": "091002",
                      "actividad_economica": "Actividades de apoyo para...",
                      "afecta_iva": false,
                      "categoria": "G",
                      "internet": true
                    }
                  ],
                  "Actividades de apoyo para la explotación de otras min...": [
                    {
                      "codigo": "099002",
                      "actividad_economica": "Actividades de apoyo para...",
                      "afecta_iva": false,
                      "categoria": "G",
                      "internet": true
                    }
                  ]
                }
              },
              "metadata": {"timestamp": "..."}
            }

        :return: Respuesta de la API, con `data` y `metadata`. En `data`, el
            listado de segunda categoría.
        :rtype: ApiResponse[dict[str, Any]]
        """
        return self.listado(2)
