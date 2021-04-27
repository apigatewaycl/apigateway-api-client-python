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

from libredte.api_client.sii.respaldo_sii import RespaldoSii


# datos del contribuyente
# ejemplo simple, no tiene todas las opciones, las mínimas
# ej: al indicar sólo "período desde" el hasta será el mismo, o sea se
# respaldará sólo un período
EMPRESA_RUT = ''
EMPRESA_CLAVE = '' # no se usa para el respaldo mipyme
USUARIO_RUT = '' # obligatorio para el respaldo mipyme
USUARIO_CLAVE = '' # obligatorio para el respaldo mipyme
PERIODO_DESDE = 202104 # por defecto bajará sólo el "período desde"
RESPALDAR = 'mipyme' # respaldar todo: 'mipyme,rcv,bhe,bte'

# realizar respaldo de un periodo
try:
    respaldo = RespaldoSii(
        empresa_rut = EMPRESA_RUT,
        empresa_clave = EMPRESA_CLAVE,
        usuario_rut = USUARIO_RUT,
        usuario_clave = USUARIO_CLAVE,
        periodo_desde = PERIODO_DESDE,
        respaldar = RESPALDAR,
    )
    estado = respaldo.generar()
    if estado is False:
        print('Falló la ejecución del respaldo')
except KeyboardInterrupt:
    pass
