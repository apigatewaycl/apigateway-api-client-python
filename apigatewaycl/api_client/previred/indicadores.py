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

from .. import ApiBase


class Indicadores(ApiBase):
    """Cliente para los indicadores previsionales de Previred."""

    def periodos(self) -> Any:
        """
        Listado de URLs del PDF de los indicadores previsionales.

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de indicadores con su URL de PDF y período.
        :rtype: dict
        """
        response = self.client.get('/previred/indicadores/periodos')
        return response.json()

    def pdf(self, periodo: str) -> Any:
        """
        PDF de un indicador previsional.

        :param str periodo: Período del indicador (AAAAMM).
        :return: Contenido del PDF del indicador.
        :rtype: bytes
        """
        url = '/previred/indicadores/pdf/%(periodo)s' % {'periodo': periodo}
        response = self.client.get(url)
        return response.content

    def data(self, periodo: str) -> Any:
        """
        Datos de un indicador previsional.

        Las tasas se entregan como fracción (`0.0144` equivale a
        `1,44%`) y los montos en pesos.

        :param str periodo: Período del indicador (AAAAMM).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, períodos, moneda (UF/UTM/UTA), renta imponible, AFP,
            seguro de cesantía, seguro social, otras cotizaciones, ahorro
            previsional y asignación familiar.
        :rtype: dict
        """
        url = '/previred/indicadores/data/%(periodo)s' % {'periodo': periodo}
        response = self.client.get(url)
        return response.json()
