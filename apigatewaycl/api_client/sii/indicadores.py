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
Módulo para obtener indicadores desde el SII.

Para más información sobre la API, consulte la `documentación completa de los Indicadores <https://developers.apigateway.cl/#65aa568c-4c5a-448b-9f3b-95c3d9153e4d>`_.
'''

from .. import ApiBase

class Uf(ApiBase):
    '''
    Cliente específico para interactuar con los endpoints de valores de UF (Unidad de Fomento) de la API de API Gateway.

    Provee métodos para obtener valores de UF anuales, mensuales y diarios.
    '''

    def anual(self, anio):
        '''
        Obtiene los valores de la UF para un año específico.

        :param int anio: Año para el cual se quieren obtener los valores de la UF.
        :return: Respuesta JSON con los valores de la UF del año especificado.
        :rtype: dict
        '''
        anio = str(anio)
        url = '/sii/indicadores/uf/anual/%(anio)s' % {'anio': anio}
        response = self.client.retry_request_http('GET', url)
        datos = response.json()
        return datos[anio] if anio in datos else {}

    def mensual(self, periodo):
        '''
        Obtiene los valores de la UF para un mes específico.

        :param str periodo: Período en formato AAAAMM (año y mes).
        :return: Respuesta JSON con los valores de la UF del mes especificado.
        :rtype: dict
        '''
        anio, mes = periodo[:4], periodo[4:6]
        url = '/sii/indicadores/uf/anual/%(anio)s/%(mes)s' % {'anio': anio, 'mes': mes}
        response = self.client.retry_request_http('GET', url)
        datos = response.json()
        return datos[periodo] if periodo in datos else {}

    def diario(self, dia):
        '''
        Obtiene el valor de la UF para un día específico.

        :param str dia: Fecha en formato AAAA-MM-DD.
        :return: Valor de la UF para el día especificado.
        :rtype: float
        '''
        anio, mes, dia = dia.split('-')
        url = '/sii/indicadores/uf/anual/%(anio)s/%(mes)s/%(dia)s' % {'anio': anio, 'mes': mes, 'dia': dia}
        response = self.client.retry_request_http('GET', url)
        datos = response.json()
        key = '%(anio)s%(mes)s%(dia)s' % {'anio': anio, 'mes': mes, 'dia': dia}
        return float(datos[key]) if key in datos else 0
