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
<https://developers.apigateway.cl/#c88f90b6-36bb-4dc2-ba93-6e418ff42098>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class Contribuyentes(ApiBase):
    """
    Cliente para los endpoints de contribuyentes de la API de API Gateway.

    Hereda de ApiBase y utiliza su funcionalidad para realizar
    solicitudes a la API.
    """

    def situacion_tributaria(self, rut: str) -> Any:
        """
        Obtiene la situación tributaria de un contribuyente.

        :param str rut: RUT del contribuyente.
        :return: Respuesta JSON con la situación tributaria.
        :rtype: dict
        """
        url = '/sii/contribuyentes/situacion_tributaria/tercero/%(rut)s' % {
            'rut': rut
        }
        response = self.client.get(url)
        return response.json()

    def verificar_rut(self, rut: str, serie: str) -> Any:
        """
        Verifica la cédula RUT de un contribuyente por su número de serie.

        :param str rut: RUT del contribuyente (ej. `76192083-9`).
        :param str serie: Número de serie de la cédula a verificar.
        :return: Respuesta JSON con la verificación del RUT.
        :rtype: dict
        """
        url = '/sii/contribuyentes/rut/verificar/%(rut)s/%(serie)s' % {
            'rut': rut,
            'serie': serie,
        }
        response = self.client.get(url)
        return response.json()
