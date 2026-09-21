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
Módulo para tasación fiscal de vehículos del SII.

Para más información sobre la API, consulte la `documentación completa
de Vehículos <https://developers.apigateway.cl/>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class Vehiculos(ApiBase):
    """
    Cliente para tasación fiscal de vehículos de la API.

    Recurso público — solo requiere el token de la plataforma, no
    credenciales de un contribuyente (`identificador`/`clave`).
    """

    def buscar(
        self,
        anio: int | None = None,
        anio_tasa: int | None = None,
        categoria: int | None = None,
        marca: int | None = None,
        modelo: str | None = None,
        tipo: int | None = None,
        version: str | None = None,
    ) -> Any:
        """
        Busca la tasación fiscal de un vehículo y su permiso de circulación.

        Sin filtros, descarga todos los registros — se recomienda al
        menos `marca` y `anio` para una búsqueda eficiente.

        :param int anio: Año del vehículo.
        :param int anio_tasa: Año fiscal de la búsqueda (por defecto
            el año actual).
        :param int categoria: ID de categoría (1 = liviano).
        :param int marca: ID de la marca (ej. 229 = SUZUKI).
        :param str modelo: Modelo del vehículo.
        :param int tipo: ID del tipo de vehículo (6 = SUV).
        :param str version: Versión del vehículo.
        :return: Listado de vehículos que calzan con la búsqueda.
        :rtype: list[dict]
        """
        # TODO: Implementar.

    def categorias_tipos(self, categoria: str) -> Any:
        """
        Tipos de vehículos disponibles para una categoría.

        :param str categoria: ID de categoría (`'1'` livianos, `'2'`
            pesados, `'3'` motos).
        :return: Listado de tipos (id, nombre).
        :rtype: list[dict]
        """
        # TODO: Implementar.

    def categorias_marcas(self, categoria: str) -> Any:
        """
        Marcas de vehículos disponibles para una categoría.

        :param str categoria: ID de categoría (`'1'` livianos, `'2'`
            pesados, `'3'` motos).
        :return: Listado de marcas (id, nombre).
        :rtype: list[dict]
        """
        # TODO: Implementar.

    def categorias_caracteristicas(self, categoria: str) -> Any:
        """
        Características disponibles para una categoría de vehículo.

        :param str categoria: ID de categoría (`'1'` livianos, `'2'`
            pesados, `'3'` motos).
        :return: Listado de características, con sus valores posibles.
        :rtype: list[dict]
        """
        # TODO: Implementar.
