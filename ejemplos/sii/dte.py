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

from libredte.api_client.sii.dte import Contribuyentes, Emitidos

### CONTRIBUYENTES ###

# datos del ejemplo
RUT = ''

if RUT != '':

    # crear cliente de la API
    c = Contribuyentes()

    # CASO 1: autorización DTE
    print(c.autorizacion(RUT), end="\n\n")

### DOCUMENTOS EMITIDOS ###

EMISOR = '76192083-9'
CLAVE = ''
RECEPTOR = '77666555-4'
DTE = 33
FOLIO = 12018
FECHA = '2021-08-26'
TOTAL = 30000
FIRMA = None

if CLAVE != '':

    e = Emitidos(EMISOR, CLAVE)
    estado = e.verificar(
        EMISOR,
        RECEPTOR,
        DTE,
        FOLIO,
        FECHA,
        TOTAL,
        FIRMA
    )
    print(estado)
