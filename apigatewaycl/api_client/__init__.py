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

from os import getenv
import urllib.parse
from requests.exceptions import Timeout, ConnectionError, RequestException, HTTPError
import urllib
import re
import requests
import json
import time
from abc import ABC

class ApiClient:
    '''
    Cliente para interactuar con la API de API Gateway.

    :param str token: Token de autenticación del usuario. Si no se proporciona, se intentará obtener de una variable de entorno.
    :param str url: URL base de la API. Si no se proporciona, se usará una URL por defecto.
    :param str version: Versión de la API. Si no se proporciona, se usará una versión por defecto.
    :param bool raise_for_status: Si se debe lanzar una excepción automáticamente para respuestas de error HTTP. Por defecto es True.
    '''

    __DEFAULT_URL = 'https://apigateway.cl'
    __DEFAULT_VERSION = 'v1'

    def __init__(self, token = None, url = None, version = None, raise_for_status = True):
        self.token = self.__validate_token(token)
        self.url = self.__validate_url(url)
        self.headers = self.__generate_headers()
        self.version = version or self.__DEFAULT_VERSION
        self.raise_for_status = raise_for_status

    def __validate_token(self, token):
        '''
        Valida y retorna el token de autenticación.

        :param str token: Token de autenticación a validar.
        :return: Token validado.
        :rtype: str
        :raises ApiException: Si el token no es válido o está ausente.
        '''
        token = token or getenv('APIGATEWAY_API_TOKEN')
        if not token:
            raise ApiException('Se debe configurar la variable de entorno: APIGATEWAY_API_TOKEN.')
        return str(token).strip()

    def __validate_url(self, url):
        '''
        Valida y retorna la URL base para la API.

        :param str url: URL a validar.
        :return: URL validada.
        :rtype: str
        :raises ApiException: Si la URL no es válida o está ausente.
        '''
        return str(url).strip() if url else getenv('APIGATEWAY_API_URL', self.__DEFAULT_URL).strip()

    def __generate_headers(self):
        '''
        Genera y retorna las cabeceras por defecto para las solicitudes.

        :return: Cabeceras por defecto.
        :rtype: dict
        '''
        return {
            'User-Agent': 'API Gateway: Cliente de API en Python.',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer %(token)s' % {'token': self.token}
        }

    def get(self, resource, headers = None):
        '''
        Realiza una solicitud GET a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        '''
        return self.__request('GET', resource, headers = headers)

    def delete(self, resource, headers = None):
        '''
        Realiza una solicitud DELETE a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        '''
        return self.__request('DELETE', resource, headers = headers)

    def post(self, resource, data = None, headers = None):
        '''
        Realiza una solicitud POST a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        '''
        return self.__request('POST', resource, data, headers)

    def put(self, resource, data = None, headers = None):
        '''
        Realiza una solicitud PUT a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        '''
        return self.__request('PUT', resource, data, headers)

    def __request(self, method, resource, data = None, headers = None):
        '''
        Método privado para realizar solicitudes HTTP.

        :param str method: Método HTTP a utilizar.
        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud (opcional).
        :param dict headers: Cabeceras adicionales para la solicitud (opcional).
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        :raises ApiException: Si el método HTTP no es soportado o si hay un error de conexión.
        '''
        api_path = '/api/%(version)s%(resource)s' % {'version': self.version, 'resource': resource}
        full_url = urllib.parse.urljoin(self.url + '/', api_path.lstrip('/'))
        headers = headers or {}
        headers = {**self.headers, **headers}
        if data and not isinstance(data, str):
            data = json.dumps(data)
        try:
            response = requests.request(method, full_url, data = data, headers = headers)
            return self.__check_and_return_response(response)
        except ConnectionError as error:
            raise ApiException('Error de conexión: %(error)s' % {'error': error})
        except Timeout as error:
            raise ApiException('Error de timeout: %(error)s' % {'error': error})
        except RequestException as error:
            raise ApiException('Error en la solicitud: %(error)s' % {'error': error})

    def __check_and_return_response(self, response):
        '''
        Verifica la respuesta de la solicitud HTTP y maneja los errores.

        :param requests.Response response: Objeto de respuesta de requests.
        :return: Respuesta validada.
        :rtype: requests.Response
        :raises ApiException: Si la respuesta contiene un error HTTP.
        '''
        if response.status_code != 200 and self.raise_for_status:
            try:
                response.raise_for_status()
            except HTTPError as error:
                try:
                    error = response.json()
                    message = error.get('message', '') or error.get('exception', '') or 'Error desconocido.'
                except json.decoder.JSONDecodeError:
                    message = 'Error al decodificar los datos en JSON: %(response)s' % {'response': response.text}
                raise ApiException('Error HTTP: %(message)s' % {'message': message})
        return response

    def rebuild_url(self, url):
        '''
        Método que reconstruye una URL usando expresiones regulares (regex), añadiendo o
        quitando el parámetro 'auth_cache=0'.

        Se ha probado con los siguientes URL:
        - www.exampleurl.com/api/v1/function
        - www.exampleurl.com/api/v1/function?auth_cache=0
        - www.exampleurl.com/api/v1/function?auth_cache=0&param1=asdf
        - www.exampleurl.com/api/v1/function?param1=asdf&auth_cache=0
        - www.exampleurl.com/api/v1/function?param1=asdf&param2=qwer
        - www.exampleurl.com/api/v1/function?auth_cache=0&param1=asdf&param2=qwer
        - www.exampleurl.com/api/v1/function?param1=asdf&auth_cache=0&param2=qwer
        - www.exampleurl.com/api/v1/function?param1=asdf&param2=qwer&auth_cache=0

        Y se obtuvo como salida:
        - www.exampleurl.com/api/v1/function?auth_cache=0
        - www.exampleurl.com/api/v1/function
        - www.exampleurl.com/api/v1/function?param1=asdf
        - www.exampleurl.com/api/v1/function?param1=asdf
        - www.exampleurl.com/api/v1/function?param1=asdf&param2=qwer&auth_cache=0
        - www.exampleurl.com/api/v1/function?param1=asdf&param2=qwer
        - www.exampleurl.com/api/v1/function?param1=asdf&param2=qwer
        - www.exampleurl.com/api/v1/function?param1=asdf&param2=qwer

        :param str url: URL a modificar.
        :return: URL modificada con (o sin) 'auth_cache=0'.
        :rtype: str
        '''
        # Define un patrón, que en este caso serán todas las posibilidades con auth_cache=0.
        patron = r'([?&])auth_cache=0(&|$)'

        if re.search(patron, url):
            # Remueve el patrón definido.
            nuevo_url = re.sub(patron, lambda m: m.group(1) if m.group(2) == '&' else '', url)
        else:
            # Añade al URL auth_cache=0.
            nuevo_url = '%(url_base)s%(url_param)s' % { 'url_base' : url, 'url_param' : '&auth_cache=0' if '?' in url else '?auth_cache=0' }

        return nuevo_url

    def retry_request_http(self, method, url, data = None, headers = None):
        '''
        Método que reintenta un HTTP request en caso de que la conexión falle.

        Además, este método permitirá reintentar en caso de un error 401 a causa de una falla en el programa.

        :param str url: URL del recurso para consumir.
        :param dict data: Body del request (opcional).
        :param dict headers: Cabeceras adicionales (opcional).
        :param str method: Método HTTP a utilizar.
        :return: Respuesta lograda.
        :rtype: requests.Response
        :raises ApiException: Si el número de reintentos es excedido, o si el método ingresado no es válido.
        '''
        wait_time = 1
        n_max_attempts = 5
        n_current_attempts = 1

        while True:
            try:
                if method == 'POST':
                    response = self.post(url, data = data, headers = headers)
                elif method == 'PUT':
                    response = self.put(url, data = data, headers = headers)
                elif method == 'GET':
                    response = self.get(url, headers = headers)
                elif method == 'DELETE':
                    response = self.delete(url, headers = headers)
                else:
                    log_message = 'No se ha ingresado un método HTTP válido. El método ingresado es %(method)s' % { 'method': method }
                    raise ApiException(log_message)
                if response.status_code == 401:
                    if 'X-Stats-NavegadorSessionProblem' in response.headers and response.headers['X-Stats-NavegadorSessionProblem'] == '1':
                        url = self.rebuild_url(url)
                        raise ConnectionError('Ocurrió un error de conexión HTTP 401.')
                break
            except (ConnectionError, Timeout) as e:
                if n_current_attempts <= n_max_attempts:
                    time.sleep(wait_time)
                    n_current_attempts += 1
                    wait_time += 2
                else:
                    log_message = 'No fue posible establecer conexión con API Gateway: %(error)s' % {'error': str(e)}
                    raise ApiException(log_message)
        return response

class ApiException(Exception):
    '''
    Excepción personalizada para errores en el cliente de la API.

    :param str message: Mensaje de error.
    :param int code: Código de error (opcional).
    :param dict params: Parámetros adicionales del error (opcional).
    '''

    def __init__(self, message, code = None, params = None):
        self.message = message
        self.code = code
        self.params = params
        super().__init__(message)

    def __str__(self):
        '''
        Devuelve una representación en cadena del error, proporcionando un contexto claro
        del problema ocurrido. Esta representación incluye el prefijo "[API Gateway]",
        seguido del código de error si está presente, y el mensaje de error.

        Si se especifica un código de error, el formato será:
        "[API Gateway] Error {code}: {message}"

        Si no se especifica un código de error, el formato será:
        "[API Gateway] {message}"

        :return: Una cadena que representa el error de una manera clara y concisa.
        '''
        if self.code is not None:
            return "[API Gateway] Error %(code)s: %(message)s" % {'code': self.code, 'message': self.message}
        else:
            return "[API Gateway] %(message)s" % {'message': self.message}

class ApiBase(ABC):
    '''
    Clase base para las clases que consumen la API (wrappers).

    :param str api_token: Token de autenticación para la API.
    :param str api_url: URL base para la API.
    :param str api_version: Versión de la API.
    :param bool api_raise_for_status: Si se debe lanzar una excepción automáticamente para respuestas de error HTTP. Por defecto es True.
    :param dict kwargs: Argumentos adicionales para la autenticación.
    '''

    auth = {}

    def __init__(self, api_token = None, api_url = None, api_version = None, api_raise_for_status = True, **kwargs):
        self.client = ApiClient(api_token, api_url, api_version, api_raise_for_status)
        self.__setup_auth(kwargs)

    def __setup_auth(self, kwargs):
        '''
        Configura la autenticación específica para la aplicación.

        :param dict kwargs: Argumentos clave-valor para configurar la autenticación.
        '''
        usuario_rut = kwargs.get('usuario_rut')
        usuario_clave = kwargs.get('usuario_clave')
        if usuario_rut and usuario_clave:
            self.auth = {'pass': {'rut': usuario_rut, 'clave': usuario_clave}}

    def _get_auth_pass(self):
        '''
        Obtiene la autenticación de tipo 'pass'.

        :return: Información de autenticación.
        :rtype: dict
        :raises ApiException: Si falta información de autenticación.
        '''
        if 'pass' not in self.auth:
            raise ApiException('auth.pass missing.')
        if 'rut' not in self.auth['pass']:
            raise ApiException('auth.pass.rut missing.')
        if self.auth['pass']['rut'] == '' or self.auth['pass']['rut'] is None:
            raise ApiException('auth.pass.rut empty.')
        if 'clave' not in self.auth['pass']:
            raise ApiException('auth.pass.clave missing.')
        if self.auth['pass']['clave'] == '' or self.auth['pass']['clave'] is None:
            raise ApiException('auth.pass.clave empty.')
        return self.auth
