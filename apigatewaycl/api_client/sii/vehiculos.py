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
de Vehículos <https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase, ApiResponse


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
    ) -> ApiResponse[list[dict[str, Any]]]:
        """
        Busca la tasación fiscal de un vehículo y su permiso de circulación.

        `categoria` y `tipo` son obligatorios: sin ellos la API
        responde `Debe especificar la categoría del vehículo.` o
        `Debe especificar el tipo de vehículo.`. Los IDs válidos se
        obtienen con `categorias_tipos()` y `categorias_marcas()`.
        Agregar `marca` y `anio` acota bastante el resultado.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "anio": "2017",
                  "anioTasa": "2020",
                  "cara": 5,
                  "cateId": "6",
                  "cateName": "Liviano",
                  "code": "SU2290241",
                  "equi": 0,
                  "haveFeatures": false,
                  "...": "..."
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        :param int anio: Año del vehículo.
        :param int anio_tasa: Año fiscal de la búsqueda (por defecto
            el año actual).
        :param int categoria: ID de categoría, obligatorio
            (1 = liviano).
        :param int marca: ID de la marca (ej. 229 = SUZUKI).
        :param str modelo: Modelo del vehículo.
        :param int tipo: ID del tipo de vehículo, obligatorio
            (6 = SUV).
        :param str version: Versión del vehículo.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de vehículos que calzan con la búsqueda.
        :rtype: ApiResponse[list[dict[str, Any]]]
        """
        # La API recibe los filtros como el cuerpo completo, no
        # anidados bajo una clave. Los que no se indiquen no se envían.
        filtros = {
            'anio': anio,
            'anio_tasa': anio_tasa,
            'categoria': categoria,
            'marca': marca,
            'modelo': modelo,
            'tipo': tipo,
            'version': version,
        }
        body = {
            clave: valor
            for clave, valor in filtros.items()
            if valor is not None
        }
        response = self.client.post('/sii/vehiculos/tasacion/buscar', body)
        return self._json(response)

    def categorias_tipos(
        self, categoria: str
    ) -> ApiResponse[list[dict[str, Any]]]:
        """
        Tipos de vehículos disponibles para una categoría.

        Respuesta (ejemplo)::

            {
              "data": [{"id": 37, "name": "Cabriolet"}],
              "metadata": {"timestamp": "..."}
            }

        :param str categoria: ID de categoría (`'1'` livianos, `'2'`
            pesados, `'3'` motos).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de tipos (id, nombre).
        :rtype: ApiResponse[list[dict[str, Any]]]
        """
        url = '/sii/vehiculos/categorias/tipos/%(categoria)s' % {
            'categoria': categoria,
        }
        response = self.client.get(url)
        return self._json(response)

    def categorias_marcas(
        self, categoria: str
    ) -> ApiResponse[list[dict[str, Any]]]:
        """
        Marcas de vehículos disponibles para una categoría.

        Respuesta (ejemplo)::

            {
              "data": [{"id": "1", "name": "ACADIAN"}],
              "metadata": {"timestamp": "..."}
            }

        :param str categoria: ID de categoría (`'1'` livianos, `'2'`
            pesados, `'3'` motos).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de marcas (id, nombre).
        :rtype: ApiResponse[list[dict[str, Any]]]
        """
        url = '/sii/vehiculos/categorias/marcas/%(categoria)s' % {
            'categoria': categoria,
        }
        response = self.client.get(url)
        return self._json(response)

    def categorias_caracteristicas(
        self, categoria: str
    ) -> ApiResponse[list[dict[str, Any]]]:
        """
        Características disponibles para una categoría de vehículo.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "id": 1,
                  "name": "Combustible",
                  "data": [{"id": "2", "name": "Bencina"}]
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        :param str categoria: ID de categoría (`'1'` livianos, `'2'`
            pesados, `'3'` motos).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de características, con sus valores posibles.
        :rtype: ApiResponse[list[dict[str, Any]]]
        """
        url = '/sii/vehiculos/categorias/caracteristicas/%(categoria)s' % {
            'categoria': categoria,
        }
        response = self.client.get(url)
        return self._json(response)
