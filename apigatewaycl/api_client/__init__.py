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

from abc import ABC
from os import getenv
import requests
import json
from requests.exceptions import ConnectionError
import urllib

class ApiClient:
    """
    Cliente para interactuar con la API de API Gateway.

    :param str token: Token de autenticación del usuario. Si no se proporciona, se intentará obtener de una variable de entorno.
    :param str url: URL base de la API. Si no se proporciona, se usará una URL por defecto.
    :param str version: Versión de la API. Si no se proporciona, se usará una versión por defecto.
    """

    __DEFAULT_URL = 'https://apigateway.cl'
    __DEFAULT_VERSION = 'v1'

    def __init__(self, token=None, url=None, version=None):
        self.token = self.__validate_token(token)
        self.url = self.__validate_url(url)
        self.headers = self.__generate_headers()
        self.version = version if version is not None else self.__DEFAULT_VERSION

    def __validate_token(self, token):
        """
        Valida y retorna el token de autenticación.

        :param str token: Token de autenticación a validar.
        :return: Token validado.
        :rtype: str
        :raises ApiException: Si el token no es válido o está ausente.
        """
        token = token or getenv('APIGATEWAY_API_TOKEN')
        if not token:
            raise ApiException('APIGATEWAY_API_TOKEN missing')
        return token.strip()

    def __validate_url(self, url):
        """
        Valida y retorna la URL base para la API.

        :param str url: URL a validar.
        :return: URL validada.
        :rtype: str
        :raises ApiException: Si la URL no es válida o está ausente.
        """
        return url.strip() if url else getenv('APIGATEWAY_API_URL', self.__DEFAULT_URL).strip()

    def __generate_headers(self):
        """
        Genera y retorna las cabeceras por defecto para las solicitudes.

        :return: Cabeceras por defecto.
        :rtype: dict
        """
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }

    def get(self, resource, headers={}):
        """
        Realiza una solicitud GET a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        """
        return self.__request('GET', resource, headers=headers)

    def delete(self, resource, headers={}):
        """
        Realiza una solicitud DELETE a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        """
        return self.__request('DELETE', resource, headers=headers)

    def post(self, resource, data=None, headers={}):
        """
        Realiza una solicitud POST a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        """
        return self.__request('POST', resource, data, headers)

    def put(self, resource, data=None, headers={}):
        """
        Realiza una solicitud PUT a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        """
        return self.__request('PUT', resource, data, headers)

    def __request(self, method, resource, data=None, headers={}):
        """
        Método privado para realizar solicitudes HTTP.

        :param str method: Método HTTP a utilizar.
        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud (opcional).
        :param dict headers: Cabeceras adicionales para la solicitud (opcional).
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        :raises ApiException: Si el método HTTP no es soportado o si hay un error de conexión.
        """
        api_path = f'/api/{self.version}{resource}'
        full_url = urllib.parse.urljoin(self.url + '/', api_path.lstrip('/'))
        headers = {**self.headers, **headers}
        if data and not isinstance(data, str):
            data = json.dumps(data)
        try:
            response = requests.request(method, full_url, data=data, headers=headers)
        except ConnectionError as e:
            raise ApiException(f'Error al conectar con el servidor: {e}')
        return self.__check_and_return_response(response)

    def __check_and_return_response(self, response):
        """
        Verifica la respuesta de la solicitud HTTP y maneja los errores.

        :param requests.Response response: Objeto de respuesta de requests.
        :return: Respuesta validada.
        :rtype: requests.Response
        :raises ApiException: Si la respuesta contiene un error HTTP.
        """
        if response.status_code != 200:
            try:
                error = response.json()
                message = error.get('message', '') or error.get('exception', '') or 'Error inesperado'
            except json.decoder.JSONDecodeError:
                message = f'Error al decodificar JSON: {response.text}'
            raise ApiException(message)
        return response

class ApiException(Exception):
    """
    Excepción personalizada para errores en el cliente de la API.

    :param str message: Mensaje de error.
    :param int code: Código de error (opcional).
    :param dict params: Parámetros adicionales del error (opcional).
    """

    def __init__(self, message, code=None, params=None):
        self.message = message
        super().__init__(message, code, params)

class ApiBase(ABC):
    """
    Clase base para las clases que consumen la API (wrappers).

    :param str api_token: Token de autenticación para la API.
    :param str api_url: URL base para la API.
    :param str api_version: Versión de la API.
    :param dict kwargs: Argumentos adicionales para la autenticación.
    """

    auth = {}

    def __init__(self, api_token=None, api_url=None, api_version=None, **kwargs):
        self.client = ApiClient(api_token, api_url, api_version)
        self.__setup_auth(kwargs)

    def __setup_auth(self, kwargs):
        """
        Configura la autenticación específica para la aplicación.

        :param dict kwargs: Argumentos clave-valor para configurar la autenticación.
        """
        usuario_rut = kwargs.get('usuario_rut')
        usuario_clave = kwargs.get('usuario_clave')
        if usuario_rut and usuario_clave:
            self.auth = {'pass': {'rut': usuario_rut, 'clave': usuario_clave}}

    def _get_auth_pass(self):
        """
        Obtiene la autenticación de tipo 'pass'.

        :return: Información de autenticación.
        :rtype: dict
        :raises ApiException: Si falta información de autenticación.
        """
        if 'pass' not in self.auth:
            raise ApiException('auth.pass missing')
        if 'rut' not in self.auth['pass']:
            raise ApiException('auth.pass.rut missing')
        if self.auth['pass']['rut'] == '' or self.auth['pass']['rut'] is None:
            raise ApiException('auth.pass.rut empty')
        if 'clave' not in self.auth['pass']:
            raise ApiException('auth.pass.clave missing')
        if self.auth['pass']['clave'] == '' or self.auth['pass']['clave'] is None:
            raise ApiException('auth.pass.clave empty')
        return self.auth
