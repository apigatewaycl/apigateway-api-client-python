#
# API Gateway: Cliente de API en Python.
# Copyright (C) API Gateway <https://www.apigateway.cl>
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la GNU Lesser General Public License (LGPL) publicada
# por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
# o (a su elección) cualquier versión posterior de la misma.
#
# Este programa se distribuye con la esperanza de que sea útil, pero SIN
# GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
# PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
# Public License (LGPL) para obtener una información más detallada.
#
# Debería haber recibido una copia de la GNU Lesser General Public License
# (LGPL) junto a este programa. En caso contrario, consulte
# <http://www.gnu.org/licenses/lgpl.html>.
#

'''
Módulo para interactuar con el Registro de Compra y Venta del SII.

Para más información sobre la API, consulte la `documentación completa del RCV <https://developers.apigateway.cl/#ef1f7d54-2e86-4732-bb91-d3448b383d66>`_.
'''

from .. import ApiBase

class Rcv(ApiBase):
    '''
    Cliente específico para interactuar con los endpoints de Registro de Compras y Ventas (RCV) de la API de API Gateway.

    Proporciona métodos para obtener resúmenes y detalles de compras y ventas.

    :param str usuario_rut: RUT del usuario.
    :param str usuario_clave: Clave del usuario.
    :param kwargs: Argumentos adicionales.
    '''

    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super().__init__(usuario_rut = usuario_rut, usuario_clave = usuario_clave, **kwargs)

    def compras_resumen(self, receptor, periodo, estado = 'REGISTRO'):
        '''
        Obtiene un resumen de las compras registradas para un receptor en un periodo específico.

        :param str receptor: RUT del receptor de las compras.
        :param str periodo: Período de tiempo de las compras.
        :param str estado: Estado de las compras ('REGISTRO', 'PENDIENTE', 'NO_INCLUIR', 'RECLAMADO').
        :return: Respuesta JSON con el resumen de compras.
        :rtype: list[dict]
        '''
        url = '/sii/rcv/compras/resumen/%(receptor)s/%(periodo)s/%(estado)s' % {
            'receptor': receptor, 'periodo': periodo, 'estado': estado
        }
        body = {
            'auth': self._get_auth_pass()
        }
        response = self.client.retry_request_http('POST', url, data = body)
        return response.json()

    def compras_detalle(self, receptor, periodo, dte = 0, estado = 'REGISTRO', tipo = None):
        '''
        Obtiene detalles de las compras para un receptor en un periodo específico.

        :param str receptor: RUT del receptor de las compras.
        :param str periodo: Período de tiempo de las compras.
        :param int dte: Tipo de DTE.
        :param str estado: Estado de las compras ('REGISTRO', 'PENDIENTE', 'NO_INCLUIR', 'RECLAMADO').
        :param str tipo: Tipo de formato de respuesta ('rcv_csv' o 'rcv').
        :return: Respuesta JSON con detalles de las compras.
        :rtype: list[dict]
        '''
        url = '/sii/rcv/compras/detalle/%(receptor)s/%(periodo)s/%(dte)s/%(estado)s?tipo=%(tipo)s' % {
            'receptor': receptor, 'periodo': periodo, 'dte': dte, 'estado': estado, 'tipo': tipo
        }
        tipo = 'rcv_csv' if dte == 0 and estado == 'REGISTRO' else tipo or 'rcv'
        body = {
            'auth': self._get_auth_pass()
        }
        response = self.client.retry_request_http('POST', url, data = body)
        return response.json()

    def ventas_resumen(self, emisor, periodo):
        '''
        Obtiene un resumen de las ventas registradas para un emisor en un periodo específico.

        :param str emisor: RUT del emisor de las ventas.
        :param str periodo: Período de tiempo de las ventas.
        :return: Respuesta JSON con el resumen de ventas.
        :rtype: list[dict]
        '''
        url = '/sii/rcv/ventas/resumen/%(emisor)s/%(periodo)s' % {'emisor': emisor, 'periodo': periodo}
        body = {
            'auth': self._get_auth_pass()
        }
        response = self.client.retry_request_http('POST', url, data = body)
        return response.json()

    def ventas_detalle(self, emisor, periodo, dte = 0, tipo = None):
        '''
        Obtiene detalles de las ventas para un emisor en un periodo específico.

        :param str emisor: RUT del emisor de las ventas.
        :param str periodo: Período de tiempo de las ventas.
        :param int dte: Tipo de DTE.
        :param str tipo: Tipo de formato de respuesta ('rcv_csv' o 'rcv').
        :return: Respuesta JSON con detalles de las ventas.
        :rtype: list[dict]
        '''
        tipo = 'rcv_csv' if dte == 0 else tipo or 'rcv'
        url = '/sii/rcv/ventas/detalle/%(emisor)s/%(periodo)s/%(dte)s?tipo=%(tipo)s' % {
            'emisor': emisor, 'periodo': periodo, 'dte': dte, 'tipo': tipo
        }
        body = {
            'auth': self._get_auth_pass()
        }
        response = self.client.retry_request_http('POST', url, data = body)
        return response.json()
