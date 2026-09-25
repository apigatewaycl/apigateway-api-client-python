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
Módulo para interactuar con la sección MiSii de un contribuyente.

Para más información sobre la API, consulte la `documentación completa
de MiSii
<https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase, ApiResponse


class Contribuyente(ApiBase):
    """
    Cliente para los endpoints de un Contribuyente de MiSii de la API.

    Hereda de ApiBase y utiliza su funcionalidad para realizar
    solicitudes a la API.
    """

    def __init__(
        self,
        identificador: str,
        clave: str,
        **kwargs: str,
    ) -> None:
        """Autentica con `identificador`/`clave` (usuario del SII)."""
        super().__init__(
            identificador=identificador,
            clave=clave,
            **kwargs,  # type: ignore[arg-type]
        )

    def datos(self) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene los datos de MiSii del contribuyente autenticado en el SII.

        Respuesta (ejemplo)::

            {
              "data": {
                "datos": {
                  "codigoError": 0,
                  "descripcionError": "OK",
                  "sysdate": "string",
                  "contribuyente": {
                    "codigoError": 0,
                    "descripcionError": "Contribuyente existe",
                    "sysdate": "string",
                    "rut": "1111111",
                    "dv": "4",
                    "...": "..."
                  },
                  "direcciones": [
                    {
                      "codigoError": 0,
                      "descripcionError": "Contribuyente posee dirección",
                      "sysdate": "string",
                      "codigo": "123456789",
                      "comunaCodigo": "43231",
                      "...": "..."
                    }
                  ],
                  "atributos": [
                    {
                      "rut": 1111111,
                      "dv": "4",
                      "atrCodigo": "NOTI",
                      "descAtrCodigo": "CONTRIBUYENTE ES NOTIFICADO POR...",
                      "fechaInicio": "01-05-2025",
                      "...": "..."
                    }
                  ],
                  "alertas": [{}]
                },
                "actividades_economicas": [
                  {
                    "codigoError": 0,
                    "descripcionError": "Contribuyente posee actividade...",
                    "sysdate": "string",
                    "codigo": "1111111",
                    "descripcion": "ACTIVIDAD ECONOMICA GLOSA",
                    "...": "..."
                  }
                ],
                "alertas": {
                  "codigoError": 0,
                  "descripcionError": "string",
                  "sysdate": "string",
                  "alertas": [{}]
                }
              },
              "metadata": {"timestamp": "..."}
            }

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos del contribuyente.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/misii/contribuyente/datos'
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)


class Representantes(ApiBase):
    """
    Cliente para los representantes de un contribuyente en MiSii.

    "Representantes" es quién puede actuar por el contribuyente
    autenticado (lo contrario de `Representados`).

    :param str identificador: Identificador del contribuyente.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    def __init__(
        self,
        identificador: str,
        clave: str,
        **kwargs: str,
    ) -> None:
        """Autentica con `identificador`/`clave` (usuario del SII)."""
        super().__init__(
            identificador=identificador,
            clave=clave,
            **kwargs,  # type: ignore[arg-type]
        )

    def listado(self) -> ApiResponse[dict[str, Any]]:
        """
        Listado de representantes del contribuyente autenticado.

        Incluye también el listado de permisos que se pueden asignar.

        Respuesta (ejemplo)::

            {
              "data": {
                "representado": {
                  "rut": 12345678,
                  "dv": "4",
                  "nombre": "Contribuyente"
                },
                "representantes": [
                  {"rut": 111111111, "dv": "4", "nombre": "Representante"}
                ],
                "permisos": [
                  {
                    "codigo": "MISII",
                    "descripcion": "Acceso a MiSII",
                    "nivel": "B"
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos del representado, sus representantes y permisos.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/misii/representantes/listado'
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)


class Representados(ApiBase):
    """
    Cliente para los representados de un contribuyente en MiSii.

    "Representados" es a quiénes puede representar el contribuyente
    autenticado (lo contrario de `Representantes`).

    :param str identificador: Identificador del contribuyente.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    def __init__(
        self,
        identificador: str,
        clave: str,
        **kwargs: str,
    ) -> None:
        """Autentica con `identificador`/`clave` (usuario del SII)."""
        super().__init__(
            identificador=identificador,
            clave=clave,
            **kwargs,  # type: ignore[arg-type]
        )

    def listado(self) -> ApiResponse[dict[str, Any]]:
        """
        Listado de contribuyentes que representa el usuario autenticado.

        Respuesta (ejemplo)::

            {
              "data": {
                "representante": {
                  "rut": 19550156,
                  "dv": "4",
                  "nombre": "NICOLAS BENJAMIN CONTRERAS BECERRA"
                },
                "representados": [],
                "permisos": []
              },
              "metadata": {"timestamp": "..."}
            }

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos del representante, sus representados y permisos.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/misii/representados/listado'
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def representar(
        self,
        rut: str,
        permisos: str,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Asigna qué contribuyente representar en las siguientes llamadas.

        Respuesta (ejemplo)::

            {
              "data": {
                "representado": {
                  "rut": 76192083,
                  "dv": "9",
                  "nombre": "EMPRESA SPA"
                }
              },
              "metadata": {"timestamp": "..."}
            }

        :param str rut: RUT del contribuyente a representar.
        :param str permisos: Códigos APPL de MiSII separados por coma
            (ej. `'RPETC,MISII'` — ver tabla de códigos en la spec).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos del contribuyente representado.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/misii/representados/representar/%(rut)s/%(permisos)s' % {
            'rut': rut,
            'permisos': permisos,
        }
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)
