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
Módulo para Boletas de Honorarios Electrónicas, emitidas y recibidas.

Para más información sobre la API, consulte la `documentación completa
de las BHE
<https://developers.apigateway.cl/#4df9775f-2cd3-4b35-80a5-373f2501230c>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class BheEmitidas(ApiBase):
    """
    Cliente para Boletas de Honorarios Electrónicas (BHE) emitidas.

    Provee métodos para emitir, anular, y consultar información
    relacionada con BHEs.

    :param str identificador: Identificador del contribuyente.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    # Quién debe hacer la retención asociada al honorario para pagar al SII
    RETENCION_RECEPTOR = 1
    RETENCION_EMISOR = 2

    # Posibles motivos de anulación de una BHE
    ANULACION_CAUSA_SIN_PAGO = 1
    ANULACION_CAUSA_SIN_PRESTACION = 2
    ANULACION_CAUSA_ERROR_DIGITACION = 3

    def __init__(self, identificador: str, clave: str, **kwargs: str) -> None:
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
        pagina: int | None = None,
        pagina_sig_codigo: str | None = None,
    ) -> Any:
        """
        Obtiene los documentos de BHE emitidos por un emisor en un periodo.

        :param str emisor: RUT del emisor de las boletas.
        :param str periodo: Período de tiempo de las boletas emitidas.
        :return: Respuesta JSON con los documentos de BHE.
        :rtype: list[dict]
        """
        url = '/sii/bhe/emitidas/documentos/%(emisor)s/%(periodo)s' % {
            'emisor': emisor,
            'periodo': periodo,
        }
        if pagina is not None:
            url += '?pagina=%(pagina)s' % {
                'pagina': pagina,
            }
            if pagina_sig_codigo:
                url += '&pagina_sig_codigo=%(pagina_sig_codigo)s' % {
                    'pagina_sig_codigo': pagina_sig_codigo or '0'
                }
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def emitir(self, boleta: dict[str, Any]) -> Any:
        """
        Emite una nueva Boleta de Honorarios Electrónica.

        :param dict boleta: Información detallada de la boleta a emitir.
        :return: Respuesta JSON con la confirmación de la emisión.
        :rtype: dict
        """
        body = {'auth': self._get_auth_pass(), 'boleta': boleta}
        response = self.client.post('/sii/bhe/emitidas/emitir', data=body)
        return response.json()

    def pdf(self, codigo: str) -> bytes:
        """
        Obtiene el PDF de una BHE emitida.

        :param str codigo: Código único de la BHE.
        :return: Contenido del PDF de la BHE.
        :rtype: bytes
        """
        url = '/sii/bhe/emitidas/pdf/%(codigo)s' % {'codigo': codigo}
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.content

    def email(self, codigo: str, email: str) -> Any:
        """
        Envía por correo electrónico una BHE emitida.

        :param str codigo: Código único de la BHE a enviar.
        :param str email: Dirección de correo a la cual enviar la BHE.
        :return: Respuesta JSON con la confirmación del envío.
        :rtype: dict
        """
        url = '/sii/bhe/emitidas/email/%(codigo)s' % {'codigo': codigo}
        body = {
            'auth': self._get_auth_pass(),
            'destinatario': {'email': email},
        }
        response = self.client.post(url, data=body)
        return response.json()

    def anular(
        self,
        emisor: str,
        folio: str,
        causa: int = ANULACION_CAUSA_ERROR_DIGITACION,
    ) -> Any:
        """
        Anula una BHE emitida.

        :param str emisor: RUT del emisor de la boleta.
        :param str folio: Número de folio de la boleta.
        :param int causa: Motivo de anulación de la boleta.
        :return: Respuesta JSON con la confirmación de la anulación.
        :rtype: dict
        """
        url = (
            '/sii/bhe/emitidas/anular/%(emisor)s/%(folio)s?causa=%(causa)s'
            % {'emisor': emisor, 'folio': folio, 'causa': causa}
        )
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()


class BheRecibidas(ApiBase):
    """
    Cliente para Boletas de Honorarios Electrónicas (BHE) recibidas.

    Provee métodos para obtener documentos, obtener PDF y observar
    BHE recibidas.

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
        receptor: str,
        periodo: str,
        pagina: int | None = None,
        pagina_sig_codigo: str | None = None,
    ) -> Any:
        """
        Obtiene los documentos de BHE recibidos por un receptor en un periodo.

        :param str receptor: RUT del receptor de las boletas.
        :param str periodo: Período de tiempo de las boletas recibidas.
        :param int pagina: Número de página para paginación (opcional).
        :param str pagina_sig_codigo: Código para la siguiente página
            (opcional).
        :return: Respuesta JSON con los documentos de BHE.
        :rtype: list[dict]
        """
        url = '/sii/bhe/recibidas/documentos/%(receptor)s/%(periodo)s' % {
            'receptor': receptor,
            'periodo': periodo,
        }
        body = {'auth': self._get_auth_pass()}
        if pagina is not None:
            url += (
                '?pagina=%(pagina)s&pagina_sig_codigo=%(pagina_sig_codigo)s'
                % {
                    'pagina': pagina,
                    'pagina_sig_codigo': (
                        pagina_sig_codigo or '00000000000000'
                    ),
                }
            )
        response = self.client.post(url, data=body)
        return response.json()

    def pdf(self, codigo: str) -> bytes:
        """
        Obtiene el PDF de una BHE recibida.

        :param str codigo: Código único de la BHE.
        :return: Contenido del PDF de la BHE.
        :rtype: bytes
        """
        url = '/sii/bhe/recibidas/pdf/%(codigo)s' % {'codigo': codigo}
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.content

    def observar(self, emisor: str, numero: str, causa: int = 1) -> Any:
        """
        Marca una observación en una BHE recibida.

        :param str emisor: RUT del emisor de la boleta.
        :param str numero: Número de la boleta.
        :param int causa: Motivo de la observación.
        :return: Respuesta JSON con la confirmación de la observación.
        :rtype: dict
        """
        url = (
            '/sii/bhe/recibidas/observar/%(emisor)s/%(numero)s'
            '?causa=%(causa)s'
            % {'emisor': emisor, 'numero': numero, 'causa': causa}
        )
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()


class ConsultasPorTerceros(ApiBase):
    """
    Cliente para que un tercero verifique la autenticidad de una BHE.

    A diferencia de `BheEmitidas`/`BheRecibidas`, la autenticación es
    de quien CONSULTA, no del emisor ni del receptor de la boleta.

    :param str identificador: Identificador de quien consulta.
    :param str clave: Clave del identificador.
    :param kwargs: Argumentos adicionales.
    """

    def __init__(self, identificador: str, clave: str, **kwargs: str) -> None:
        """Autentica con `identificador`/`clave` de quien consulta."""
        super().__init__(
            identificador=identificador,
            clave=clave,
            **kwargs,  # type: ignore[arg-type]
        )

    def verificar(
        self,
        codigo_barras: str | None = None,
        emisor: str | None = None,
        receptor: str | None = None,
        periodo: str | None = None,
        folio: int | None = None,
    ) -> Any:
        """
        Verifica la autenticidad de una BHE ante el SII.

        Modos excluyentes: enviar solo `codigo_barras`, o todos de
        `emisor`/`receptor`/`periodo`/`folio`.

        :param str codigo_barras: Código de barras de la boleta.
        :param str emisor: RUT del emisor de la boleta.
        :param str receptor: RUT del receptor de la boleta.
        :param str periodo: Fecha de la boleta (AAAA-MM-DD).
        :param int folio: Folio de la boleta.
        :return: PDF oficial de la boleta emitido por el SII.
        :rtype: bytes
        """
        # TODO: Implementar.
