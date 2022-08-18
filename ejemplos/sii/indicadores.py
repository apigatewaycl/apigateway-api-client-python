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

from libredte.api_client.sii.indicadores import Uf


# datos del ejemplo
ANIO = 2021

# crear cliente de la API
uf = Uf()

# CASO 1: obtener valores de la UF de todo un año
print(uf.anual(ANIO), end="\n\n")

# CASO 2: obtener valores de la UF de todo un mes (enero del anio)
print(uf.mensual(str(ANIO) + '01'), end="\n\n")

# CASO 3: obtener valores de la UF de un día específico (1ero de enero del ANIO)
print(uf.diario(str(ANIO) + '-01-01'))
