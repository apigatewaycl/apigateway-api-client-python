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

from libredte.api_client.sii.rcv import Rcv
from sasco_utils.dict import dict_save_to_json


# datos del contribuyente
CONTRIBUYENTE_RUT = ''
CONTRIBUYENTE_CLAVE = ''
PERIODO = 202103
estados = ['REGISTRO', 'PENDIENTE', 'NO_INCLUIR', 'RECLAMADO']

# crear cliente de la API
rcv = Rcv(CONTRIBUYENTE_RUT, CONTRIBUYENTE_CLAVE)

# CASO 1: resumen de compras y detalle de compras con tipo rcv
for estado in estados:
    resumen = rcv.compras_resumen(CONTRIBUYENTE_RUT, PERIODO, estado)
    filename = '%(contribuyente)s_compras_resumen_%(periodo)s_%(estado)s.json' % {
        'contribuyente': CONTRIBUYENTE_RUT,
        'periodo': str(PERIODO),
        'estado': str(estado),
    }
    dict_save_to_json(filename, resumen)
    for r in resumen:
        if r['dcvTipoIngresoDoc'] != 'DET_ELE' or r['rsmnTotDoc'] == 0:
            continue
        detalle = rcv.compras_detalle(CONTRIBUYENTE_RUT, PERIODO, r['rsmnTipoDocInteger'], estado)
        filename = '%(contribuyente)s_compras_detalle_%(periodo)s_%(dte)s_%(estado)s.json' % {
            'contribuyente': CONTRIBUYENTE_RUT,
            'periodo': str(PERIODO),
            'dte': str(r['rsmnTipoDocInteger']),
            'estado': str(estado),
        }
        dict_save_to_json(filename, detalle)

# CASO 2: detalle de compras con tipo rcv_csv
detalle = rcv.compras_detalle(CONTRIBUYENTE_RUT, PERIODO)
filename = '%(contribuyente)s_compras_detalle_%(periodo)s.json' % {
    'contribuyente': CONTRIBUYENTE_RUT,
    'periodo': str(PERIODO),
}
dict_save_to_json(filename, detalle)

# CASO 3: resumen de ventas y detalle de ventas con tipo rcv
resumen = rcv.ventas_resumen(CONTRIBUYENTE_RUT, PERIODO)
filename = '%(contribuyente)s_ventas_resumen_%(periodo)s.json' % {
    'contribuyente': CONTRIBUYENTE_RUT,
    'periodo': str(PERIODO),
}
dict_save_to_json(filename, resumen)
for r in resumen:
    if r['dcvTipoIngresoDoc'] != 'DET_ELE' or r['rsmnTotDoc'] == 0:
        continue
    detalle = rcv.ventas_detalle(CONTRIBUYENTE_RUT, PERIODO, r['rsmnTipoDocInteger'])
    filename = '%(contribuyente)s_ventas_detalle_%(periodo)s_%(dte)s.json' % {
        'contribuyente': CONTRIBUYENTE_RUT,
        'periodo': str(PERIODO),
        'dte': str(r['rsmnTipoDocInteger']),
    }
    dict_save_to_json(filename, detalle)

# CASO 4: detalle de ventas con tipo rcv_csv
detalle = rcv.ventas_detalle(CONTRIBUYENTE_RUT, PERIODO)
filename = '%(contribuyente)s_ventas_detalle_%(periodo)s.json' % {
    'contribuyente': CONTRIBUYENTE_RUT,
    'periodo': str(PERIODO),
}
dict_save_to_json(filename, detalle)
