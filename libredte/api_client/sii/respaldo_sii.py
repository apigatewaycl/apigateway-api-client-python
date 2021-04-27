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

import datetime
import pathlib
import os

from sasco_utils.datetime import period_range, period_first_day, period_last_day, period_current, period_previous
from sasco_utils.dict import dict_save_to_csv, dict_load_from_csv

from ..exceptions import LibreDTEApiException
from .portal_mipyme import DteEmitidos, DteRecibidos
from .rcv import Rcv
from .bhe import BheRecibidas
from .bte import BteEmitidas


class RespaldoSii:

    DEFAULT_RESPALDAR = {
        'mipyme': ['csv', 'xml', 'pdf'],
        'rcv': ['csv_compras_resumen', 'csv_compras_detalle', 'csv_ventas_resumen', 'csv_ventas_detalle'],
        'bhe': ['csv', 'pdf'],
        'bte': ['csv', 'html'],
    }
    DEFAULT_ITERACIONES = 10
    DEFAULT_DELIMITER = ';'

    def __init__(self, **kwargs):
        self.empresa_rut = kwargs.get('empresa_rut')
        self.empresa_clave = kwargs.get('empresa_clave')
        self.usuario_rut = kwargs.get('usuario_rut') if kwargs.get('usuario_rut') is not None else self.empresa_rut
        self.usuario_clave = kwargs.get('usuario_clave') if kwargs.get('usuario_clave') is not None else self.empresa_clave
        self.periodo_desde = int(
            kwargs.get('periodo_desde') if kwargs.get('periodo_desde') is not None else datetime.date.today().strftime('%Y%m')
        )
        self.periodo_hasta = int(
            kwargs.get('periodo_hasta') if kwargs.get('periodo_hasta') is not None else self.periodo_desde
        )
        self.respaldar = kwargs.get('respaldar')
        if self.respaldar is None:
            self.respaldar = self.DEFAULT_RESPALDAR
        elif isinstance(self.respaldar, str):
            self.respaldar = self.respaldar.split(',')
            respaldar = {}
            for respaldo in self.respaldar:
                try:
                    respaldar[respaldo] = self.DEFAULT_RESPALDAR[respaldo]
                except KeyError:
                    self._send_message('ERROR Tipo de respaldo %(respaldo)s no existe. Los disponibles son: %(respaldos)s' % {
                        'respaldo': respaldo,
                        'respaldos': ', '.join(list(self.DEFAULT_RESPALDAR.keys())),
                    })
            self.respaldar = respaldar
        self.directorio_salida = kwargs.get('directorio_salida')
        if self.directorio_salida is None:
            self.directorio_salida = os.path.join(str(pathlib.Path.home()), 'Descargas', 'respaldo_sii_' + self.empresa_rut)
        if not os.path.exists(self.directorio_salida) :
            os.makedirs(self.directorio_salida)
        self.iteraciones = kwargs.get('iteraciones') if kwargs.get('iteraciones') is not None else self.DEFAULT_ITERACIONES
        self.csv_delimiter = kwargs.get('csv_delimiter') if kwargs.get('csv_delimiter') is not None else self.DEFAULT_DELIMITER
        self.periodos_forzar_descarga_csv = kwargs.get('periodos_forzar_descarga_csv')
        if self.periodos_forzar_descarga_csv is None:
            self.periodos_forzar_descarga_csv = [period_current(), period_previous()]
        self.callback_log = kwargs.get('callback_log') if kwargs.get('callback_log') is not None else self._default_log

    def generar(self):
        # crear directorios que se usarán para el respaldo
        for respaldo in self.respaldar:
            if not os.path.exists(os.path.join(self.directorio_salida, respaldo)):
                os.makedirs(os.path.join(self.directorio_salida, respaldo))
        # armar periodos que se usarán para el respaldo
        periodos = period_range(self.periodo_desde, self.periodo_hasta)
        # revisar credenciales
        if self.usuario_rut is None:
            self._send_message('ERROR Debe especificar usuario_rut')
            return False
        if self.usuario_clave is None:
            self._send_message('ERROR Debe especificar usuario_clave')
            return False
        # ejecutar respaldo por cada período
        estado_respaldos = {}
        for i in range(self.iteraciones):
            self.iteracion = i+1
            # ejecutar respaldo por período y tipo de respaldo solicitado
            for periodo in periodos:
                for respaldo in self.respaldar:
                    ok = getattr(self, '_generar_' + respaldo)(periodo)
                    if not ok:
                        estado_respaldos[respaldo] = False
            # si todo fue ok con todos los respaldos terminamos las iteraciones
            estados_mal = sum(list(map(lambda x: 0 if estado_respaldos[x] is True else 1, estado_respaldos)))
            if estados_mal == 0:
                break
            if self.iteracion < self.iteraciones:
                for respaldo in self.respaldar:
                    estado_respaldos[respaldo] = True
        estados_mal = sum(list(map(lambda x: 0 if estado_respaldos[x] is True else 1, estado_respaldos)))
        return True if estados_mal == 0 else False

    def _generar_mipyme(self, periodo):
        ok = True
        dte_emitidos = DteEmitidos(self.usuario_rut, self.usuario_clave)
        dte_recibidos = DteRecibidos(self.usuario_rut, self.usuario_clave)
        filtros = {'FEC_DESDE': period_first_day(periodo), 'FEC_HASTA': period_last_day(periodo)}
        # documentos emitidos en el portal mipyme
        if 'csv' in self.respaldar['mipyme'] or 'xml' in self.respaldar['mipyme'] or 'pdf' in self.respaldar['mipyme']:
            # obtener listado de documentos emitidos
            self._send_message('GET %(periodo)s mipyme dte_emitidos' % {
                'periodo': periodo
            })
            filename = 'mipyme_%(periodo)s_dte_emitidos.csv' % {'periodo': periodo}
            filepath = os.path.join(self.directorio_salida, 'mipyme', filename)
            if not os.path.exists(filepath) or periodo in self.periodos_forzar_descarga_csv:
                try:
                    documentos = dte_emitidos.documentos(self.empresa_rut, filtros)
                    if 'csv' in self.respaldar['mipyme']:
                        dict_save_to_csv(filepath, documentos, delimiter = self.csv_delimiter)
                except LibreDTEApiException as e:
                    self._send_message('ERROR %(periodo)s mipyme dte_emitidos: %(error)s' % {
                        'periodo': periodo,
                        'error': str(e)
                    })
                    documentos = []
                    ok = False
            else:
                documentos = dict_load_from_csv(filepath, delimiter = self.csv_delimiter)
            # iterar documentos si se requiere XML o PDF
            if 'xml' in self.respaldar['mipyme'] or 'pdf' in self.respaldar['mipyme']:
                for documento in documentos:
                    # obtener XML de los documentos emitidos
                    if 'xml' in self.respaldar['mipyme']:
                        self._send_message('GET %(periodo)s mipyme dte_emitido xml T%(dte)sF%(folio)s' % {
                            'periodo': periodo,
                            'dte': documento['dte'],
                            'folio': documento['folio'],
                        })
                        filename = 'mipyme_%(periodo)s_dte_emitido_T%(dte)sF%(folio)s.xml' % {
                            'periodo': str(periodo),
                            'dte': documento['dte'],
                            'folio': documento['folio'],
                        }
                        filepath = os.path.join(self.directorio_salida, 'mipyme', filename)
                        if not os.path.exists(filepath):
                            try:
                                xml = dte_emitidos.xml(self.empresa_rut, documento['dte'], documento['folio'])
                                with open(filepath, 'w') as f:
                                    f.write(xml)
                            except LibreDTEApiException as e:
                                self._send_message('ERROR %(periodo)s mipyme dte_emitido xml T%(dte)sF%(folio)s: %(error)s' % {
                                    'periodo': periodo,
                                    'dte': documento['dte'],
                                    'folio': documento['folio'],
                                    'error': str(e)
                                })
                                ok = False
                    # obtener PDF de los documentos emitidos
                    if 'pdf' in self.respaldar['mipyme']:
                        self._send_message('GET %(periodo)s mipyme dte_emitido pdf T%(dte)sF%(folio)s' % {
                            'periodo': periodo,
                            'dte': documento['dte'],
                            'folio': documento['folio'],
                        })
                        filename = 'mipyme_%(periodo)s_dte_emitido_T%(dte)sF%(folio)s.pdf' % {
                            'periodo': str(periodo),
                            'dte': documento['dte'],
                            'folio': documento['folio'],
                        }
                        filepath = os.path.join(self.directorio_salida, 'mipyme', filename)
                        if not os.path.exists(filepath):
                            try:
                                pdf = dte_emitidos.pdf(self.empresa_rut, documento['codigo'])
                                with open(filepath, 'wb') as f:
                                    f.write(pdf)
                            except LibreDTEApiException as e:
                                self._send_message('ERROR %(periodo)s mipyme dte_emitido pdf T%(dte)sF%(folio)s: %(error)s' % {
                                    'periodo': periodo,
                                    'dte': documento['dte'],
                                    'folio': documento['folio'],
                                    'error': str(e)
                                })
                                ok = False
        # documentos recibidos en el portal mipyme
        if 'csv' in self.respaldar['mipyme'] or 'xml' in self.respaldar['mipyme'] or 'pdf' in self.respaldar['mipyme']:
            # obtener listado de documentos recibidos
            self._send_message('GET %(periodo)s mipyme dte_recibidos' % {
                'periodo': periodo
            })
            filename = 'mipyme_%(periodo)s_dte_recibidos.csv' % {'periodo': periodo}
            filepath = os.path.join(self.directorio_salida, 'mipyme', filename)
            if not os.path.exists(filepath) or periodo in self.periodos_forzar_descarga_csv:
                try:
                    documentos = dte_recibidos.documentos(self.empresa_rut, filtros)
                    if 'csv' in self.respaldar['mipyme']:
                        dict_save_to_csv(filepath, documentos, delimiter = self.csv_delimiter)
                except LibreDTEApiException as e:
                    self._send_message('ERROR %(periodo)s mipyme dte_recibidos: %(error)s' % {
                        'periodo': periodo,
                        'error': str(e)
                    })
                    documentos = []
                    ok = False
            else:
                documentos = dict_load_from_csv(filepath, delimiter = self.csv_delimiter)
            # iterar documentos si se requiere XML o PDF
            if 'xml' in self.respaldar['mipyme'] or 'pdf' in self.respaldar['mipyme']:
                for documento in documentos:
                    # obtener XML de los documentos recibidos
                    if 'xml' in self.respaldar['mipyme']:
                        self._send_message('GET %(periodo)s mipyme dte_recibido xml %(rut)s-%(dv)s T%(dte)sF%(folio)s' % {
                            'periodo': periodo,
                            'rut': documento['rut'],
                            'dv': documento['dv'],
                            'dte': documento['dte'],
                            'folio': documento['folio'],
                        })
                        filename = 'mipyme_%(periodo)s_dte_recibido_%(rut)s-%(dv)s_T%(dte)sF%(folio)s.xml' % {
                            'periodo': str(periodo),
                            'rut': documento['rut'],
                            'dv': documento['dv'],
                            'dte': documento['dte'],
                            'folio': documento['folio'],
                        }
                        filepath = os.path.join(self.directorio_salida, 'mipyme', filename)
                        if not os.path.exists(filepath):
                            try:
                                xml = dte_recibidos.xml(self.empresa_rut, documento['rut'] + '-' + documento['dv'], documento['dte'], documento['folio'])
                                with open(filepath, 'w') as f:
                                    f.write(xml)
                            except LibreDTEApiException as e:
                                self._send_message('ERROR %(periodo)s mipyme dte_recibido xml %(rut)s-%(dv)s T%(dte)sF%(folio)s: %(error)s' % {
                                    'periodo': periodo,
                                    'rut': documento['rut'],
                                    'dv': documento['dv'],
                                    'dte': documento['dte'],
                                    'folio': documento['folio'],
                                    'error': str(e)
                                })
                                ok = False
                    # obtener PDF de los documentos recibidos
                    if 'pdf' in self.respaldar['mipyme']:
                        self._send_message('GET %(periodo)s mipyme dte_recibido pdf %(rut)s-%(dv)s T%(dte)sF%(folio)s' % {
                            'periodo': periodo,
                            'rut': documento['rut'],
                            'dv': documento['dv'],
                            'dte': documento['dte'],
                            'folio': documento['folio'],
                        })
                        filename = 'mipyme_%(periodo)s_dte_recibido_%(rut)s-%(dv)s_T%(dte)sF%(folio)s.pdf' % {
                            'periodo': str(periodo),
                            'rut': documento['rut'],
                            'dv': documento['dv'],
                            'dte': documento['dte'],
                            'folio': documento['folio'],
                        }
                        filepath = os.path.join(self.directorio_salida, 'mipyme', filename)
                        if not os.path.exists(filepath):
                            try:
                                pdf = dte_recibidos.pdf(self.empresa_rut, documento['rut'] + '-' + documento['dv'], documento['codigo'])
                                with open(filepath, 'wb') as f:
                                    f.write(pdf)
                            except LibreDTEApiException as e:
                                self._send_message('ERROR %(periodo)s mipyme dte_recibido pdf %(rut)s-%(dv)s T%(dte)sF%(folio)s: %(error)s' % {
                                    'periodo': periodo,
                                    'rut': documento['rut'],
                                    'dv': documento['dv'],
                                    'dte': documento['dte'],
                                    'folio': documento['folio'],
                                    'error': str(e)
                                })
                                ok = False
        # entregar estado para saber si se debe volver a revisar este período
        return ok

    def _generar_rcv(self, periodo):
        ok = True
        if self.empresa_clave is not None:
            rcv = Rcv(self.empresa_rut, self.empresa_clave)
        else:
            rcv = Rcv(self.usuario_rut, self.usuario_clave)
        # no es posible respaldar previo a agosto de 2017 (no existía el RCV)
        if periodo < 201708:
            return ok
        # generar respaldo compras
        if 'csv_compras_resumen' in self.respaldar['rcv'] or 'csv_compras_detalle' in self.respaldar['rcv']:
            try:
                # obtener resumen de compras
                self._send_message('GET %(periodo)s rcv compras resumen' % {
                    'periodo': periodo
                })
                filename = 'rcv_%(periodo)s_compras_resumen.csv' % {'periodo': periodo}
                filepath = os.path.join(self.directorio_salida, 'rcv', filename)
                if not os.path.exists(filepath) or periodo in self.periodos_forzar_descarga_csv:
                    resumen = rcv.compras_resumen(self.empresa_rut, periodo)
                    if 'csv_compras_resumen' in self.respaldar['rcv']:
                        dict_save_to_csv(filepath, resumen, delimiter = self.csv_delimiter)
                else:
                    resumen = dict_load_from_csv(filepath, delimiter = self.csv_delimiter)
                # obtener detalle de compras
                if 'csv_compras_detalle' in self.respaldar['rcv']:
                    self._send_message('GET %(periodo)s rcv compras detalle' % {
                        'periodo': periodo
                    })
                    filename = 'rcv_%(periodo)s_compras_detalle.csv' % {'periodo': periodo}
                    filepath = os.path.join(self.directorio_salida, 'rcv', filename)
                    if not os.path.exists(filepath) or periodo in self.periodos_forzar_descarga_csv:
                        documentos = []
                        for r in resumen:
                            if r['rsmnTotDoc'] > 0:
                                documentos.append(r['rsmnTipoDocInteger'])
                        detalle = rcv.compras_detalle(self.empresa_rut, periodo, ','.join(map(str, documentos)))
                        dict_save_to_csv(filepath, detalle, delimiter = self.csv_delimiter)
            except LibreDTEApiException as e:
                self._send_message('ERROR %(periodo)s rcv compras: %(error)s' % {
                    'periodo': periodo,
                    'error': str(e)
                })
                ok = False
        # generar respaldo ventas
        if 'csv_ventas_resumen' in self.respaldar['rcv'] or 'csv_ventas_detalle' in self.respaldar['rcv']:
            try:
                # descargar resumen ventas
                self._send_message('GET %(periodo)s rcv ventas resumen' % {
                    'periodo': periodo
                })
                filename = 'rcv_%(periodo)s_ventas_resumen.csv' % {'periodo': periodo}
                filepath = os.path.join(self.directorio_salida, 'rcv', filename)
                if not os.path.exists(filepath) or periodo in self.periodos_forzar_descarga_csv:
                    resumen = rcv.ventas_resumen(self.empresa_rut, periodo)
                    if 'csv_ventas_resumen' in self.respaldar['rcv']:
                        dict_save_to_csv(filepath, resumen, delimiter = self.csv_delimiter)
                else:
                    resumen = dict_load_from_csv(filepath, delimiter = self.csv_delimiter)
                # descargar detalle ventas
                if 'csv_ventas_detalle' in self.respaldar['rcv']:
                    self._send_message('GET %(periodo)s rcv ventas detalle' % {
                        'periodo': periodo
                    })
                    filename = 'rcv_%(periodo)s_ventas_detalle.csv' % {'periodo': str(periodo)}
                    filepath = os.path.join(self.directorio_salida, 'rcv', filename)
                    if not os.path.exists(filepath) or periodo in self.periodos_forzar_descarga_csv:
                        documentos = []
                        for r in resumen:
                            if r['rsmnTotDoc'] > 0:
                                documentos.append(r['rsmnTipoDocInteger'])
                        detalle = rcv.ventas_detalle(self.empresa_rut, periodo, ','.join(map(str, documentos)))
                        dict_save_to_csv(filepath, detalle, delimiter = self.csv_delimiter)
            except LibreDTEApiException as e:
                self._send_message('ERROR %(periodo)s rcv ventas: %(error)s' % {
                    'periodo': periodo,
                    'error': str(e)
                })
                ok = False
        # entregar estado para saber si se debe volver a revisar este período
        return ok

    def _generar_bhe(self, periodo):
        ok = True
        bhe = BheRecibidas(self.empresa_rut, self.empresa_clave)
        # descargar detalle de boletas
        self._send_message('GET %(periodo)s bhe documentos' % {
            'periodo': periodo
        })
        filename = 'bhe_%(periodo)s.csv' % {'periodo': str(periodo)}
        filepath = os.path.join(self.directorio_salida, 'bhe', filename)
        if not os.path.exists(filepath) or periodo in self.periodos_forzar_descarga_csv:
            try:
                documentos = bhe.documentos(self.empresa_rut, periodo)
                if 'csv' in self.respaldar['bhe']:
                    dict_save_to_csv(filepath, documentos, delimiter = self.csv_delimiter)
            except LibreDTEApiException as e:
                self._send_message('ERROR %(periodo)s bhe documentos: %(error)s' % {
                    'periodo': periodo,
                    'error': str(e)
                })
                documentos = []
                ok = False
        else:
            documentos = dict_load_from_csv(filepath, delimiter = self.csv_delimiter)
        # descargar PDF de boletas
        if 'pdf' in self.respaldar['bhe']:
            for documento in documentos:
                if documento['anulada'] != '':
                    continue
                self._send_message('GET %(periodo)s bhe pdf %(rut)s-%(dv)s %(numero)s' % {
                    'periodo': periodo,
                    'rut': documento['rut'],
                    'dv': documento['dv'],
                    'numero': documento['numero'],
                })
                filename = 'bhe_%(periodo)s_%(codigo)s.pdf' % {
                    'periodo': str(periodo),
                    'codigo': documento['codigo'],
                }
                filepath = os.path.join(self.directorio_salida, 'bhe', filename)
                if not os.path.exists(filepath):
                    try:
                        pdf = bhe.pdf(documento['codigo'])
                        with open(filepath, 'wb') as f:
                            f.write(pdf)
                    except LibreDTEApiException as e:
                        self._send_message('ERROR %(periodo)s bhe pdf %(rut)s-%(dv)s %(numero)s: %(error)s' % {
                            'periodo': periodo,
                            'rut': documento['rut'],
                            'dv': documento['dv'],
                            'numero': documento['numero'],
                            'error': str(e)
                        })
                        ok = False
        # entregar estado para saber si se debe volver a revisar este período
        return ok

    def _generar_bte(self, periodo):
        ok = True
        bte = BteEmitidas(self.empresa_rut, self.empresa_clave)
        # descargar detalle de boletas
        self._send_message('GET %(periodo)s bte documentos' % {
            'periodo': periodo
        })
        filename = 'bte_%(periodo)s.csv' % {'periodo': str(periodo)}
        filepath = os.path.join(self.directorio_salida, 'bte', filename)
        if not os.path.exists(filepath) or periodo in self.periodos_forzar_descarga_csv:
            try:
                documentos = bte.documentos(self.empresa_rut, periodo)
                if 'csv' in self.respaldar['bte']:
                    dict_save_to_csv(filepath, documentos, delimiter = self.csv_delimiter)
            except LibreDTEApiException as e:
                self._send_message('ERROR %(periodo)s bte documentos: %(error)s' % {
                    'periodo': periodo,
                    'error': str(e)
                })
                documentos = []
                ok = False
        else:
            documentos = dict_load_from_csv(filepath, delimiter = self.csv_delimiter)
        # descargar HTML de boletas
        if 'html' in self.respaldar['bte']:
            for documento in documentos:
                if documento['estado'] == 'ANUL':
                    continue
                self._send_message('GET %(periodo)s bte html %(numero)s' % {
                    'periodo': periodo,
                    'numero': documento['numero'],
                })
                filename = 'bte_%(periodo)s_%(codigo)s.html' % {
                    'periodo': str(periodo),
                    'codigo': documento['codigo'],
                }
                filepath = os.path.join(self.directorio_salida, 'bte', filename)
                if not os.path.exists(filepath):
                    try:
                        html = bte.html(documento['codigo'])
                        with open(filepath, 'wb') as f:
                            f.write(html)
                    except LibreDTEApiException as e:
                        self._send_message('ERROR %(periodo)s bte html %(numero)s: %(error)s' % {
                            'periodo': periodo,
                            'numero': documento['numero'],
                            'error': str(e)
                        })
                        ok = False
        # entregar estado para saber si se debe volver a revisar este período
        return ok

    def _send_message(self, message):
        message = '%(iteracion)s %(message)s' % {
            'iteracion': self.iteracion,
            'message': message
        }
        self.callback_log(message)

    def _default_log(self, message):
        print(message)
