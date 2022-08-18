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

from libredte.api_client.sii.bhe import BheRecibidas
from sasco_utils.dict import dict_save_to_json


# datos del receptor
RECEPTOR_RUT = ''
RECEPTOR_CLAVE = ''
PERIODO = 202102

# datos para observar una boleta
OBSERVAR_EMISOR_RUT = ''
OBSERVAR_NUMERO = 3166

# importaciones para el ejemplo
import sys
import json

# crear cliente de la API
bhe = BheRecibidas(RECEPTOR_RUT, RECEPTOR_CLAVE)

# CASO 1: boletas del periodo
documentos = bhe.documentos(RECEPTOR_RUT, PERIODO)
filename = '%(receptor)s_bhe_%(periodo)s.json' % {
    'receptor': RECEPTOR_RUT,
    'periodo': str(PERIODO),
}
dict_save_to_json(filename, documentos)

# CASO 2: bajar PDF
if len(documentos) > 0:
    boleta_codigo = documentos[0]['codigo']
    pdf = bhe.pdf(boleta_codigo)
    filename = '%(receptor)s_bhe_%(periodo)s_%(codigo)s.pdf' % {
        'receptor': RECEPTOR_RUT,
        'periodo': str(PERIODO),
        'codigo': boleta_codigo,
    }
    with open(filename, 'wb') as f:
        f.write(pdf)

# CASO 3: observar una boleta
if OBSERVAR_EMISOR_RUT != '':
    resultado = bhe.observar(OBSERVAR_EMISOR_RUT, OBSERVAR_NUMERO)
    filename = '%(emisor)s_bhe_%(numero)s_observada.json' % {
        'emisor': OBSERVAR_EMISOR_RUT,
        'numero': str(OBSERVAR_NUMERO),
    }
    dict_save_to_json(filename, resultado)
