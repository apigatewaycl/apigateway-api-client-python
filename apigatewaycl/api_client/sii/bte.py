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
BTE <https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase, Respuesta


class BteEmitidas(ApiBase):
    """
    Cliente para Boletas de Terceros Electrónicas (BTE) emitidas.

    Provee métodos para emitir, anular, y consultar información
    relacionada con BTEs.

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

    def documentos(
        self,
        emisor: str,
        periodo: str,
        pagina: int = 1,
    ) -> Respuesta[list[dict[str, Any]]]:
        """
        Obtiene los documentos BTE emitidos por un emisor en un periodo.

        La API exige `pagina`: parte en `1` y se avanza de a una.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "numero": 123,
                  "codigo": "C76192083000123D09D17",
                  "emisor_rut": "76192083-9",
                  "emisor_nombre": "EMPRESA SPA",
                  "receptor_rut": "12345678-9",
                  "receptor_nombre": "RECEPTOR EJEMPLO",
                  "fecha": "2025-01-15",
                  "fecha_emision": "2025-01-15",
                  "...": "..."
                }
              ],
              "metadata": {"timestamp": "...", "n_boletas": 1, "n_paginas": 1}
            }

        :param str emisor: RUT del emisor de las BTE.
        :param str periodo: Período de las BTE emitidas.
        :param int pagina: Página a consultar, partiendo desde `1`.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, documentos BTE.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/bte/emitidas/documentos/%(emisor)s/%(periodo)s'
            % {'emisor': emisor, 'periodo': periodo},
            pagina=pagina,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def resumen(
        self,
        emisor: str,
        anio: str,
    ) -> Respuesta[dict[str, Any]]:
        """
        Resumen anual y mensual de boletas de terceros emitidas.

        Respuesta (ejemplo)::

            {
              "data": {
                "anual": {
                  "anuladas": 2,
                  "bruto": 500000,
                  "folio_final": 150,
                  "folio_inicial": 100,
                  "retencion": 50000,
                  "total": 450000,
                  "vigentes": 48
                },
                "mensual": [
                  {
                    "anuladas": 0,
                    "bruto": 100000,
                    "folio_final": 110,
                    "folio_inicial": 100,
                    "mes_codigo": "01",
                    "...": "..."
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor de las BTE.
        :param str anio: Año del resumen.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, resumen anual (`anual`) y, por cada mes, su propio
            resumen (`mensual`). Sin movimientos en el año, `anual` es
            `None` y `mensual` una lista vacía.
        :rtype: dict
        """
        url = '/sii/bte/emitidas/resumen/%(emisor)s/%(anio)s' % {
            'emisor': emisor,
            'anio': anio,
        }
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def html(self, codigo: str) -> bytes:
        """
        Obtiene la representación HTML de una BTE emitida.

        :param str codigo: Código único de la BTE.
        :return: Contenido HTML de la BTE, sin decodificar (viene en
            ISO-8859-1).
        :rtype: bytes
        """
        url = '/sii/bte/emitidas/html/%(codigo)s' % {'codigo': codigo}
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.content

    def emitir(self, datos: dict[str, Any]) -> Respuesta[dict[str, Any]]:
        """
        Emite una nueva Boleta de Tercero Electrónica.

        Respuesta (ejemplo)::

            {
              "data": {
                "Encabezado": {
                  "Emisor": {
                    "RUTEmisor": "76192083-9",
                    "RznSoc": "EMPRESA EMISORA SPA",
                    "GiroEmis": "SERVICIOS DE INFORMATICA",
                    "Acteco": "620200",
                    "DirOrigen": "AV. PRINCIPAL 123",
                    "...": "..."
                  },
                  "IdDoc": {
                    "FchEmis": "2025-01-15",
                    "Folio": 336,
                    "CodigoBarras": "C76192083000336D09D17"
                  },
                  "Receptor": {
                    "RUTRecep": "12345678-9",
                    "RznSocRecep": "Contribuyente Receptor",
                    "DirRecep": "Av. Principal 123",
                    "CmnaRecep": "Santiago"
                  },
                  "Totales": {
                    "MntBruto": 150000,
                    "TasaRetencion": 14.5,
                    "MntRetencion": 21750,
                    "MntNeto": 128250
                  }
                },
                "Detalle": [
                  {"NmbItem": "Servicio de consultoría", "MontoItem": 50000}
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param dict datos: Datos de la boleta a emitir.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, confirmación de la emisión de la BTE.
        :rtype: dict
        """
        body = {'auth': self._get_auth(), 'boleta': datos}
        response = self.client.post('/sii/bte/emitidas/emitir', data=body)
        return self._json(response)

    def anular(
        self,
        emisor: str,
        numero: str,
        causa: int = 3,
        periodo: str | None = None,
    ) -> Respuesta[dict[str, Any]]:
        """
        Anula una BTE emitida.

        Respuesta (ejemplo)::

            {
              "data": {
                "numero": 123,
                "fecha": null,
                "emisor_rut": "12345678-9",
                "emisor_nombre": "EMISOR",
                "fecha_emision": "2025-01-01",
                "receptor_rut": "66666666",
                "receptor_nombre": "RECEPTOR",
                "total_honorarios": 1000000,
                "...": "..."
              },
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor de la boleta.
        :param str numero: Número de la boleta.
        :param int causa: Causa de anulación.
        :param str periodo: Período de emisión de la boleta (opcional).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, confirmación de la anulación.
        :rtype: dict
        """
        body = {'auth': self._get_auth()}
        url = (
            '/sii/bte/emitidas/anular/%(emisor)s/%(numero)s?causa=%(causa)s'
            % {'emisor': emisor, 'numero': numero, 'causa': causa}
        )
        if periodo:
            url += '&periodo=%(periodo)s' % {'periodo': periodo}
        response = self.client.post(url, data=body)
        return self._json(response)

    def documento(
        self,
        emisor: str,
        folio: int,
        periodo: str,
    ) -> Respuesta[dict[str, Any]]:
        """
        Detalle de una BTE emitida específica (no un listado).

        Respuesta (ejemplo)::

            {
              "data": {
                "codigo": "123ADSA45FSA67890",
                "emisor_nombre": "API Gateway",
                "emisor_rut": "76192083-9",
                "estado": "ANUL",
                "fecha": "2019-12-22",
                "fecha_emision": "2019-12-22",
                "numero": "123",
                "receptor_nombre": "RECEPTOR",
                "...": "..."
              },
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor.
        :param int folio: Folio de la boleta.
        :param str periodo: Período de la boleta (AAAAMM). Acota la
            consulta a ese mes: sin él, el SII se recorre año por año
            buscando el folio.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos de la boleta (número, código, montos, estado).
        :rtype: dict
        """
        url = self._build_url(
            '/sii/bte/emitidas/documento/%(emisor)s/%(folio)s'
            % {'emisor': emisor, 'folio': folio},
            periodo=periodo,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def receptor_tasa(
        self,
        emisor: str,
        receptor: str,
        periodo: str | None = None,
    ) -> Respuesta[dict[str, Any]]:
        """
        Obtiene la tasa de retención aplicada a un receptor por un emisor.

        Respuesta (ejemplo)::

            {
              "data": {
                "periodo": 202501,
                "tasa_base": 11.5,
                "tasa_receptor": 11.5
              },
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor de la boleta.
        :param str receptor: RUT del receptor de la boleta.
        :param str periodo: Período de emisión de la boleta (opcional).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, tasa de retención.
        :rtype: dict
        """
        body = {'auth': self._get_auth()}
        url = '/sii/bte/emitidas/receptor_tasa/%(emisor)s/%(receptor)s' % {
            'emisor': emisor,
            'receptor': receptor,
        }
        if periodo:
            url += '?periodo=%(periodo)s' % {'periodo': periodo}
        response = self.client.post(url, data=body)
        return self._json(response)


class BteRecibidas(ApiBase):
    """
    Cliente para Boletas de Terceros Electrónicas (BTE) recibidas.

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

    def documentos(
        self,
        receptor: str,
        periodo: str,
        pagina: int,
    ) -> Respuesta[list[dict[str, Any]]]:
        """
        Obtiene los documentos BTE recibidos por un receptor en un periodo.

        `periodo` acepta AAAAMM (mensual) o AAAAMMDD (diario).
        Paginado — `pagina` parte en `1`.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "numero": 123,
                  "fecha": "2025-01-15",
                  "emisor_rut": "76192083-9",
                  "emisor_nombre": "EMPRESA SPA",
                  "fecha_emision": "2025-01-15",
                  "receptor_rut": "12345678-9",
                  "receptor_nombre": "RECEPTOR EJEMPLO",
                  "total_honorarios": 150000,
                  "...": "..."
                }
              ],
              "metadata": {
                "timestamp": "...",
                "n_boletas": 150,
                "n_paginas": 15
              }
            }

        :param str receptor: RUT del receptor de las BTE.
        :param str periodo: Período de las BTE buscadas.
        :param int pagina: Página a consultar, partiendo desde `1`.
        :return: Respuesta de la API, con `data` y `metadata`. En
            `data`, la lista de boletas; en `metadata`, `n_boletas` y
            `n_paginas`.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/bte/recibidas/documentos/%(receptor)s/%(periodo)s'
            % {'receptor': receptor, 'periodo': periodo},
            pagina=pagina,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def html(self, codigo: str) -> bytes:
        """
        Obtiene la representación HTML de una BTE recibida.

        :param str codigo: Código único de la BTE recibida.
        :return: Contenido HTML de la BTE, sin decodificar (viene en
            ISO-8859-1).
        :rtype: bytes
        """
        url = '/sii/bte/recibidas/html/%(codigo)s' % {'codigo': codigo}
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.content
