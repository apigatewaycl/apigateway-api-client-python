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
del RTC <https://developers.apigateway.cl/>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class Cesiones(ApiBase):
    """
    Cliente para cesiones de DTE (factoring) del RTC de la API.

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

    def certificado(
        self,
        emisor: str,
        dte: str,
        folio: str,
        fecha: str,
        certificacion: str | None = None,
    ) -> Any:
        """
        Certificado de cesión de un DTE, con cedente/cesionario/fecha.

        La respuesta es el certificado del SII en HTML, no un objeto
        JSON.

        :param str emisor: RUT del emisor del documento.
        :param str dte: Código del tipo de documento.
        :param str folio: Folio del documento.
        :param str fecha: Fecha de emisión del documento (AAAA-MM-DD).
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Certificado de cesión en HTML.
        :rtype: str
        """
        # TODO: Implementar.

    def estado_envio(
        self, track_id: str, certificacion: str | None = None
    ) -> Any:
        """
        Estado de envío de una cesión.

        :param str track_id: ID de la cesión.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Estado del envío y track id.
        :rtype: dict
        """
        # TODO: Implementar.

    def estado(
        self,
        emisor: str,
        dte: str,
        folio: str,
        certificacion: str | None = None,
    ) -> Any:
        """
        Estado de cesión de un DTE (si está o no cedido, tenedor vigente).

        :param str emisor: RUT del emisor del documento.
        :param str dte: Código del tipo de documento.
        :param str folio: Folio del documento.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Estado de la cesión (y detalle, si hay tenedor vigente).
        :rtype: dict
        """
        # TODO: Implementar.

    def documentos(
        self,
        desde: str,
        hasta: str,
        consulta: str,
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> Any:
        """
        Listado de documentos cedidos en un período (máximo 1 mes).

        Requiere autenticación de un contribuyente relacionado con la
        cesión (deudor, cedente o cesionario) o su representante.

        :param str desde: Fecha de inicio (AAAA-MM-DD).
        :param str hasta: Fecha de fin, máximo 30 días desde `desde`
            (AAAA-MM-DD).
        :param str consulta: `'0'` deudor, `'1'` cedente, `'2'`
            cesionario.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'xml'`, `'csv'` o `'txt'` — de no
            indicarse, la respuesta es JSON.
        :return: Listado de cesiones del período.
        :rtype: list[dict]
        """
        # TODO: Implementar.
