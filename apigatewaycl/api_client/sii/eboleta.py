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
de eBoleta <https://developers.apigateway.cl/>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class EboletaContribuyente(ApiBase):
    """
    Cliente para información de contribuyentes emisores de eBoleta.

    :param str identificador: Identificador del contribuyente.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    def __init__(self, identificador: str, clave: str, **kwargs: str) -> None:
        """Autentica con `identificador`/`clave` del contribuyente."""
        super().__init__(
            identificador=identificador,
            clave=clave,
            **kwargs,  # type: ignore[arg-type]
        )

    def emisor(self, emisor: str) -> Any:
        """
        Información del emisor de la boleta electrónica.

        :param str emisor: RUT del emisor (formato 11222333-K).
        :return: Datos del contribuyente, sus sucursales y usuarios.
        :rtype: dict
        """
        # TODO: Implementar.

    def emisores_autorizados(self) -> Any:
        """
        Lista de emisores autorizados de la boleta electrónica.

        :return: Listado de contribuyentes (RUT, DV y razón social).
        :rtype: list[dict]
        """
        # TODO: Implementar.


class EboletaEmitidas(ApiBase):
    """
    Cliente para boletas electrónicas emitidas de eBoleta.

    :param str identificador: Identificador del contribuyente.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    def __init__(self, identificador: str, clave: str, **kwargs: str) -> None:
        """Autentica con `identificador`/`clave` del contribuyente."""
        super().__init__(
            identificador=identificador,
            clave=clave,
            **kwargs,  # type: ignore[arg-type]
        )

    def documentos(
        self,
        contribuyente: str,
        date_from: str,
        date_to: str,
        page: int | None = None,
        items_per_page: int | None = None,
        estado: str | None = None,
    ) -> Any:
        """
        Listado de documentos emitidos de la boleta electrónica.

        :param str contribuyente: RUT del contribuyente, sin puntos ni
            dígito verificador.
        :param str date_from: Fecha de inicio (AAAA-MM-DD).
        :param str date_to: Fecha de fin (AAAA-MM-DD).
        :param int page: Página a obtener (por defecto `1`).
        :param int items_per_page: Ítems por página (por defecto
            `10`).
        :param str estado: Estado del documento (por defecto
            `emitido`).
        :return: Listado de documentos emitidos y `metadata` de la
            consulta.
        :rtype: dict
        """
        # TODO: Implementar.

    def emitir(self, dte: dict[str, Any]) -> Any:
        """
        Emite una Boleta Electrónica Afecta (39) o Exenta (41).

        Solo admite un ítem por documento. `dte['vendedor']` debe ser
        el mismo RUT usado para autenticar (`auth.pass.rut`).

        :param dict dte: Datos de la boleta a emitir (`vendedor`,
            `Encabezado`, `Detalle`).
        :return: Folio y tipo de documento emitido, URL del PDF y PDF
            en base64.
        :rtype: dict
        """
        # TODO: Implementar.

    def documento(
        self, contribuyente: str, folio: int, dte: int, fecha: str
    ) -> Any:
        """
        Detalle de un documento de la boleta electrónica.

        :param str contribuyente: RUT del contribuyente.
        :param int folio: Folio del documento.
        :param int dte: Tipo de documento.
        :param str fecha: Fecha de emisión del documento (AAAA-MM-DD).
        :return: Datos del documento (montos, estado, revisión, PDF).
        :rtype: dict
        """
        # TODO: Implementar.

    def pdf(self, contribuyente: str, folio: int, dte: int, fecha: str) -> Any:
        """
        PDF de un documento de la boleta electrónica.

        :param str contribuyente: RUT del contribuyente.
        :param int folio: Folio del documento.
        :param int dte: Tipo de documento.
        :param str fecha: Fecha de emisión del documento (AAAA-MM-DD).
        :return: PDF del documento codificado en base64.
        :rtype: bytes
        """
        # TODO: Implementar.

    def email(
        self,
        contribuyente: str,
        folio: int,
        dte: int,
        fecha: str,
        to: str,
    ) -> Any:
        """
        Envía por correo electrónico un documento de la boleta.

        :param str contribuyente: RUT del contribuyente.
        :param int folio: Folio del documento.
        :param int dte: Tipo de documento.
        :param str fecha: Fecha de emisión del documento (AAAA-MM-DD).
        :param str to: Dirección de correo de destino.
        :return: Mensaje de confirmación del envío.
        :rtype: dict
        """
        # TODO: Implementar.
