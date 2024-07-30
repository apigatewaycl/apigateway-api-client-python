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
Módulo para interactuar con la sección MiSii de un contribuyente en el sitio web del SII.

Para más información sobre la API, consulte la `documentación completa de MiSii <https://developers.apigateway.cl/#b585f374-f106-46a9-9f47-666d478b8ac8>`_.
'''

from .. import ApiBase

class Contribuyente(ApiBase):
    '''
    Cliente específico para interactuar con los endpoints de un Contribuyente de MiSii de la API de API Gateway.

    Hereda de ApiBase y utiliza su funcionalidad para realizar solicitudes a la API.
    '''

    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super().__init__(usuario_rut = usuario_rut, usuario_clave = usuario_clave, **kwargs)

    def datos(self):
        '''
        Obtiene los datos de MiSii del contribuyente autenticado en el SII.

        :return: Respuesta JSON con los datos del contribuyente.
        :rtype: dict
        '''
        body = {
            'auth': self._get_auth_pass()
        }
        response = self.client.retry_request_http('post', '/sii/misii/contribuyente/datos', data = body)
        return response.json()
