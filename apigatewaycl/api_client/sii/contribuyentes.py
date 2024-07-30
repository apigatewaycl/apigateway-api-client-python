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
Módulo para obtener datos de los contribuyentes a través del SII.

Para más información sobre la API, consulte la `documentación completa de los Contribuyentes <https://developers.apigateway.cl/#c88f90b6-36bb-4dc2-ba93-6e418ff42098>`_.
'''

from .. import ApiBase

class Contribuyentes(ApiBase):
    '''
    Cliente específico para interactuar con los endpoints de contribuyentes de la API de API Gateway.

    Hereda de ApiBase y utiliza su funcionalidad para realizar solicitudes a la API.
    '''

    def situacion_tributaria(self, rut):
        '''
        Obtiene la situación tributaria de un contribuyente.

        :param str rut: RUT del contribuyente.
        :return: Respuesta JSON con la situación tributaria del contribuyente.
        :rtype: dict
        '''
        url = '/sii/contribuyentes/situacion_tributaria/tercero/%(rut)s' % {'rut': rut}
        response = self.client.retry_request_http('GET', url)
        return response.json()

    def verificar_rut(self, serie):
        '''
        Verifica el RUT de un contribuyente.

        :param str serie: Serie del RUT a verificar.
        :return: Respuesta JSON con la verificación del RUT.
        :rtype: dict
        '''
        url = '/sii/contribuyentes/rut/verificar/%(serie)s' % {'serie': serie}
        response = self.client.retry_request_http('GET', url)
        return response.json()
