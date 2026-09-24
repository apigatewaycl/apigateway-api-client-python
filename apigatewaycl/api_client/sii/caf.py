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
del CAF <https://www.apigateway.cl/docs>`_.
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

    def estado_timbraje(
        self,
        emisor: str,
        dte: int,
        certificacion: str | None = None,
    ) -> Any:
        """
        Estado de timbraje de un tipo de DTE.

        Folios timbrables y observaciones del SII sobre el
        contribuyente. Solo consulta, no solicita folios.

        :param str emisor: RUT del emisor.
        :param int dte: Código del tipo de documento.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos del tipo de DTE y situación del contribuyente.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/caf/estado_timbraje/%(emisor)s/%(dte)s'
            % {'emisor': emisor, 'dte': dte},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()

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
        :return: Contenido del XML del CAF.
        :rtype: bytes
        """
        url = self._build_url(
            '/sii/dte/caf/solicitar/%(emisor)s/%(dte)s/%(cantidad)s'
            % {'emisor': emisor, 'dte': dte, 'cantidad': cantidad},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.content

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
        :return: Contenido del XML del CAF.
        :rtype: bytes
        """
        url = self._build_url(
            '/sii/dte/caf/xml/%(emisor)s/%(dte)s/%(folio_inicial)s'
            '/%(folio_final)s/%(fecha_autorizacion)s'
            % {
                'emisor': emisor,
                'dte': dte,
                'folio_inicial': folio_inicial,
                'folio_final': folio_final,
                'fecha_autorizacion': fecha_autorizacion,
            },
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.content

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
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, estado del folio. Con `formato='html'` la API igual
            responde JSON: el HTML viene como una cadena dentro del cuerpo.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/caf/estado/%(emisor)s/%(dte)s/%(folio)s'
            % {'emisor': emisor, 'dte': dte, 'folio': folio},
            certificacion=certificacion,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()

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
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos de la anulación (fecha, usuario, rango). Con
            `formato='html'` la API igual responde JSON: el HTML viene como una
            cadena dentro del cuerpo.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/caf/anular/%(emisor)s/%(dte)s/%(folio_inicial)s'
            '/%(folio_final)s'
            % {
                'emisor': emisor,
                'dte': dte,
                'folio_inicial': folio_inicial,
                'folio_final': folio_final,
            },
            certificacion=certificacion,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()

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
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, el listado de solicitudes; en `metadata`,
            `siguiente_pagina` (`None` si es la última). Con
            `formato='html'` la API igual responde JSON: el HTML viene
            como una cadena dentro de `data`.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/caf/solicitudes/%(emisor)s/%(dte)s'
            % {'emisor': emisor, 'dte': dte},
            pagina=pagina,
            certificacion=certificacion,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()

    def estados(
        self,
        emisor: str,
        dte: int,
        folio_inicial: int,
        folio_final: int,
        estado: str,
        certificacion: str | None = None,
    ) -> Any:
        """
        Estados de un rango de folios en el SII, agrupados por tramos.

        :param str emisor: RUT del emisor.
        :param int dte: Código del tipo de documento.
        :param int folio_inicial: Primer folio del rango.
        :param int folio_final: Último folio del rango.
        :param str estado: Estado de los folios a consultar: `recibidos`,
            `anulados` o `pendientes`.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de tramos (inicial/final/cantidad).
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/caf/estados/%(emisor)s/%(dte)s/%(folio_inicial)s'
            '/%(folio_final)s/%(estado)s'
            % {
                'emisor': emisor,
                'dte': dte,
                'folio_inicial': folio_inicial,
                'folio_final': folio_final,
                'estado': estado,
            },
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()
