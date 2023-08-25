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

# importaciones para el ejemplo
import sys
import json
import copy


# clase encargada de generar los registros en JSON y CSV
class TestLog:

    logs = []
    log_console_mask = '%(pagina)20s %(n_boletas_pagina)20s %(n_boletas_acumulado)20s %(n_boletas)20s %(pagina_sig_codigo)20s'
    filename = ''

    def __init__(self):
            self.__start_console_log()

    def __start_console_log(self):
        print(self.log_console_mask % {
            'pagina': 'Página',
            'n_boletas_pagina': 'Boletas por Página',
            'n_boletas_acumulado': 'Boletas Acumuladas',
            'n_boletas': 'Cantidad Total',
            'pagina_sig_codigo': 'Código Siguiente',
        })

    def __log_console(self, _log):
        log = copy.deepcopy(_log)
        print(self.log_console_mask % log)

    def write(self, log):
        # guardar logs
        self.logs.append(log)
        self.__log_console(log)

    def save_to_files(self, receptor_rut, periodo, listado_bhe):
        # guardar logs como CSV
        # guardar boletas en archivo
        self.filename = '%(receptor)s_bhe_%(periodo)s.json' % {
            'receptor': receptor_rut,
            'periodo': str(periodo),
        }
        # guardar logs como JSON
        dict_save_to_json( self.filename, listado_bhe)
        # resultado
        print('Se guardaron %(n_boletas)s en el archivo %(filename)s del periodo %(periodo)s' % {
            'n_boletas': len(listado_bhe),
            'filename': self.filename,
            'periodo': periodo
        })


# clase para excepciones del test
class TestException(Exception):
    pass

# clase que ejecuta el test
class Test:
    # config inicial
    boletas = []
    pagina = 1
    pagina_sig_codigo = '00000000000000'

    def __init__(self, receptor_rut, receptor_clave, periodo):
        # crear cliente de la API
        self.receptor_rut = receptor_rut
        self.log = TestLog()
        self.bhe = BheRecibidas(receptor_rut, receptor_clave)
        self.periodo = periodo

    # método para obtener el listado de boletas
    def obtener_bhe_recibidas(self):
        # iteración
        listado_bhe = []
        n_boletas_acumulado = 0
        while True:
            documentos = self.bhe.documentos(self.receptor_rut, self.periodo, pagina = self.pagina, pagina_sig_codigo = self.pagina_sig_codigo)
            if documentos['pagina_sig_codigo'] in ('00000000000000'):
                break
            self.pagina_sig_codigo = documentos['pagina_sig_codigo']
            # guardar el listado completo de boletas
            listado_bhe = listado_bhe + documentos['boletas']
            n_boletas_acumulado += len(documentos['boletas'])
            log = {
                'pagina': self.pagina,
                'n_boletas_pagina': len(documentos['boletas']),
                'n_boletas_acumulado': n_boletas_acumulado,
                'n_boletas': documentos['n_boletas'],
                'pagina_sig_codigo': documentos['pagina_sig_codigo'],
            }
            self.pagina += 1
            self.log.write(log)
        # guardar logs en los archivos
        self.log.save_to_files(self.receptor_rut, self.periodo, listado_bhe)
        return listado_bhe, self.log.filename

def usage(message = None):
    print("\n" + 'APIGATEWAY: Tester', end="\n\n")
    if message is not None:
        print('[error] ' + message, end="\n\n")
    sys.exit(0)

# ejecutar el test si este archivo es el principal de la ejecución
if __name__ == '__main__':
    try:
        # datos del receptor
        RECEPTOR_RUT = os.getenv('APIGATEWAY_TESTS_EMPRESA_RUT', '')
        RECEPTOR_CLAVE = os.getenv('APIGATEWAY_TESTS_EMPRESA_CLAVE', '')
        PERIODO = 202308
        test = Test(RECEPTOR_RUT, RECEPTOR_CLAVE, PERIODO)
        test.obtener_bhe_recibidas()
    except KeyboardInterrupt:
        print('Se interrumpió la ejecución del programa.')
        sys.exit(0)
    except TestException as e:
        usage(str(e))
        sys.exit(1)
