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
Módulo para interactuar con las opciones de Documentos Tributarios Electrónicos (DTE) del SII.

Para más información sobre la API, consulte la `documentación completa de los DTE <https://developers.apigateway.cl/#8c113b9a-ea05-4981-9273-73e3f20ef991>`_.
'''

from .. import ApiBase

class Contribuyentes(ApiBase):
    '''
    Cliente específico para interactuar con los endpoints de contribuyentes de la API de API Gateway.

    Proporciona métodos para consultar la autorización de emisión de DTE de un contribuyente.
    '''

    def autorizacion(self, rut, certificacion = None):
        '''
        Verifica si un contribuyente está autorizado para emitir DTE.

        :param str rut: RUT del contribuyente a verificar.
        :param bool certificacion: Indica si se consulta en ambiente de certificación (opcional).
        :return: Respuesta JSON con el estado de autorización del contribuyente.
        :rtype: dict
        '''
        certificacion_flag = 1 if certificacion else 0
        url = '/sii/dte/contribuyentes/autorizado/%(rut)s?certificacion=%(certificacion_flag)s' % {
            'rut': rut, 'certificacion_flag': certificacion_flag
        }
        response = self.client.retry_request_http('GET', url)
        return response.json()

class Emitidos(ApiBase):
    '''
    Cliente específico para gestionar DTE emitidos.

    Permite verificar la validez y autenticidad de un DTE emitido.

    :param str usuario_rut: RUT del usuario.
    :param str usuario_clave: Clave del usuario.
    :param kwargs: Argumentos adicionales.
    '''

    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super().__init__(usuario_rut = usuario_rut, usuario_clave = usuario_clave, **kwargs)

    def verificar(self, emisor, receptor, dte, folio, fecha, total, firma = None, certificacion = None):
        '''
        Verifica la validez de un DTE emitido.

        :param str emisor: RUT del emisor del DTE.
        :param str receptor: RUT del receptor del DTE.
        :param int dte: Tipo de DTE.
        :param int folio: Número de folio del DTE.
        :param str fecha: Fecha de emisión del DTE.
        :param int total: Monto total del DTE.
        :param str firma: Firma electrónica del DTE (opcional).
        :param bool certificacion: Indica si la verificación es en ambiente de certificación (opcional).
        :return: Respuesta JSON con el resultado de la verificación del DTE.
        :rtype: dict
        '''
        certificacion_flag = 1 if certificacion else 0
        url = '/sii/dte/emitidos/verificar?certificacion=%(certificacion_flag)s' % {'certificacion_flag': certificacion_flag}
        body = {
            'auth': self._get_auth_pass(),
            'dte': {
                'emisor': emisor,
                'receptor': receptor,
                'dte': dte,
                'folio': folio,
                'fecha': fecha,
                'total': total,
                'firma': firma
            }
        }
        response = self.client.retry_request_http('POST', url, data = body)
        return response.json()
