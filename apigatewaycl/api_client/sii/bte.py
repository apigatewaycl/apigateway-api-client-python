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
Módulo para la emisión de Boletas de Terceros Electrónicas del SII.

Para más información sobre la API, consulte la `documentación completa de las
BTE <https://developers.apigateway.cl/#e08f50ab-5509-48ab-81ab-63fc8e5985e1>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class BteEmitidas(ApiBase):
    """
    Cliente para Boletas de Terceros Electrónicas (BTE) emitidas.

    Provee métodos para emitir, anular, y consultar información
    relacionada con BTEs.

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
        self, emisor: str, periodo: str, pagina: int | None = None
    ) -> Any:
        """
        Obtiene los documentos BTE emitidos por un emisor en un periodo.

        :param str emisor: RUT del emisor de las BTE.
        :param str periodo: Período de las BTE emitidas.
        :return: Respuesta JSON con los documentos BTE.
        :rtype: list[dict]
        """
        url = '/sii/bte/emitidas/documentos/%(emisor)s/%(periodo)s' % {
            'emisor': emisor,
            'periodo': periodo,
        }
        if pagina is not None:
            url += '?pagina=%(pagina)s' % {
                'pagina': pagina,
            }
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def resumen(self, emisor: str, anio: str) -> Any:
        """
        Resumen anual y mensual de boletas de terceros emitidas.

        :param str emisor: RUT del emisor de las BTE.
        :param str anio: Año del resumen.
        :return: Resumen anual y, por cada mes, su propio resumen.
        :rtype: dict
        """
        # TODO: Implementar.

    def html(self, codigo: str) -> bytes:
        """
        Obtiene la representación HTML de una BTE emitida.

        :param str codigo: Código único de la BTE.
        :return: Contenido HTML de la BTE.
        :rtype: str
        """
        url = '/sii/bte/emitidas/html/%(codigo)s' % {'codigo': codigo}
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.content

    def emitir(self, datos: dict[str, Any]) -> Any:
        """
        Emite una nueva Boleta de Tercero Electrónica.

        :param dict datos: Datos de la boleta a emitir.
        :return: Respuesta JSON con la confirmación de la emisión de la BTE.
        :rtype: dict
        """
        body = {'auth': self._get_auth_pass(), 'boleta': datos}
        response = self.client.post('/sii/bte/emitidas/emitir', data=body)
        return response.json()

    def anular(
        self,
        emisor: str,
        numero: str,
        causa: int = 3,
        periodo: str | None = None,
    ) -> Any:
        """
        Anula una BTE emitida.

        :param str emisor: RUT del emisor de la boleta.
        :param str numero: Número de la boleta.
        :param int causa: Causa de anulación.
        :param str periodo: Período de emisión de la boleta (opcional).
        :return: Respuesta JSON con la confirmación de la anulación.
        :rtype: dict
        """
        body = {'auth': self._get_auth_pass()}
        url = (
            '/sii/bte/emitidas/anular/%(emisor)s/%(numero)s?causa=%(causa)s'
            % {'emisor': emisor, 'numero': numero, 'causa': causa}
        )
        if periodo:
            url += '&periodo=%(periodo)s' % {'periodo': periodo}
        response = self.client.post(url, data=body)
        return response.json()

    def documento(
        self, emisor: str, folio: int, periodo: str | None = None
    ) -> Any:
        """
        Detalle de una BTE emitida específica (no un listado).

        :param str emisor: RUT del emisor.
        :param int folio: Folio de la boleta.
        :param str periodo: Período de la boleta (AAAAMM), opcional.
        :return: Datos de la boleta (número, código, montos, estado).
        :rtype: dict
        """
        # TODO: Implementar.

    def receptor_tasa(
        self, emisor: str, receptor: str, periodo: str | None = None
    ) -> Any:
        """
        Obtiene la tasa de retención aplicada a un receptor por un emisor.

        :param str emisor: RUT del emisor de la boleta.
        :param str receptor: RUT del receptor de la boleta.
        :param str periodo: Período de emisión de la boleta (opcional).
        :return: Respuesta JSON con la tasa de retención.
        :rtype: dict
        """
        body = {'auth': self._get_auth_pass()}
        url = '/sii/bte/emitidas/receptor_tasa/%(emisor)s/%(receptor)s' % {
            'emisor': emisor,
            'receptor': receptor,
        }
        if periodo:
            url += '?periodo=%(periodo)s' % {'periodo': periodo}
        response = self.client.post(url, data=body)
        return response.json()


class BteRecibidas(ApiBase):
    """
    Cliente para Boletas de Terceros Electrónicas (BTE) recibidas.

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

    def documentos(self, receptor: str, periodo: str, pagina: int) -> Any:
        """
        Obtiene los documentos BTE recibidos por un receptor en un periodo.

        `periodo` acepta AAAAMM (mensual) o AAAAMMDD (diario).
        Paginado — `pagina` parte en `1`.

        :param str receptor: RUT del receptor de las BTE.
        :param str periodo: Período de las BTE buscadas.
        :param int pagina: Página a consultar, partiendo desde `1`.
        :return: Boletas y `metadata` (n_boletas, n_paginas).
        :rtype: dict
        """
        # TODO: Implementar.

    def html(self, codigo: str) -> Any:
        """
        Obtiene la representación HTML de una BTE recibida.

        :param str codigo: Código único de la BTE recibida.
        :return: Contenido HTML de la BTE.
        :rtype: str
        """
        # TODO: Implementar.
