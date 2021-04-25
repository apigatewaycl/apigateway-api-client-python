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

from os import getenv
import requests
import json

from .exceptions import LibreDTEApiException


"""
Clase con las funcionalidades para integrar con la API de LibreDTE
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2021-04-25
"""
class LibreDTE:

    DEFAULT_URL = 'https://api.libredte.cl'
    DEFAULT_VERSION = 'v1'

    def __init__(self, token = None, url = None, version = None):
        """Constructor de la clase LibreDTE
        :param token: Access Token de autenticación del usuario
        :param url: Host con la dirección web base de LibreDTE
        :param version: Versión de la API que se está usando
        """
        # validar token
        if token is not None:
            self.token = str(token).strip()
        else:
            self.token = str(getenv('LIBREDTE_API_TOKEN')).strip()
        if self.token == '':
            raise LibreDTEApiException('LIBREDTE_API_TOKEN missing')
        # validar url
        if url is not None:
            self.url = str(url).strip()
        else:
            self.url = str(getenv('LIBREDTE_API_URL', self.DEFAULT_URL)).strip()
        if self.url == '':
            raise LibreDTEApiException('LIBREDTE_API_URL missing')
        # asignar cabecera y versión
        self.headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + self.token
        }
        self.version = version if version is not None else self.DEFAULT_VERSION

    def get(self, resource, headers = {}, method = 'GET'):
        """Método que consume un servicio web de LibreDTE a través de GET
        :param resource: Recurso de la API que se desea consumir (sin /api)
        :param headers: cabeceras adicionales o que reemplazan las por defecto
        :param method: parámetro para uso privado
        """
        headers = {**self.headers, **headers}
        uri = self.url + '/api/' + self.version + resource
        if method == 'GET':
            r = requests.get(uri, headers=headers)
        elif method == 'DELETE':
            r = requests.delete(uri, headers=headers)
        else:
            raise LibreDTEApiException('Método ' + method + ' no soportado')
        return self._check_and_return_response(r)

    def delete(self, resource, headers = {}):
        """Método que consume un servicio web de LibreDTE a través de DELETE
        :param resource: Recurso de la API que se desea consumir (sin /api)
        :param headers: cabeceras adicionales o que reemplazan las por defecto
        """
        return self.get(resource, headers, 'DELETE')

    def post(self, resource, data = None, headers = {}, method = 'POST'):
        """Método que consume un servicio web de LibreDTE a través de POST
        :param resource: Recurso de la API que se desea consumir (sin /api)
        :param data: Datos que se codificarán como JSON y se enviarán al recurso
        :param headers: cabeceras adicionales o que reemplazan las por defecto
        :param method: parámetro para uso privado
        """
        if isinstance(data, str):
            payload = data
        else :
            payload = json.dumps(data)
        headers = {**self.headers, **headers}
        uri = self.url + '/api/' + self.version + resource
        if method == 'POST':
            r = requests.post(uri, data=payload, headers=headers)
        elif method == 'PUT':
            r = requests.put(uri, data=payload, headers=headers)
        else:
            raise LibreDTEApiException('Método ' + method + ' no soportado')
        return self._check_and_return_response(r)

    def put(self, resource, data = None, headers = {}):
        """Método que consume un servicio web de LibreDTE a través de POST
        :param resource: Recurso de la API que se desea consumir (sin /api)
        :param data: Datos que se codificarán como JSON y se enviarán al recurso
        :param headers: cabeceras adicionales o que reemplazan las por defecto
        """
        return self.post(resource, data, headers, 'PUT')

    def _check_and_return_response(self, response):
        """Método privado que valida la respuesta HTTP para verificar si hubo errores
        :param response: respuesta de requests que se valida antes de ser entregada
        """
        if response.status_code != 200:
            error = response.json()
            if 'message' in error and error['message'] != '':
                message = error['message']
            elif 'exception' in error and error['exception'] != '':
                message = error['exception']
            else:
                message = 'Ocurrió un error inesperado (sin mensaje ni excepción)'
            raise LibreDTEApiException(message)
        return response
