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
Módulo para obtener datos de los contribuyentes a través del SII.

Para más información sobre la API, consulte la `documentación completa
de Contribuyentes
<https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase, ApiResponse


class Contribuyentes(ApiBase):
    """
    Cliente para los endpoints de contribuyentes de la API de API Gateway.

    Hereda de ApiBase y utiliza su funcionalidad para realizar
    solicitudes a la API.
    """

    def situacion_tributaria(self, rut: str) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene la situación tributaria de un contribuyente.

        Respuesta (ejemplo)::

            {
              "data": {
                "rut": 76192083,
                "dv": "9",
                "razon_social": "EMPRESA EJEMPLO SPA",
                "inicio_actividades": true,
                "fecha_inicio_actividades": "2012-06-08",
                "fecha_consulta": "18-05-2026 12:32:03",
                "pro_pyme": true,
                "moneda_extranjera": false,
                "...": "..."
              },
              "metadata": {"timestamp": "..."}
            }

        :param str rut: RUT del contribuyente.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, situación tributaria.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/contribuyentes/situacion_tributaria/tercero/%(rut)s' % {
            'rut': rut
        }
        response = self.client.get(url)
        return self._json(response)

    def verificar_rut(
        self,
        rut: str,
        serie: str,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Verifica la cédula RUT de un contribuyente por su número de serie.

        Respuesta (ejemplo)::

            {
              "data": {
                "rut": "78.580.345-6",
                "nombre_o_razon_social": "NOMBRE O RAZÓN SOCIAL",
                "direccion_principal_casa_matriz": "DANIEL BARROS GREZ 191...",
                "n_de_serie": "22389021489",
                "fecha_de_emision": "11/11/2024",
                "rut_usuario_cedula": "12.345.678-9",
                "usuario_cedula": "USUARIO CÉDULA",
                "tipo": "Cédula"
              },
              "metadata": {"timestamp": "..."}
            }

        :param str rut: RUT del contribuyente (ej. `76192083-9`).
        :param str serie: Número de serie de la cédula a verificar.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, verificación del RUT.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/contribuyentes/rut/verificar/%(rut)s/%(serie)s' % {
            'rut': rut,
            'serie': serie,
        }
        response = self.client.get(url)
        return self._json(response)
