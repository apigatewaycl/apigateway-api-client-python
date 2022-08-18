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

from libredte.api_client.sii.portal_mipyme import Contribuyentes, DteEmitidos, DteRecibidos
from sasco_utils.dict import dict_save_to_json


# datos del contribuyente
USUARIO_RUT = ''
USUARIO_CLAVE = ''
CONTRIBUYENTE_RUT = ''
FECHA_DESDE = '2020-01-01'
FECHA_HASTA = '2020-01-31'

# sólo bajar el PDF y XML del primer DTE (para hacer más rápido el ejemplo)
# asignar esto en False bajará todos los PDF y XML del rango de fechas
bajarSolo1ro = True

# crear clientes de la API
contribuyentes = Contribuyentes(USUARIO_RUT, USUARIO_CLAVE)
dte_emitidos = DteEmitidos(USUARIO_RUT, USUARIO_CLAVE)
dte_recibidos = DteRecibidos(USUARIO_RUT, USUARIO_CLAVE)

# CASO 1: datos de un contribuyente
datos = contribuyentes.info('76192083-9', CONTRIBUYENTE_RUT, 34)
filename = '%(contribuyente)s_mipyme_info.json' % {
    'contribuyente': CONTRIBUYENTE_RUT,
}
dict_save_to_json(filename, datos)

# CASO 2: documentos emitidos
documentos = dte_emitidos.documentos(CONTRIBUYENTE_RUT, {
    'FEC_DESDE': FECHA_DESDE,
    'FEC_HASTA': FECHA_HASTA,
})
filename = '%(contribuyente)s_mipyme_dte_emitidos.json' % {
    'contribuyente': CONTRIBUYENTE_RUT,
}
dict_save_to_json(filename, documentos)

for documento in documentos:

    # CASO 3: bajar PDF de un DTE emitido
    pdf = dte_emitidos.pdf(CONTRIBUYENTE_RUT, documento['codigo'])
    # usar el folio también funciona, pero es más lento
    #pdf = dte_emitidos.pdf(CONTRIBUYENTE_RUT, documento['dte'], documento['folio'])
    filename = '%(contribuyente)s_mipyme_dte_emitido_T%(dte)sF%(folio)s.pdf' % {
       'contribuyente': CONTRIBUYENTE_RUT,
       'dte': documento['dte'],
       'folio': documento['folio'],
    }
    with open(filename, 'wb') as f:
        f.write(pdf)

    # CASO 4: bajar XML de un DTE recibido (mismo caso que el PDF)
    xml = dte_emitidos.xml(CONTRIBUYENTE_RUT, documento['dte'], documento['folio'])
    filename = '%(contribuyente)s_mipyme_dte_emitido_T%(dte)sF%(folio)s.xml' % {
       'contribuyente': CONTRIBUYENTE_RUT,
       'dte': documento['dte'],
       'folio': documento['folio'],
    }
    with open(filename, 'w') as f:
        f.write(xml)

    if bajarSolo1ro:
        break

# CASO 5: documentos recibidos
documentos = dte_recibidos.documentos(CONTRIBUYENTE_RUT, {
    'FEC_DESDE': FECHA_DESDE,
    'FEC_HASTA': FECHA_HASTA,
})
filename = '%(contribuyente)s_mipyme_dte_recibidos.json' % {
    'contribuyente': CONTRIBUYENTE_RUT,
}
dict_save_to_json(filename, documentos)

for documento in documentos:

    emisor = documento['rut'] + '-' + documento['dv']

    # CASO 6: bajar PDF de un DTE recibido
    pdf = dte_recibidos.pdf(CONTRIBUYENTE_RUT, emisor, documento['codigo'])
    # usar el folio también funciona, pero es más lento
    #pdf = dte_recibidos.pdf(CONTRIBUYENTE_RUT, emisor, documento['dte'], documento['folio'])
    filename = '%(contribuyente)s_mipyme_dte_recibido_%(emisor)s_T%(dte)sF%(folio)s.pdf' % {
       'contribuyente': CONTRIBUYENTE_RUT,
       'emisor': emisor,
       'dte': documento['dte'],
       'folio': documento['folio'],
    }
    with open(filename, 'wb') as f:
        f.write(pdf)

    # CASO 7: bajar XML de un DTE recibido (mismo caso que el PDF)
    xml = dte_recibidos.xml(CONTRIBUYENTE_RUT, emisor, documento['dte'], documento['folio'])
    filename = '%(contribuyente)s_mipyme_dte_recibido_%(emisor)s_T%(dte)sF%(folio)s.xml' % {
       'contribuyente': CONTRIBUYENTE_RUT,
       'emisor': emisor,
       'dte': documento['dte'],
       'folio': documento['folio'],
    }
    with open(filename, 'w') as f:
        f.write(xml)

    if bajarSolo1ro:
        break
