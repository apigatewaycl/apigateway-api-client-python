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
Tipos de las respuestas JSON de la API.

Describen la forma del cuerpo que entrega la API, sin transformarlo:
en ejecución siguen siendo los mismos `dict` de `response.json()`.
"""

from __future__ import annotations

from typing import Any, TypedDict


class ApiResponse[T](TypedDict):
    """
    Cuerpo JSON de una respuesta exitosa de la API.

    `data` trae el resultado: según el recurso es un `dict` o una
    `list`, y `T` indica cuál (`ApiResponse[dict[str, Any]]` o
    `ApiResponse[list[dict[str, Any]]]`). `metadata` trae los datos de
    la consulta (`timestamp` siempre; el resto de las claves, como la
    paginación, depende del recurso y se deja abierto para no
    amarrarlo a una lista fija). Con `raise_for_status=False` una
    respuesta de error no tiene esta forma.
    """

    data: T
    metadata: dict[str, Any]
