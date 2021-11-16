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
from sasco_utils.dict import dict_save_to_json


# datos del emisor
EMISOR_RUT = ''
EMISOR_CLAVE = ''
PERIODO = 202102
RECEPTOR_RUT = '66666666-6'

# importaciones para el ejemplo
import sys
import json

# crear cliente de la API
bte = BteEmitidas(EMISOR_RUT, EMISOR_CLAVE)

# CASO 1: boletas del periodo
documentos = bte.documentos(EMISOR_RUT, PERIODO)
filename = '%(emisor)s_bte_%(periodo)s.json' % {
    'emisor': EMISOR_RUT,
    'periodo': str(PERIODO),
}
dict_save_to_json(filename, documentos)

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


# CASO 3: emitir boleta
datos = {
    'Encabezado': {
        'IdDoc': {
            'FchEmis': '2021-04-23'
        },
        'Emisor': {
            'RUTEmisor': EMISOR_RUT
        },
        'Receptor': {
            'RUTRecep': RECEPTOR_RUT,
            'RznSocRecep': 'Receptor generico',
            'DirRecep': 'Santa Cruz',
            'CmnaRecep': 'Santa Cruz'
        }
    },
    'Detalle': [
        {
            'NmbItem': 'Prueba integracion LibreDTE API 1',
            'MontoItem': 50
        },
        {
            'NmbItem': 'Prueba integracion LibreDTE API 2',
            'MontoItem': 100
        }
    ]
}
boleta = bte.emitir(datos)
boleta_folio = boleta['Encabezado']['IdDoc']['Folio']
filename = '%(emisor)s_bte_%(numero)s.json' % {
    'emisor': EMISOR_RUT,
    'numero': str(boleta_folio),
}
dict_save_to_json(filename, boleta)

# CASO 4: anular boleta
resultado = bte.anular(EMISOR_RUT, boleta_folio)
filename = '%(emisor)s_bte_%(numero)s_anulada.json' % {
    'emisor': EMISOR_RUT,
    'numero': str(boleta_folio),
}
dict_save_to_json(filename, boleta)

# CASO 5: tasa de receptor
tasa = bte.receptor_tasa(EMISOR_RUT, RECEPTOR_RUT)
filename = 'bte_receptor_tasa_%(receptor)s.json' % {
    'receptor': RECEPTOR_RUT,
}
dict_save_to_json(filename, tasa)
