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

from libredte.api_client.sii.bhe import BheEmitidas


# datos del emisor
USUARIO_RUT = ''
USUARIO_CLAVE = ''
RECEPTOR_EMAIL = ''
PERIODO = 202102
EMISOR_RUT = USUARIO_RUT

# crear cliente de la API
bhe = BheEmitidas(USUARIO_RUT, USUARIO_CLAVE)

# CASO 1: boletas del periodo
documentos = bhe.documentos(EMISOR_RUT, PERIODO)
print('CASO 1: boletas del periodo')
print(documentos, end="\n\n")

# CASO 2: emitir boleta
datos = {
    'Encabezado': {
        'IdDoc': {
            'FchEmis': '2021-04-18',
            'TipoRetencion': BheEmitidas.RETENCION_RECEPTOR
        },
        'Emisor': {
            'RUTEmisor': EMISOR_RUT
        },
        'Receptor': {
            'RUTRecep': '66666666-6',
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
boleta = bhe.emitir(datos)
boleta_folio = boleta['Encabezado']['IdDoc']['Folio']
boleta_codigo = boleta['Encabezado']['IdDoc']['CodigoBarras']
print('CASO 2: emitir boleta')
print(boleta, end="\n\n")

# CASO 3: bajar PDF
pdf = bhe.pdf(boleta_codigo)
with open(EMISOR_RUT + '_bhe_' + boleta_codigo + '.pdf', 'wb') as f:
    f.write(pdf)
print('CASO 3: PDF descargado', end="\n\n")

# CASO 4: enviar por email
resultado = bhe.email(boleta_codigo, RECEPTOR_EMAIL)
print('CASO 4: enviar por email')
print(resultado, end="\n\n")

# CASO 5: anular
boleta_anulada = bhe.anular(EMISOR_RUT, boleta_folio, BheEmitidas.ANULACION_CAUSA_ERROR_DIGITACION)
print('CASO 5: anular')
print(boleta_anulada, end="\n\n")
