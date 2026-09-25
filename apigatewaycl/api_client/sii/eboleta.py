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
Módulo para eBoleta (Boletas Electrónicas del SII, sistema propio).

Para más información sobre la API, consulte la `documentación completa
de eBoleta <https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase, ApiResponse


class EboletaContribuyente(ApiBase):
    """
    Cliente para información de contribuyentes emisores de eBoleta.

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

    def emisor(self, emisor: str) -> ApiResponse[dict[str, Any]]:
        """
        Información del emisor de la boleta electrónica.

        Respuesta (ejemplo)::

            {
              "data": {
                "contribuyente": {
                  "rut": 12345678,
                  "razon_social": "RAZON SOCIAL DEL EMISOR",
                  "dv": "9",
                  "giro": "GIRO DEL EMISOR",
                  "actividad_economica": "Actividad económica del emisor",
                  "telefono": "1234567890",
                  "email": "emisor@example.com",
                  "direccion": "Dirección del emisor",
                  "...": "..."
                },
                "sucursales": [
                  {
                    "rut": 12345678,
                    "codigo": 12345678,
                    "sucursal": null,
                    "direccion": "ERRAZURIZ 827 ",
                    "comuna": "Santa Cruz",
                    "...": "..."
                  }
                ],
                "usuarios": [
                  {
                    "user": "12345678-9",
                    "nombre": "NOMBRE DEL USUARIO 1",
                    "es_representante": true,
                    "permisos": 0,
                    "total_records": 2
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor (formato 11222333-K).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos del contribuyente, sus sucursales y usuarios.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/eboleta/contribuyente/emisor/%(emisor)s' % {
            'emisor': emisor,
        }
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def emisores_autorizados(self) -> ApiResponse[dict[str, Any]]:
        """
        Lista de emisores autorizados de la boleta electrónica.

        Respuesta (ejemplo)::

            {
              "data": {
                "emisores": [
                  {
                    "rut": 12345678,
                    "dv": "9",
                    "razon_social": "RAZON SOCIAL DEL EMISOR"
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de contribuyentes (RUT, DV y razón social).
        :rtype: ApiResponse[dict[str, Any]]
        """
        body = {'auth': self._get_auth()}
        response = self.client.post(
            '/sii/eboleta/contribuyente/emisores_autorizados',
            data=body,
        )
        return self._json(response)


class EboletaEmitidas(ApiBase):
    """
    Cliente para boletas electrónicas emitidas de eBoleta.

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

    def _body_documento(
        self,
        contribuyente: str,
        folio: int,
        dte: int,
        fecha: str,
    ) -> dict[str, Any]:
        """
        Cuerpo que identifica un documento ya emitido.

        `documento()`, `pdf()` y `email()` apuntan al mismo documento
        con estos cuatro campos, todos en el cuerpo.

        :param str contribuyente: RUT del contribuyente.
        :param int folio: Folio del documento.
        :param int dte: Tipo de documento.
        :param str fecha: Fecha de emisión del documento (AAAA-MM-DD).
        :return: Cuerpo de la solicitud, con la autenticación incluida.
        :rtype: dict[str, Any]
        """
        return {
            'auth': self._get_auth(),
            'contribuyente': contribuyente,
            'folio': folio,
            'dte': dte,
            'fecha': fecha,
        }

    def documentos(
        self,
        contribuyente: str,
        date_from: str,
        date_to: str,
        page: int | None = None,
        items_per_page: int | None = None,
        estado: str | None = None,
    ) -> ApiResponse[list[dict[str, Any]]]:
        """
        Listado de documentos emitidos de la boleta electrónica.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "folio": 35,
                  "neto": 4202,
                  "iva": 798,
                  "total": 5000,
                  "exento": 0,
                  "dte": 39,
                  "revision_estado": "pendiente",
                  "anulado": false,
                  "...": "..."
                }
              ],
              "metadata": {
                "timestamp": "...",
                "total": "23390",
                "cantidad_emitida": "5"
              }
            }

        :param str contribuyente: RUT del contribuyente, sin puntos ni
            dígito verificador.
        :param str date_from: Fecha de inicio (AAAA-MM-DD).
        :param str date_to: Fecha de fin (AAAA-MM-DD).
        :param int page: Página a obtener (por defecto `1`).
        :param int items_per_page: Ítems por página (por defecto
            `10`).
        :param str estado: Estado del documento (por defecto
            `emitido`).
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, el listado de documentos emitidos; en `metadata`,
            los datos de la consulta.
        :rtype: ApiResponse[list[dict[str, Any]]]
        """
        # Todos los parámetros de esta API van en el cuerpo, no en la
        # ruta ni en la query string. Los opcionales no se envían si
        # no se indican, para que aplique el valor por defecto.
        opcionales = {
            'page': page,
            'items_per_page': items_per_page,
            'estado': estado,
        }
        body: dict[str, Any] = {
            'auth': self._get_auth(),
            'contribuyente': contribuyente,
            'date_from': date_from,
            'date_to': date_to,
        }
        body.update(
            {
                clave: valor
                for clave, valor in opcionales.items()
                if valor is not None
            }
        )
        response = self.client.post(
            '/sii/eboleta/emitidas/documentos',
            data=body,
        )
        return self._json(response)

    def emitir(self, dte: dict[str, Any]) -> ApiResponse[dict[str, Any]]:
        """
        Emite una Boleta Electrónica Afecta (39) o Exenta (41).

        Solo admite un ítem por documento. `dte['vendedor']` debe ser
        el mismo RUT usado para autenticar (`auth.pass.rut`).

        Respuesta (ejemplo)::

            {
              "data": {
                "pdf": "url del pdf",
                "pdf_base64": "data:application/pdf;base64,...",
                "dte": 39,
                "folio": 40
              },
              "metadata": {"timestamp": "..."}
            }

        :param dict dte: Datos de la boleta a emitir (`vendedor`,
            `Encabezado`, `Detalle`).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, folio y tipo de documento emitido, URL del PDF y PDF en
            base64.
        :rtype: ApiResponse[dict[str, Any]]
        """
        body = {'auth': self._get_auth(), 'dte': dte}
        response = self.client.post('/sii/eboleta/emitidas/emitir', data=body)
        return self._json(response)

    def documento(
        self,
        contribuyente: str,
        folio: int,
        dte: int,
        fecha: str,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Detalle de un documento de la boleta electrónica.

        Respuesta (ejemplo)::

            {
              "data": {
                "folio": 35,
                "neto": 4202,
                "iva": 798,
                "total": 5000,
                "exento": 0,
                "dte": 39,
                "revision_estado": "pendiente",
                "anulado": false,
                "...": "..."
              },
              "metadata": {"timestamp": "..."}
            }

        :param str contribuyente: RUT del contribuyente.
        :param int folio: Folio del documento.
        :param int dte: Tipo de documento.
        :param str fecha: Fecha de emisión del documento (AAAA-MM-DD).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos del documento (montos, estado, revisión, PDF).
        :rtype: ApiResponse[dict[str, Any]]
        """
        response = self.client.post(
            '/sii/eboleta/emitidas/documento',
            data=self._body_documento(contribuyente, folio, dte, fecha),
        )
        return self._json(response)

    def pdf(
        self,
        contribuyente: str,
        folio: int,
        dte: int,
        fecha: str,
    ) -> bytes:
        """
        PDF de un documento de la boleta electrónica.

        :param str contribuyente: RUT del contribuyente.
        :param int folio: Folio del documento.
        :param int dte: Tipo de documento.
        :param str fecha: Fecha de emisión del documento (AAAA-MM-DD).
        :return: Contenido del PDF del documento.
        :rtype: bytes
        """
        response = self.client.post(
            '/sii/eboleta/emitidas/pdf',
            data=self._body_documento(contribuyente, folio, dte, fecha),
        )
        return response.content

    def email(
        self,
        contribuyente: str,
        folio: int,
        dte: int,
        fecha: str,
        to: str,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Envía por correo electrónico un documento de la boleta.

        Respuesta (ejemplo)::

            {
              "data": {"mensaje": "Email enviado con éxito"},
              "metadata": {"timestamp": "..."}
            }

        :param str contribuyente: RUT del contribuyente.
        :param int folio: Folio del documento.
        :param int dte: Tipo de documento.
        :param str fecha: Fecha de emisión del documento (AAAA-MM-DD).
        :param str to: Dirección de correo de destino.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, mensaje de confirmación del envío.
        :rtype: ApiResponse[dict[str, Any]]
        """
        body = self._body_documento(contribuyente, folio, dte, fecha)
        body['to'] = to
        response = self.client.post('/sii/eboleta/emitidas/email', data=body)
        return self._json(response)
