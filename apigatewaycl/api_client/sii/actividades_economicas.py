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
Módulo para obtener las actividades económicas del SII.

Para más información sobre la API, consulte la `documentación completa de Actividades Económicas <https://developers.apigateway.cl/#e64eb128-173a-48c7-ab0b-b6152e59c327>`_.
'''

from .. import ApiBase

class ActividadesEconomicas(ApiBase):
    '''
    Cliente específico para interactuar con los endpoints de actividades económicas de la API de API Gateway.

    Provee métodos para obtener listados de actividades económicas, tanto de primera como de segunda categoría.
    '''

    def listado(self, categoria = None):
        '''
        Obtiene un listado de actividades económicas. Puede filtrar por categoría.

        :param int categoria: Categoría de las actividades económicas (opcional).
        :return: Respuesta JSON con el listado de actividades económicas.
        :rtype: list[dict]
        '''
        url = '/sii/contribuyentes/actividades_economicas'
        if categoria is not None:
            url += '/%(categoria)s' % {'categoria': categoria}
        response = self.client.retry_request_http('GET', url)
        return response.json()

    def listado_primera_categoria(self):
        '''
        Obtiene un listado de actividades económicas de primera categoría.

        :return: Respuesta JSON con el listado de actividades económicas de primera categoría.
        :rtype: list[dict]
        '''
        return self.listado(1)

    def listado_segunda_categoria(self):
        '''
        Obtiene un listado de actividades económicas de segunda categoría.

        :return: Respuesta JSON con el listado de actividades económicas de segunda categoría.
        :rtype: list[dict]
        '''
        return self.listado(2)
