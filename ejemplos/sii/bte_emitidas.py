#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
LibreDTE API Client
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

from libredte.api_client.sii.bte import BteEmitidas
from ejemplos.json_save import json_save


# datos del emisor
EMISOR_RUT = ''
EMISOR_CLAVE = ''
PERIODO = 202102

# importaciones para el ejemplo
import sys
import json

# crear cliente de la API
bte = BteEmitidas(EMISOR_RUT, EMISOR_CLAVE)

# CASO 1: boletas del periodo
documentos = bte.documentos(EMISOR_RUT, PERIODO)
filename = '%(emisor)s_bte_%(periodo)s' % {
    'emisor': EMISOR_RUT,
    'periodo': str(PERIODO),
}
json_save(filename, documentos)

# CASO 2: bajar HTML
if len(documentos) > 0:
    boleta_codigo = documentos[0]['codigo']
    html = bte.html(boleta_codigo)
    filename = '%(emisor)s_bte_%(periodo)s_%(codigo)s.html' % {
        'emisor': EMISOR_RUT,
        'periodo': str(PERIODO),
        'codigo': boleta_codigo,
    }
    with open(filename, 'wb') as f:
        f.write(html)
