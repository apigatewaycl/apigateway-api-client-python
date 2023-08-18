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
PERIODO = 202308

# importaciones para el ejemplo
import sys
import json

# crear cliente de la API
bhe = BheRecibidas(RECEPTOR_RUT, RECEPTOR_CLAVE)

# config inicial
boletas = []
pagina = 1
pagina_sig_codigo = '00000000000000'

# iteración
documentos = bhe.documentos(RECEPTOR_RUT, PERIODO, pagina = pagina, pagina_sig_codigo = pagina_sig_codigo)
boletas = boletas + documentos['boletas']

# guardar boletas en archivo
filename = '%(receptor)s_bhe_%(periodo)s.json' % {
    'receptor': RECEPTOR_RUT,
    'periodo': str(PERIODO),
}
dict_save_to_json(filename, boletas)

# resultado
print('Se guardaron %(n_boletas)s en el archivo %(filename)s', {
    'n_boletas': len(boletas),
    'filename': filename
})
