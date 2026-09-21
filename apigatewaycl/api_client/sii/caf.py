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
Módulo para el Código de Asignación de Folios (CAF) del SII.

Para más información sobre la API, consulte la `documentación completa
del CAF <https://developers.apigateway.cl/>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class Caf(ApiBase):
    """
    Cliente para el Código de Asignación de Folios (CAF) de la API.

    Provee métodos para consultar, solicitar y anular folios.

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

    def estado_timbraje(self, emisor: str, dte: int) -> Any:
        """
        Estado de timbraje de un tipo de DTE.

        Folios timbrables y observaciones del SII sobre el
        contribuyente. Solo consulta, no solicita folios.

        :param str emisor: RUT del emisor.
        :param int dte: Código del tipo de documento.
        :return: Datos del tipo de DTE y situación del contribuyente.
        :rtype: dict
        """
        # TODO: Implementar.

    def solicitar(
        self,
        emisor: str,
        dte: int,
        cantidad: int,
        certificacion: str | None = None,
    ) -> Any:
        """
        Solicita un nuevo CAF (folios) al SII.

        La respuesta es el XML del CAF, no un objeto JSON.

        :param str emisor: RUT del emisor del CAF.
        :param int dte: Código del tipo de documento.
        :param int cantidad: Cantidad de folios a solicitar.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: XML del CAF.
        :rtype: str
        """
        # TODO: Implementar.

    def xml(
        self,
        emisor: str,
        dte: int,
        folio_inicial: int,
        folio_final: int,
        fecha_autorizacion: str,
        certificacion: str | None = None,
    ) -> Any:
        """
        Obtiene el XML de un CAF ya solicitado.

        :param str emisor: RUT del emisor del CAF.
        :param int dte: Código del tipo de documento.
        :param int folio_inicial: Folio inicial del CAF.
        :param int folio_final: Folio final del CAF.
        :param str fecha_autorizacion: Fecha de autorización del CAF.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: XML del CAF.
        :rtype: str
        """
        # TODO: Implementar.

    def estado(
        self,
        emisor: str,
        dte: int,
        folio: int,
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> Any:
        """
        Estado de un folio en el SII (estado, glosa, track id de envío).

        :param str emisor: RUT del emisor del folio.
        :param int dte: Código del tipo de documento.
        :param int folio: Folio a consultar.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'json'` o `'html'`.
        :return: Estado del folio.
        :rtype: dict
        """
        # TODO: Implementar.

    def anular(
        self,
        emisor: str,
        dte: int,
        folio_inicial: int,
        folio_final: int,
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> Any:
        """
        Anula un rango de folios ya solicitados al SII.

        :param str emisor: RUT del emisor.
        :param int dte: Código del tipo de documento.
        :param int folio_inicial: Primer folio a anular.
        :param int folio_final: Último folio a anular.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'json'` o `'html'`.
        :return: Datos de la anulación (fecha, usuario, rango).
        :rtype: dict
        """
        # TODO: Implementar.

    def solicitudes(
        self,
        emisor: str,
        dte: int,
        pagina: int,
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> Any:
        """
        Listado paginado de solicitudes de CAF de un emisor.

        `pagina` parte en `1` — usar `metadata.siguiente_pagina` de la
        respuesta (`None` si es la última) para paginar.

        :param str emisor: RUT del emisor del CAF.
        :param int dte: Código del tipo de documento.
        :param int pagina: Página a consultar, partiendo desde `1`.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'json'` o `'html'`.
        :return: Listado de solicitudes y `metadata.siguiente_pagina`.
        :rtype: dict
        """
        # TODO: Implementar.

    def estados(
        self,
        emisor: str,
        dte: int,
        folio_inicial: int,
        folio_final: int,
        estado: str,
    ) -> Any:
        """
        Estados de un rango de folios en el SII, agrupados por tramos.

        :param str emisor: RUT del emisor.
        :param int dte: Código del tipo de documento.
        :param int folio_inicial: Primer folio del rango.
        :param int folio_final: Último folio del rango.
        :param str estado: Estado de los folios a consultar.
        :return: Listado de tramos (inicial/final/cantidad).
        :rtype: list[dict]
        """
        # TODO: Implementar.
