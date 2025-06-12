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

from requests.exceptions import Timeout, ConnectionError, RequestException, HTTPError
from os import getenv
from abc import ABC

import urllib.parse
import urllib
import requests
import base64
import json
import re

class ApiClient:
    '''
    Cliente para interactuar con la API de API Gateway.

    :param str token: Token de autenticación del usuario. Si no se proporciona,
    se intentará obtener de una variable de entorno.
    :param str url: URL base de la API. Si no se proporciona, se usará una
    URL por defecto.
    :param str version: Versión de la API. Si no se proporciona, se usará
    una versión por defecto.
    :param bool raise_for_status: Si se debe lanzar una excepción automáticamente
    para respuestas de error HTTP. Por defecto es True.
    '''

    __DEFAULT_URL = 'https://legacy.apigateway.cl'
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
        return str(url).strip() if url else getenv(
            'APIGATEWAY_API_URL',
            self.__DEFAULT_URL).strip()

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

    def __request(self, method, resource, data = None, headers = None):
        '''
        Método privado para realizar solicitudes HTTP.

        :param str method: Método HTTP a utilizar.
        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud (opcional).
        :param dict headers: Cabeceras adicionales para la solicitud (opcional).
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        :raises ApiException: Si el método HTTP no es soportado o si hay
        un error de conexión.
        '''
        api_path = '/api/%(version)s%(resource)s' % {
            'version': self.version, 'resource': resource
        }
        full_url = urllib.parse.urljoin(self.url + '/', api_path.lstrip('/'))
        headers = headers or {}
        headers = {**self.headers, **headers}
        if data and not isinstance(data, str):
            data = json.dumps(data)
        try:
            response = requests.request(method, full_url, data = data, headers = headers)
            return self.__check_and_return_response(response)
        except ConnectionError as error:
            raise ApiException('Error de conexión: %(error)s' % {
                'error': error
            })
        except Timeout as error:
            raise ApiException('Error de timeout: %(error)s' % {
                'error': error
            })
        except RequestException as error:
            raise ApiException('Error en la solicitud: %(error)s' % {
                'error': error
            })

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
                    message = error.get(
                        'message', ''
                    ) or error.get(
                        'exception', ''
                    ) or 'Error desconocido.'
                except json.decoder.JSONDecodeError:
                    message = 'Error al decodificar los datos en JSON: %(response)s' % {
                        'response': response.text
                    }
                raise ApiException('Error HTTP: %(message)s' % {
                    'message': message
                })
        return response

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
            return "[API Gateway] Error %(code)s: %(message)s" % {
                'code': self.code,
                'message': self.message
            }
        else:
            return "[API Gateway] %(message)s" % {
                'message': self.message
            }

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

    def __init__(
            self,
            api_token = None,
            api_url = None,
            api_version = None,
            api_raise_for_status = True,
            **kwargs
        ):
        self.client = ApiClient(
            api_token,
            api_url,
            api_version,
            api_raise_for_status
        )
        self.__setup_auth(kwargs)

    def __setup_auth(self, kwargs):
        '''
        Configura la autenticación específica para la aplicación.

        :param dict kwargs: Argumentos clave-valor para configurar la autenticación.
        '''
        identificador = kwargs.get('identificador')
        clave = kwargs.get('clave')
        if identificador and clave:
            if self.__is_auth_pass(identificador):
                self.auth = {
                    'pass': {
                        'rut': identificador,
                        'clave': clave
                    }
                }
            elif self.__is_auth_cert_data(identificador):
                self.auth = {
                    'cert': {
                        'cert-data': identificador,
                        'pkey-data': clave
                    }
                }
            elif self.__is_auth_file_data(identificador):
                self.auth = {
                    'cert': {
                        'file-data': identificador,
                        'file-pass': clave
                    }
                }
            else:
                raise ApiException('No se han proporcionado las credenciales de autentificación.')

    def __is_auth_pass(self, rut):
        """
        Valida la estructura de un RUT chileno utilizando una expresión regular.

        Este método verifica que el RUT cumpla con el formato estándar chileno, que incluye
        puntos como separadores de miles opcionales y un guion antes del dígito verificador.
        El dígito verificador puede ser un número o la letra 'K'.

        **Ejemplos de RUT válidos:**
            - 12.345.678-5
            - 12345678-5
            - 9.876.543-K
            - 9876543-K

        **Ejemplos de RUT inválidos:**
            - 12.345.678-9 (dígito verificador incorrecto)
            - 12345678- (falta dígito verificador)
            - 12345-6 (formato incorrecto)
            - 12.345.6785 (falta guion)
            - abcdefgh-i (caracteres no permitidos)

        :param str rut: El RUT a validar.
        :return: True si el RUT tiene un formato válido, False en caso contrario.
        :rtype: bool
        """
        if rut is None:
            return False
        # Expresión regular para validar el formato del RUT chileno
        patron = re.compile(r'^(\d{1,3}\.?)(\d{3}\.?)(\d{3,4})-([\dkK])$')
        return bool(patron.match(rut))

    def __is_auth_file_data(self, firma_electronica_base64):
        """
        Verifica si una cadena es una cadena codificada en Base64 válida.

        :param str firma_electronica_base64: La cadena a verificar.
        :return: True si la cadena es válida en Base64, False en caso contrario.
        :rtype: bool
        """
        if firma_electronica_base64 is None:
            return False
        try:
            # Asegúrate de que la longitud de la cadena sea múltiplo de 4
            if len(firma_electronica_base64) % 4 != 0:
                return False
            # Intenta decodificar la cadena con validación estricta
            base64.b64decode(firma_electronica_base64, validate=True)
            return True
        except (base64.binascii.Error, ValueError):
            return False

    def __is_auth_cert_data(self, pem_str):
        """
        Valida si una cadena tiene formato PEM válido.

        El formato PEM debe cumplir con los siguientes criterios:
            - Comienza con una línea "-----BEGIN [LABEL]-----"
            - Termina con una línea "-----END [LABEL]-----"
            - Contiene contenido Base64 válido entre las líneas BEGIN y END

        **Ejemplos de PEM Válidos:**
            ```
            -----BEGIN CERTIFICATE-----
            MIIDdzCCAl+gAwIBAgIEbGzVnzANBgkqhkiG9w0BAQsFADBvMQswCQYDVQQGEwJV
            ...
            -----END CERTIFICATE-----
            ```

        **Ejemplos de PEM Inválidos:**
            - Falta la línea de inicio o fin.
            - Contenido no codificado en Base64.
            - Etiquetas de BEGIN y END que no coinciden.

        :param str pem_str: La cadena a validar.
        :return: True si la cadena tiene formato PEM válido, False en caso contrario.
        :rtype: bool
        """
        if pem_str is None:
            return False
        # Expresión regular para validar el formato PEM
        patron = re.compile(
            r'-----BEGIN ([A-Z ]+)-----\s+'
            r'([A-Za-z0-9+/=\s]+)'
            r'-----END \1-----$',
            re.MULTILINE
        )

        # Intentar hacer match con el patrón
        match = patron.fullmatch(pem_str.strip())
        if not match:
            return False

        # Extraer el contenido Base64
        base64_content = match.group(2).replace('\n', '').replace('\r', '').strip()

        # Verificar que el contenido Base64 sea válido
        try:
            base64.b64decode(base64_content, validate=True)
            return True
        except (base64.binascii.Error, ValueError):
            return False

    def _get_auth_pass(self):
        '''
        Obtiene la autenticación de tipo 'pass'.

        :return: Información de autenticación.
        :rtype: dict
        :raises ApiException: Si falta información de autenticación.
        '''
        if 'pass' in self.auth:
            if 'rut' not in self.auth['pass']:
                raise ApiException('auth.pass.rut missing.')
            if self.auth['pass']['rut'] == '' or self.auth['pass']['rut'] is None:
                raise ApiException('auth.pass.rut empty.')
            if 'clave' not in self.auth['pass']:
                raise ApiException('auth.pass.clave missing.')
            if self.auth['pass']['clave'] == '' or self.auth['pass']['clave'] is None:
                raise ApiException('auth.pass.clave empty.')
        elif 'cert' in self.auth:
            if 'cert-data' in self.auth['cert'] and self.auth['cert']['cert-data'] == '' and self.auth['cert']['cert-data'] is None:
                raise ApiException('auth.cert.cert-data empty.')
            if 'pkey-data' in self.auth['cert'] and self.auth['cert']['pkey-data'] == '' and self.auth['cert']['pkey-data'] is None:
                raise ApiException('auth.cert.pkey-data empty.')
            if 'file-data' in self.auth['cert'] and self.auth['cert']['file-data'] == '' and self.auth['cert']['file-data'] is None:
                raise ApiException('auth.cert.file-data empty.')
            if 'file-pass' in self.auth['cert'] and self.auth['cert']['file-pass'] == '' and self.auth['cert']['file-pass'] is None:
                raise ApiException('auth.cert.file-pass empty.')
        else:
            raise ApiException('auth.pass or auth.cert missing.')
        return self.auth
