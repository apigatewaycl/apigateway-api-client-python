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
Módulo para consultas al Portal MIPYME del SII.

Para más información sobre la API, consulte la `documentación completa del
Portal MIPYME <https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from abc import ABC
from typing import Any, ClassVar

from .. import ApiBase


class PortalMipyme(ApiBase, ABC):
    """
    Base para los clientes específicos del Portal Mipyme.

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


class Contribuyentes(PortalMipyme):
    """
    Cliente para los endpoints de contribuyentes del Portal Mipyme.

    :param str identificador: Identificador del contribuyente.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    def info(
        self,
        contribuyente: str,
        emisor: str,
        dte: int = 33,
    ) -> Any:
        """
        Obtiene información de un contribuyente específico.

        :param str contribuyente: RUT del contribuyente.
        :param str emisor: RUT del emisor del DTE.
        :param int dte: Tipo de DTE.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos del contribuyente.
        :rtype: dict
        """
        url = (
            '/sii/mipyme/contribuyentes/info/'
            '%(contribuyente)s/%(emisor)s/%(dte)s'
            % {'contribuyente': contribuyente, 'emisor': emisor, 'dte': dte}
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()


class Dte(PortalMipyme):
    """
    Base para los clientes específicos de DTE del Portal Mipyme.

    Incluye constantes para diferentes estados de DTE.

    :param str identificador: Identificador del contribuyente.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    ESTADO_EMITIDO = 'EMI'  # Documento emitido
    ESTADO_BORRADOR = 'PRV'  # Borrador (pre-view) de documento
    ESTADO_CERTIFICADO_RECHAZADO = 'DCD'  # Certificado rechazado
    ESTADO_EMISOR_INVALIDO = 'DEI'  # RUT emisor inválido
    ESTADO_FOLIO_INVALIDO = 'DFI'  # Folio DTE inválido
    ESTADO_INCOMPLETO = 'DIN'  # Incompleto
    ESTADO_FIRMA_SIN_PERMISO = 'DPF'  # Sin permiso de firma
    ESTADO_FIRMA_RECHAZADA = 'DRF'  # DTE rechazado por firma
    ESTADO_RECEPTOR_INVALIDO = 'DRI'  # RUT receptor inválido
    ESTADO_REPETIDO = 'DRR'  # Rechazado por repetido
    ESTADO_INICIALIZADO = 'INI'  # DTE inicializado
    ESTADO_ACEPTADO = 'RAC'  # DTE aceptado por receptor
    ESTADO_DISCREPANCIAS = 'RAD'  # DTE aceptado con discrepancias
    ESTADO_NO_RECIBIDO = 'RNR'  # DTE no recibido por receptor
    ESTADO_RECIBIDO = 'RRC'  # DTE recibido por receptor
    ESTADO_ACEPTADO_LEY_19983 = 'RAL'  # DTE aceptado Ley 19.983
    ESTADO_RECHAZADO_RECEPTOR = 'RRH'  # DTE rechazado por receptor
    ESTADO_SIN_REPAROS = 'RSR'  # Recibido sin reparos

    DTE_TIPOS: ClassVar[dict[str, str]] = {
        '33': '33',
        '34': '34',
        '35': '35',
        '36': '36',
        '37': '37',
        '38': '38',
        '39': '39',
    }

    def get_codigo_dte(self, tipo: str) -> str:
        """
        Obtiene el código correspondiente al tipo de DTE.

        :param str tipo: Tipo de DTE.
        :return: Código del DTE.
        :rtype: str
        """
        if tipo in self.DTE_TIPOS:
            return self.DTE_TIPOS[tipo]
        return tipo.replace(' ', '-')


class Borradores(Dte):
    """
    Cliente para documentos borradores del Portal Mipyme.

    Un borrador es un DTE armado en el Portal MIPYME del SII, antes
    de convertirse en un documento emitido de verdad.

    :param str identificador: Identificador del contribuyente.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    def documentos(
        self,
        emisor: str,
        filtros: dict[str, Any] | None = None,
    ) -> Any:
        """
        Listado de documentos borradores del emisor.

        Por defecto entrega todos los borradores, ordenados por fecha
        ascendente. Para paginar se indica `NUM_PAG` en `filtros` (100
        borradores por página) y `metadata.n_paginas` dice cuántas páginas
        hay con los filtros usados.

        Filtros disponibles: `NUM_PAG`, `CODIGO` (código del borrador),
        `TPO_DOC` (código de DTE), `RUT_RECP` (RUT del receptor, con o sin
        dígito verificador), `RZN_SOC` (razón social del receptor, o parte
        de ella), `FEC_DESDE` y `FEC_HASTA` (AAAA-MM-DD) y `ORDEN`
        (`FecAsc` o `FecDesc`).

        :param str emisor: RUT del emisor de los documentos.
        :param dict filtros: Filtros de búsqueda (opcional).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de borradores con los campos del Portal
            MIPYME en minúsculas; el código del borrador es `ehdr_codigo`.
        :rtype: dict
        """
        url = '/sii/mipyme/borradores/documentos/%(emisor)s' % {
            'emisor': emisor,
        }
        body = {'auth': self._get_auth(), 'filtros': filtros or {}}
        response = self.client.post(url, data=body)
        return response.json()

    def emitir(self, dte: dict[str, Any]) -> Any:
        """
        Crea un documento borrador en el Portal Mipyme.

        No emite un DTE real ante el SII — el borrador se confirma
        luego desde el propio Portal MIPYME.

        :param dict dte: Datos del DTE a armar como borrador.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, el borrador creado.
        :rtype: dict
        """
        body = {'auth': self._get_auth(), 'dte': dte}
        response = self.client.post('/sii/mipyme/borradores/emitir', data=body)
        return response.json()

    def eliminar(
        self,
        emisor: str,
        codigo: str,
    ) -> Any:
        """
        Elimina un documento borrador del Portal Mipyme.

        :param str emisor: RUT del emisor de los documentos.
        :param str codigo: Código del borrador (del listado de documentos).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, `True` si el borrador fue eliminado.
        :rtype: dict
        """
        url = '/sii/mipyme/borradores/eliminar/%(emisor)s/%(codigo)s' % {
            'emisor': emisor,
            'codigo': codigo,
        }
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()


class DteEmitidos(Dte):
    """
    Cliente específico para gestionar DTE emitidos en el Portal Mipyme.

    :param str identificador: Identificador del contribuyente.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    def documentos(
        self,
        emisor: str,
        filtros: dict[str, Any] | None = None,
    ) -> Any:
        """
        Obtiene documentos de DTE emitidos por un emisor.

        :param str emisor: RUT del emisor.
        :param dict filtros: Filtros adicionales para la consulta.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, documentos de DTE emitidos.
        :rtype: dict
        """
        url = '/sii/mipyme/emitidos/documentos/%(emisor)s' % {'emisor': emisor}
        body = {'auth': self._get_auth(), 'filtros': filtros or {}}
        response = self.client.post(url, data=body)
        return response.json()

    def pdf(self, emisor: str, codigo: str) -> bytes:
        """
        Obtiene el PDF de un DTE emitido.

        El documento se identifica por su `codigo`, que entrega el
        listado de `documentos()`; no por tipo de DTE y folio.

        :param str emisor: RUT del emisor.
        :param str codigo: Código del DTE emitido.
        :return: Contenido del PDF del DTE emitido.
        :rtype: bytes
        """
        url = '/sii/mipyme/emitidos/pdf/%(emisor)s/%(codigo)s' % {
            'emisor': emisor,
            'codigo': codigo,
        }
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.content

    def xml(
        self,
        emisor: str,
        dte: str,
        folio: str,
        fecha_emision: str,
    ) -> bytes:
        """
        Obtiene el XML de un DTE emitido.

        :param str emisor: RUT del emisor.
        :param str dte: Tipo de DTE.
        :param str folio: Número de folio del DTE.
        :param str fecha_emision: Fecha de emisión del documento
            (AAAA-MM-DD). Sin ella el Portal MIPYME no ubica el
            documento y la API no entrega el XML.
        :return: Contenido del XML del DTE emitido, sin decodificar.
        :rtype: bytes
        """
        url = self._build_url(
            '/sii/mipyme/emitidos/xml/%(emisor)s/%(dte)s/%(folio)s'
            % {'emisor': emisor, 'dte': dte, 'folio': folio},
            fecha_emision=fecha_emision,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.content


class DteRecibidos(Dte):
    """
    Cliente para DTE recibidos en el Portal Mipyme.

    Proporciona métodos para obtener documentos, PDF y XML de DTE
    recibidos.

    :param str identificador: Identificador del contribuyente.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    def documentos(
        self,
        receptor: str,
        filtros: dict[str, Any] | None = None,
    ) -> Any:
        """
        Obtiene documentos de DTE recibidos por un receptor.

        :param str receptor: RUT del receptor.
        :param dict filtros: Filtros adicionales para la consulta.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, documentos de DTE recibidos.
        :rtype: dict
        """
        url = '/sii/mipyme/recibidos/documentos/%(receptor)s' % {
            'receptor': receptor
        }
        body = {'auth': self._get_auth(), 'filtros': filtros or {}}
        response = self.client.post(url, data=body)
        return response.json()

    def pdf(self, receptor: str, codigo: str) -> bytes:
        """
        Obtiene el PDF de un DTE recibido.

        El documento se identifica por su `codigo`, que entrega el
        listado de `documentos()`; no por emisor, tipo de DTE y folio.

        :param str receptor: RUT del receptor.
        :param str codigo: Código del DTE recibido.
        :return: Contenido del PDF del DTE recibido.
        :rtype: bytes
        """
        url = '/sii/mipyme/recibidos/pdf/%(receptor)s/%(codigo)s' % {
            'receptor': receptor,
            'codigo': codigo,
        }
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.content

    def xml(
        self,
        receptor: str,
        emisor: str,
        dte: str,
        folio: str,
        fecha_emision: str,
    ) -> bytes:
        """
        Obtiene el XML de un DTE recibido.

        :param str receptor: RUT del receptor.
        :param str emisor: RUT del emisor.
        :param str dte: Tipo de DTE.
        :param str folio: Número de folio del DTE.
        :param str fecha_emision: Fecha de emisión del documento
            (AAAA-MM-DD). Sin ella el Portal MIPYME no ubica el
            documento y la API no entrega el XML.
        :return: Contenido del XML del DTE recibido, sin decodificar.
        :rtype: bytes
        """
        url = self._build_url(
            '/sii/mipyme/recibidos/xml/'
            '%(receptor)s/%(emisor)s/%(dte)s/%(folio)s'
            % {
                'receptor': receptor,
                'emisor': emisor,
                'dte': dte,
                'folio': folio,
            },
            fecha_emision=fecha_emision,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.content
