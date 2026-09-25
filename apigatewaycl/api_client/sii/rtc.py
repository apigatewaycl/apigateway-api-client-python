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
Módulo para el Registro de Transferencia de Crédito (RTC) del SII.

Para más información sobre la API, consulte la `documentación completa
del RTC <https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase, ApiResponse


class Cesiones(ApiBase):
    """
    Cliente para cesiones de DTE (factoring) del RTC de la API.

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
        """Autentica con `identificador`/`clave` del contribuyente."""
        super().__init__(
            identificador=identificador,
            clave=clave,
            **kwargs,  # type: ignore[arg-type]
        )

    def certificado(
        self,
        emisor: str,
        dte: str,
        folio: str,
        fecha: str,
        certificacion: str | None = None,
    ) -> bytes:
        """
        Certificado de cesión de un DTE, con cedente/cesionario/fecha.

        El certificado es un documento, no datos: la API lo entrega en
        HTML tal cual lo emite el SII, sin `data` ni `metadata`.

        :param str emisor: RUT del emisor del documento.
        :param str dte: Código del tipo de documento.
        :param str folio: Folio del documento.
        :param str fecha: Fecha de la cesión (AAAA-MM-DD), no la de
            emisión del documento. Es el campo `FCH_CESION` del
            listado de cesiones que entrega `documentos()`.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Certificado de cesión en HTML, sin decodificar.
        :rtype: bytes
        """
        url = self._build_url(
            '/sii/rtc/cesiones/certificado/%(emisor)s/%(dte)s/%(folio)s'
            '/%(fecha)s'
            % {
                'emisor': emisor,
                'dte': dte,
                'folio': folio,
                'fecha': fecha,
            },
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.content

    def estado_envio(
        self,
        track_id: str,
        certificacion: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Estado de envío de una cesión.

        Respuesta (ejemplo)::

            {
              "data": {
                "estado": "Anotacion de Cesion Aceptada, Envio A...",
                "track_id": 75312822
              },
              "metadata": {"timestamp": "..."}
            }

        :param str track_id: ID de la cesión.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, estado del envío y track id.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = self._build_url(
            '/sii/rtc/cesiones/estado_envio/%(track_id)s'
            % {'track_id': track_id},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def estado(
        self,
        emisor: str,
        dte: str,
        folio: str,
        certificacion: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Estado de cesión de un DTE (si está o no cedido, tenedor vigente).

        Respuesta (ejemplo)::

            {
              "data": {
                "cedido": true,
                "clave_acceso": "",
                "declaracion_jurada": "Archivo Electrónico de Cesión in...",
                "fecha_ultima_anotacion": "2019-07-06 19:56:58",
                "tenedor_vigente": "1-9"
              },
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor del documento.
        :param str dte: Código del tipo de documento.
        :param str folio: Folio del documento.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, estado de la cesión (y detalle, si hay tenedor vigente).
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = self._build_url(
            '/sii/rtc/cesiones/estado/%(emisor)s/%(dte)s/%(folio)s'
            % {'emisor': emisor, 'dte': dte, 'folio': folio},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def documentos(
        self,
        desde: str,
        hasta: str,
        consulta: str,
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> ApiResponse[list[dict[str, Any]]] | bytes:
        """
        Listado de documentos cedidos en un período (máximo 1 mes).

        Requiere autenticación de un contribuyente relacionado con la
        cesión (deudor, cedente o cesionario) o su representante.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "CEDENTE": "76192083-9",
                  "CESIONARIO": "2-7",
                  "DEUDOR": "1-9",
                  "ESTADO_CESION": "Cesion Vigente",
                  "FCH_CESION": "2019-07-06 19:56",
                  "FCH_EMIS_DTE": "2019-07-01",
                  "FCH_VENCIMIENTO": "2019-07-01",
                  "FOLIO_DOC": "123",
                  "...": "..."
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        :param str desde: Fecha de inicio (AAAA-MM-DD).
        :param str hasta: Fecha de fin, máximo 30 días desde `desde`
            (AAAA-MM-DD).
        :param str consulta: `'0'` deudor, `'1'` cedente, `'2'`
            cesionario.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'xml'`, `'csv'` o `'txt'` — de no
            indicarse, la respuesta es JSON.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de cesiones del período. Con `formato` `'xml'`,
            `'csv'` o `'txt'` se entrega el archivo crudo, sin decodificar.
        :rtype: ApiResponse[list[dict[str, Any]]] | bytes
        """
        url = self._build_url(
            '/sii/rtc/cesiones/documentos/%(desde)s/%(hasta)s/%(consulta)s'
            % {'desde': desde, 'hasta': hasta, 'consulta': consulta},
            certificacion=certificacion,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        if formato in ('xml', 'csv', 'txt'):
            return response.content
        return self._json(response)
