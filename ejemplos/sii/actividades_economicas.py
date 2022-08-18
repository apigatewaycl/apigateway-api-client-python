#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
API Gateway: Cliente en Python
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
<http://www.gnu.org/licenses/lgpl.html>.
"""


import os, sys
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, app_dir)

from libredte.api_client.sii.actividades_economicas import ActividadesEconomicas
from sasco_utils.dict import dict_save_to_json, dict_save_to_csv


# crear cliente de la API
ae = ActividadesEconomicas()

# CASO 1: todas las actividades
listado = ae.listado()
dict_save_to_json('actividades_economicas_todas.json', listado)

# guardar el CASO 1 en un csv
actividades = []
for categoria in listado:
    for subcategoria in listado[categoria]:
        for actividad in listado[categoria][subcategoria]:
            actividades.append(actividad)
dict_save_to_csv('actividades_economicas_todas.csv', actividades)

# CASO 2: sólo actividades de primera categoría
listado = ae.listado_primera_categoria()
dict_save_to_json('actividades_economicas_1era.json', listado)

# CASO 3: sólo actividades de segunda categoría
listado = ae.listado_segunda_categoria()
dict_save_to_json('actividades_economicas_2da.json', listado)
