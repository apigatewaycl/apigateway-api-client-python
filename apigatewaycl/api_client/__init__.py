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

"""
Cliente base de la API de API Gateway (`ApiClient`/`ApiBase`).

Este cliente habla únicamente con la versión 2 de la API
(`https://app.apigateway.cl/api/v2`). La versión 1 (legacy) ya no
está soportada.

Los métodos que responden JSON entregan el cuerpo tal cual lo envía
la API, sin transformarlo::

    {"data": ..., "metadata": {...}}

`data` trae el resultado y `metadata` los datos de la consulta
(marca de tiempo, paginación, etc.). Los recursos que responden un
archivo (PDF, XML, CSV, HTML) entregan su contenido sin decodificar.
"""

from __future__ import annotations

import base64
import json
import re
import urllib.parse
from os import getenv
from typing import Any, cast

import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import HTTPError, RequestException, Timeout

from .tipos import ApiResponse

__all__ = ['ApiBase', 'ApiClient', 'ApiException', 'ApiResponse']

_HTTP_OK = 200

# La API avisa con esta cabecera cuando el SII pidió reautenticar, y el
# mensaje de error también lo dice. Ver la documentación de la API:
# "conviene repetir la consulta con auth_cache=0 para forzar un login".
_CABECERA_SESION = 'X-Auth-Session-Problem'
_TEXTO_SESION = 'volver a autenticar'


def _sesion_caida(response: requests.Response) -> bool:
    """
    Indica si la API avisó que hay que reautenticar ante el SII.

    Ocurre cuando el SII cerró la sesión antes de que venciera y la
    API intentó reutilizar la que tenía guardada.

    :param requests.Response response: Respuesta de la API.
    :return: True si corresponde repetir forzando un login nuevo.
    :rtype: bool
    """
    if response.headers.get(_CABECERA_SESION) == '1':
        return True
    if response.status_code == _HTTP_OK:
        return False
    return _TEXTO_SESION in response.text[:2000]


class ApiClient:
    """
    Cliente para interactuar con la API de API Gateway.

    :param str token: Token de autenticación del usuario. Si no se
        proporciona, se intentará obtener de una variable de entorno.
    :param str url: URL base de la API. Si no se proporciona, se usará
        `https://app.apigateway.cl`.
    :param bool raise_for_status: Si se debe lanzar una excepción
        automáticamente para respuestas de error HTTP. Por defecto es
        True.
    :param bool auth_cache: Con `False` se fuerza un login nuevo en el
        SII en vez de reutilizar la sesión guardada. Sirve para
        recuperarse cuando el portal cerró la sesión antes de que
        venciera y la API responde que hay que volver a autenticar.
    """

    _api_version = 'v2'
    _default_url = 'https://app.apigateway.cl'
    token_prefix = 'Token'

    def __init__(
        self,
        token: str | None = None,
        url: str | None = None,
        raise_for_status: bool = True,
        auth_cache: bool | None = None,
    ) -> None:
        """Construye el cliente validando el token y la URL."""
        self.token = self.__validate_token(token)
        self.url = self.__validate_url(url)
        self.headers = self.__generate_headers()
        self.raise_for_status = raise_for_status
        self.auth_cache = auth_cache

    def __validate_token(self, token: str | None) -> str:
        """
        Valida y retorna el token de autenticación.

        :param str token: Token de autenticación a validar.
        :return: Token validado.
        :rtype: str
        :raises ApiException: Si el token no es válido o está ausente.
        """
        token = token or getenv('APIGATEWAY_API_TOKEN')
        if not token:
            raise ApiException(
                'Se debe configurar la variable de entorno: '
                'APIGATEWAY_API_TOKEN.'
            )
        return str(token).strip()

    def __validate_url(self, url: str | None) -> str:
        """
        Valida y retorna la URL base para la API.

        :param str url: URL a validar.
        :return: URL validada.
        :rtype: str
        :raises ApiException: Si la URL no es válida o está ausente.
        """
        return (
            str(url).strip()
            if url
            else getenv('APIGATEWAY_API_URL', self._default_url).strip()
        )

    def __generate_headers(self) -> dict[str, str]:
        """
        Genera y retorna las cabeceras por defecto para las solicitudes.

        :return: Cabeceras por defecto.
        :rtype: dict[str, str]
        """
        return {
            'User-Agent': 'API Gateway: Cliente de API en Python.',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': '%(prefix)s %(token)s'
            % {'prefix': self.token_prefix, 'token': self.token},
        }

    def __request(
        self,
        method: str,
        resource: str,
        data: dict[str, Any] | str | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """
        Método privado para realizar solicitudes HTTP.

        :param str method: Método HTTP a utilizar.
        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud (opcional).
        :param dict headers: Cabeceras adicionales para la solicitud
            (opcional).
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        :raises ApiException: Si el método HTTP no es soportado o si
            hay un error de conexión.
        """
        api_path = '/api/%(version)s%(resource)s' % {
            'version': self._api_version,
            'resource': resource,
        }
        if self.auth_cache is not None:
            # La API lo lee para cualquier recurso de scraping, así que
            # se agrega de forma transversal y no método por método.
            separador = '&' if '?' in api_path else '?'
            api_path += '%(sep)sauth_cache=%(valor)s' % {
                'sep': separador,
                'valor': '1' if self.auth_cache else '0',
            }
        full_url = urllib.parse.urljoin(self.url + '/', api_path.lstrip('/'))
        headers = headers or {}
        headers = {**self.headers, **headers}
        if data and not isinstance(data, str):
            data = json.dumps(data)
        try:
            response = requests.request(
                method,
                full_url,
                data=data,
                headers=headers,
            )
            # Si la sesión del SII se cayó, se repite una sola vez
            # forzando un login nuevo. Es de rescate: dejar
            # `auth_cache=0` en todas las llamadas abre una sesión por
            # consulta y el SII bloquea la cuenta al pasar de diez.
            if self.auth_cache is None and _sesion_caida(response):
                reintento = urllib.parse.urljoin(
                    self.url + '/',
                    (
                        api_path
                        + ('&' if '?' in api_path else '?')
                        + 'auth_cache=0'
                    ).lstrip('/'),
                )
                response = requests.request(
                    method,
                    reintento,
                    data=data,
                    headers=headers,
                )
            return self.__check_and_return_response(response)
        except RequestsConnectionError as error:
            raise ApiException(
                'Error de conexión: %(error)s' % {'error': error}
            ) from error
        except Timeout as error:
            raise ApiException(
                'Error de timeout: %(error)s' % {'error': error}
            ) from error
        except RequestException as error:
            raise ApiException(
                'Error en la solicitud: %(error)s' % {'error': error}
            ) from error

    def __check_and_return_response(
        self, response: requests.Response
    ) -> requests.Response:
        """
        Verifica la respuesta de la solicitud HTTP y maneja los errores.

        :param requests.Response response: Objeto de respuesta de requests.
        :return: La misma respuesta HTTP, ya validada.
        :rtype: requests.Response
        :raises ApiException: Si la respuesta contiene un error HTTP.
        """
        if response.status_code != _HTTP_OK and self.raise_for_status:
            try:
                response.raise_for_status()
            except HTTPError as http_error:
                try:
                    error = response.json()
                    message = (
                        error.get('detail', '')
                        or error.get('message', '')
                        or error.get('exception', '')
                        or json.dumps(error)
                        or 'Error desconocido.'
                    )
                except json.decoder.JSONDecodeError:
                    message = (
                        'Error al decodificar los datos en JSON: '
                        '%(response)s' % {'response': response.text}
                    )
                raise ApiException(
                    'Error HTTP: %(message)s' % {'message': message}
                ) from http_error
        return response

    def get(
        self,
        resource: str,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """
        Realiza una solicitud GET a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        """
        return self.__request('GET', resource, headers=headers)

    def delete(
        self,
        resource: str,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """
        Realiza una solicitud DELETE a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        """
        return self.__request('DELETE', resource, headers=headers)

    def post(
        self,
        resource: str,
        data: dict[str, Any] | str | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """
        Realiza una solicitud POST a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        """
        return self.__request('POST', resource, data, headers)

    def put(
        self,
        resource: str,
        data: dict[str, Any] | str | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """
        Realiza una solicitud PUT a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        """
        return self.__request('PUT', resource, data, headers)


class ApiException(Exception):
    """
    Excepción personalizada para errores en el cliente de la API.

    :param str message: Mensaje de error.
    :param int code: Código de error (opcional).
    :param dict params: Parámetros adicionales del error (opcional).
    """

    def __init__(
        self,
        message: str,
        code: int | None = None,
        params: dict[str, Any] | None = None,
    ) -> None:
        """Guarda `message`/`code`/`params` del error."""
        self.message = message
        self.code = code
        self.params = params
        super().__init__(message)

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del error.

        Proporciona un contexto claro del problema ocurrido. Esta
        representación incluye el prefijo "[API Gateway]", seguido
        del código de error si está presente, y el mensaje de error.

        Si se especifica un código de error, el formato será:
        "[API Gateway] Error {code}: {message}"

        Si no se especifica un código de error, el formato será:
        "[API Gateway] {message}"

        :return: Una cadena que representa el error de forma clara.
        """
        if self.code is not None:
            return '[API Gateway] Error %(code)s: %(message)s' % {
                'code': self.code,
                'message': self.message,
            }
        return '[API Gateway] %(message)s' % {'message': self.message}


class ApiBase:
    """
    Clase base para las clases que consumen la API (wrappers).

    No es ABC: ninguna subclase fuerza métodos propios con
    `abstractmethod` — todas comparten exactamente el mismo `__init__`
    (autenticación), no hay nada que declarar como contrato acá.

    Los dos primeros argumentos posicionales son siempre las
    credenciales del contribuyente, en todas las clases. Antes, las que
    no definían su propio `__init__` heredaban este con `api_token` y
    `api_url` al frente, así que `Clase(rut, clave)` terminaba usando
    la clave como URL de la API.

    :param str identificador: RUT del contribuyente, o el certificado
        digital en PEM o en base64. Opcional: los recursos públicos no
        lo necesitan.
    :param str clave: Clave del identificador, o la llave privada
        cuando el identificador es un certificado en PEM.
    :param str api_token: Token de autenticación para la API.
    :param str api_url: URL base para la API.
    :param bool api_raise_for_status: Si se debe lanzar una excepción
        automáticamente para respuestas de error HTTP. Por defecto es
        True.
    :param bool api_auth_cache: Con `False` se fuerza un login nuevo en
        el SII en vez de reutilizar la sesión guardada.
    :param dict kwargs: Argumentos adicionales para la autenticación.
    """

    def __init__(
        self,
        identificador: str | None = None,
        clave: str | None = None,
        api_token: str | None = None,
        api_url: str | None = None,
        api_raise_for_status: bool = True,
        api_auth_cache: bool | None = None,
        **kwargs: str,
    ) -> None:
        """Arma el `ApiClient` y configura la autenticación."""
        self.auth: dict[str, Any] = {}
        self.client = ApiClient(
            api_token,
            api_url,
            api_raise_for_status,
            api_auth_cache,
        )
        credenciales = dict(kwargs)
        if identificador is not None:
            credenciales['identificador'] = identificador
        if clave is not None:
            credenciales['clave'] = clave
        self.__setup_auth(credenciales)

    def __setup_auth(self, kwargs: dict[str, str]) -> None:
        """
        Configura la autenticación específica para la aplicación.

        :param dict kwargs: Argumentos clave-valor para configurar la
            autenticación.
        """
        identificador = kwargs.get('identificador')
        clave = kwargs.get('clave')
        if identificador and clave:
            if self.__is_auth_pass(identificador):
                self.auth = {'pass': {'rut': identificador, 'clave': clave}}
            elif self.__is_auth_cert_data(identificador):
                # Se guardan normalizados: si vinieron en una sola
                # línea con los saltos escapados, la API debe recibir
                # los saltos reales.
                self.auth = {
                    'cert': {
                        'cert-data': self._normalizar_pem(identificador),
                        'pkey-data': self._normalizar_pem(clave),
                    }
                }
            elif self.__is_auth_file_data(identificador):
                self.auth = {
                    'cert': {'file-data': identificador, 'file-pass': clave}
                }
            else:
                raise ApiException(
                    'No se han proporcionado las credenciales de '
                    'autentificación.'
                )

    def __is_auth_pass(self, rut: str | None) -> bool:
        """
        Valida la estructura de un RUT chileno con una expresión regular.

        Este método verifica que el RUT cumpla con el formato estándar
        chileno, que incluye puntos como separadores de miles
        opcionales y un guion antes del dígito verificador. El dígito
        verificador puede ser un número o la letra 'K'.

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
        :return: True si el RUT tiene un formato válido.
        :rtype: bool
        """
        if rut is None:
            return False
        # Expresión regular para validar el formato del RUT chileno
        patron = re.compile(r'^(\d{1,3}\.?)(\d{3}\.?)(\d{3,4})-([\dkK])$')
        return bool(patron.match(rut))

    def __is_auth_file_data(
        self, firma_electronica_base64: str | None
    ) -> bool:
        """
        Verifica si una cadena es una cadena codificada en Base64 válida.

        :param str firma_electronica_base64: La cadena a verificar.
        :return: True si la cadena es válida en Base64.
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
        except (base64.binascii.Error, ValueError):  # type: ignore[attr-defined]
            return False
        else:
            return True

    @staticmethod
    def _normalizar_pem(pem_str: str) -> str:
        r"""
        Convierte a saltos de línea reales los `\n` escritos como texto.

        El tutorial oficial para extraer el PEM desde un `.p12` deja el
        certificado y la llave en una sola línea, con los saltos
        escapados, para poder pegarlos dentro de un JSON. Leído desde
        Python ese archivo llega con los `\n` literales, así que se
        normalizan antes de usarlo.

        :param str pem_str: Contenido del PEM, tal cual se recibió.
        :return: El mismo contenido con saltos de línea reales.
        :rtype: str
        """
        return pem_str.replace('\\r\\n', '\n').replace('\\n', '\n')

    def __is_auth_cert_data(self, pem_str: str | None) -> bool:
        """
        Valida si una cadena tiene formato PEM válido.

        Acepta uno o varios bloques seguidos, porque el certificado de
        una firma electrónica suele venir como cadena de certificación
        con dos o más bloques `BEGIN CERTIFICATE`. También acepta el
        PEM en una sola línea con los saltos escapados.

        El formato PEM de cada bloque debe cumplir con lo siguiente:
            - Comienza con una línea "-----BEGIN [LABEL]-----"
            - Termina con una línea "-----END [LABEL]-----"
            - Contiene contenido Base64 válido entre BEGIN y END

        :param str pem_str: La cadena a validar.
        :return: True si la cadena tiene formato PEM válido.
        :rtype: bool
        """
        if pem_str is None:
            return False
        texto = self._normalizar_pem(pem_str).strip()
        patron = re.compile(
            r'-----BEGIN (?P<etiqueta>[A-Z ]+)-----\s+'
            r'(?P<cuerpo>[A-Za-z0-9+/=\s]+?)'
            r'-----END (?P=etiqueta)-----'
        )
        bloques = list(patron.finditer(texto))
        if not bloques:
            return False
        # Fuera de los bloques no puede haber nada más que espacios.
        resto = texto
        for bloque in bloques:
            resto = resto.replace(bloque.group(0), '', 1)
        if resto.strip():
            return False
        # Cada bloque debe traer Base64 válido.
        for bloque in bloques:
            cuerpo = re.sub(r'\s', '', bloque.group('cuerpo'))
            try:
                base64.b64decode(cuerpo, validate=True)
            except (base64.binascii.Error, ValueError):  # type: ignore[attr-defined]
                return False
        return True

    def _build_url(self, recurso: str, **params: Any) -> str:
        """
        Arma un recurso de la API junto a su query string.

        Los parámetros con valor `None` se omiten, para que la API
        aplique el valor por defecto que tenga definido para cada uno.

        :param str recurso: Recurso de la API, sin query string.
        :param params: Parámetros a enviar en la query string.
        :return: Recurso con la query string ya codificada.
        :rtype: str
        """
        query = {
            clave: str(valor)
            for clave, valor in params.items()
            if valor is not None
        }
        if not query:
            return recurso
        return '%(recurso)s?%(query)s' % {
            'recurso': recurso,
            'query': urllib.parse.urlencode(query),
        }

    @staticmethod
    def _json(response: requests.Response) -> ApiResponse[Any]:
        """
        Entrega el cuerpo JSON de la respuesta, tipado como `ApiResponse`.

        `requests` tipa `json()` como `Any`; el `cast` se hace acá una
        sola vez en vez de repetirlo en cada método. `ApiResponse[Any]`
        se asigna a cualquier `ApiResponse[T]`, así que cada método
        declara la forma de `data` en su anotación sin otro `cast`.

        :param requests.Response response: Respuesta de la API.
        :return: Respuesta de la API, con `data` y `metadata`.
        :rtype: ApiResponse[Any]
        """
        return cast(ApiResponse[Any], response.json())

    def _get_auth(self) -> dict[str, Any]:
        """
        Obtiene la autenticación configurada, validando sus datos.

        La autenticación puede ser de tipo 'pass' (RUT y clave) o de
        tipo 'cert' (certificado y llave en PEM, o archivo de la firma
        electrónica en Base64 y su contraseña).

        :return: Información de autenticación, con la clave 'pass' o
            'cert' según el tipo configurado.
        :rtype: dict[str, Any]
        :raises ApiException: Si falta información de autenticación o
            viene vacía.
        """
        if 'pass' in self.auth:
            auth_pass = self.auth['pass']
            if 'rut' not in auth_pass:
                raise ApiException('auth.pass.rut missing.')
            if auth_pass['rut'] == '' or auth_pass['rut'] is None:
                raise ApiException('auth.pass.rut empty.')
            if 'clave' not in auth_pass:
                raise ApiException('auth.pass.clave missing.')
            if auth_pass['clave'] == '' or auth_pass['clave'] is None:
                raise ApiException('auth.pass.clave empty.')
        elif 'cert' in self.auth:
            auth_cert = self.auth['cert']
            if 'cert-data' in auth_cert and (
                auth_cert['cert-data'] == '' or auth_cert['cert-data'] is None
            ):
                raise ApiException('auth.cert.cert-data empty.')
            if 'pkey-data' in auth_cert and (
                auth_cert['pkey-data'] == '' or auth_cert['pkey-data'] is None
            ):
                raise ApiException('auth.cert.pkey-data empty.')
            if 'file-data' in auth_cert and (
                auth_cert['file-data'] == '' or auth_cert['file-data'] is None
            ):
                raise ApiException('auth.cert.file-data empty.')
            if 'file-pass' in auth_cert and (
                auth_cert['file-pass'] == '' or auth_cert['file-pass'] is None
            ):
                raise ApiException('auth.cert.file-pass empty.')
        else:
            raise ApiException('auth.pass or auth.cert missing.')
        return self.auth
