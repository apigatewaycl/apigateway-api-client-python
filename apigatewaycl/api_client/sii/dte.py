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
Módulo para Documentos Tributarios Electrónicos (DTE) del SII.

Para más información sobre la API, consulte la `documentación completa
de los DTE
<https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class Contribuyentes(ApiBase):
    """
    Cliente para los endpoints de contribuyentes de la API de API Gateway.

    Proporciona métodos para consultar la autorización de emisión de
    DTE de un contribuyente, sus datos privados y sus usuarios
    autorizados.

    :param str identificador: Identificador del contribuyente
        (opcional, sólo para los recursos que requieren autenticación).
    :param str clave: Clave del identificador (opcional).
    :param kwargs: Argumentos adicionales.
    """

    def __init__(
        self,
        identificador: str | None = None,
        clave: str | None = None,
        **kwargs: str,
    ) -> None:
        """
        Autentica con `identificador`/`clave` del contribuyente.

        Ambos son opcionales porque `autorizacion()` es un recurso
        público: no requiere credenciales del contribuyente.
        """
        argumentos: dict[str, str] = dict(kwargs)
        if identificador and clave:
            argumentos['identificador'] = identificador
            argumentos['clave'] = clave
        super().__init__(
            **argumentos,  # type: ignore[arg-type]
        )

    def autorizacion(
        self,
        rut: str,
        certificacion: bool | None = None,
    ) -> Any:
        """
        Verifica si un contribuyente está autorizado para emitir DTE.

        :param str rut: RUT del contribuyente a verificar.
        :param bool certificacion: Indica si se consulta en ambiente
            de certificación (opcional).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, estado de autorización.
        :rtype: dict
        """
        certificacion_flag = 1 if certificacion else 0
        url = (
            '/sii/dte/contribuyentes/autorizado/%(rut)s'
            '?certificacion=%(certificacion_flag)s'
            % {'rut': rut, 'certificacion_flag': certificacion_flag}
        )
        response = self.client.get(url)
        return response.json()

    def datos(
        self,
        contribuyente: str,
        certificacion: str | None = None,
    ) -> Any:
        """
        Datos privados del contribuyente autenticado.

        Incluye resolución de autorización, correos y software de
        facturación declarado.

        :param str contribuyente: RUT del contribuyente.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos privados del contribuyente.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/datos/%(contribuyente)s'
            % {'contribuyente': contribuyente},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()

    def set_datos(
        self,
        contribuyente: str,
        datos: dict[str, Any],
        certificacion: str | None = None,
    ) -> Any:
        """
        Actualiza los datos privados del contribuyente (emails, software).

        :param str contribuyente: RUT del contribuyente a actualizar.
        :param dict datos: Datos a actualizar (`emails`, `software`).
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos privados del contribuyente, ya actualizados.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/set_datos/%(contribuyente)s'
            % {'contribuyente': contribuyente},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth(), 'datos': datos}
        response = self.client.post(url, data=body)
        return response.json()

    def usuarios(
        self,
        rut: str,
        certificacion: str | None = None,
    ) -> Any:
        """
        Listado de usuarios autorizados de un contribuyente.

        :param str rut: RUT del contribuyente a consultar.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de usuarios, con nombre, RUN y permisos.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/usuarios/%(rut)s' % {'rut': rut},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()

    def set_usuario(
        self,
        contribuyente: str,
        usuario: dict[str, Any],
        certificacion: str | None = None,
    ) -> Any:
        """
        Asigna un usuario autorizado a un contribuyente.

        :param str contribuyente: RUT del contribuyente a actualizar.
        :param dict usuario: Usuario a asignar (`run` y `permisos`).
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, usuario asignado, con sus permisos.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/set_usuario/%(contribuyente)s'
            % {'contribuyente': contribuyente},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth(), 'usuario': usuario}
        response = self.client.post(url, data=body)
        return response.json()

    def autorizacion_certificado(
        self,
        rut: str,
        certificacion: str | None = None,
    ) -> Any:
        """
        Estado de autorización de un contribuyente, con certificado.

        A diferencia de `autorizacion()` (`GET`, pública), esta
        variante requiere certificado digital y agrega el correo
        electrónico de intercambio del contribuyente a la respuesta.

        :param str rut: RUT del contribuyente a consultar.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, autorización, resolución, dirección regional, software
            declarado, email de intercambio y documentos autorizados.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/autorizado/%(rut)s' % {'rut': rut},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()

    def autorizados(
        self,
        certificacion: str | None = None,
        dia: str | None = None,
        formato: str | None = None,
    ) -> Any:
        """
        Descarga masiva de contribuyentes autorizados a emitir DTE.

        Descarga la base completa del SII (cercana a un millón de
        registros, cientos de MB, hasta 15 minutos). No es para
        consultas puntuales de un RUT — para eso usar `autorizacion()`
        o `autorizacion_certificado()`.

        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str dia: Fecha de corte (AAAAMMDD o AAAA-MM-DD).
        :param str formato: `'json'`, `'csv'` o `'csv_sii'` (oficial
            del SII, sin transformar — recomendado y valor por defecto
            de la API).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de contribuyentes autorizados (RUT, razón
            social, resolución, email de intercambio, URL). Con
            `formato='json'` se entrega ya decodificado; con los dos formatos
            CSV se entrega el archivo crudo, sin decodificar (`csv_sii` viene
            en ISO-8859-1).
        :rtype: dict | bytes
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/autorizados',
            certificacion=certificacion,
            dia=dia,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        # Sólo `json` responde JSON. Los dos formatos CSV (incluído
        # `csv_sii`, el que aplica la API si no se pide otro) vienen
        # como texto plano y decodificarlos fallaría.
        if formato == 'json':
            return response.json()
        return response.content


class Emitidos(ApiBase):
    """
    Cliente específico para gestionar DTE emitidos.

    Permite verificar la validez y autenticidad de un DTE emitido.

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

    def verificar(
        self,
        emisor: str,
        receptor: str,
        dte: int,
        folio: int,
        fecha: str,
        total: int,
        firma: str | None = None,
        certificacion: str | None = None,
    ) -> Any:
        """
        Verifica la validez de un DTE emitido.

        :param str emisor: RUT del emisor del DTE.
        :param str receptor: RUT del receptor del DTE.
        :param int dte: Tipo de DTE.
        :param int folio: Número de folio del DTE.
        :param str fecha: Fecha de emisión del DTE.
        :param int total: Monto total del DTE.
        :param str firma: Firma electrónica del DTE (opcional).
        :param str certificacion: `'0'` producción, `'1'` certificación.
            Sólo aplica a documentos que no son boletas: las boletas (39
            y 41) se verifican siempre en producción.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, resultado de la verificación del DTE.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/emitidos/verificar',
            certificacion=certificacion,
        )
        body = {
            'auth': self._get_auth(),
            'dte': {
                'emisor': emisor,
                'receptor': receptor,
                'dte': dte,
                'folio': folio,
                'fecha': fecha,
                'total': total,
                'firma': firma,
            },
        }
        response = self.client.post(url, data=body)
        return response.json()

    def estado_envio(
        self,
        emisor: str,
        track_id: int,
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> Any:
        """
        Estado del envío de un XML de DTE al SII.

        Solo consulta envíos de empresas a las que el usuario
        autenticado con certificado digital tenga acceso.

        :param str emisor: RUT del emisor de los documentos.
        :param int track_id: Identificador del envío.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'json'` o `'html'`.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, estado del envío y resumen de documentos por tipo de
            DTE.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/emitidos/estado_envio/%(emisor)s/%(track_id)s'
            % {'emisor': emisor, 'track_id': track_id},
            certificacion=certificacion,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        # Con `formato='html'` la API igual responde JSON: el HTML
        # viene como una cadena dentro del cuerpo.
        return response.json()


class Iecv(ApiBase):
    """
    Cliente para la Información Electrónica de Compras y Ventas (IECV).

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

    def codigo_reemplazo(
        self,
        emisor: str,
        periodo: str,
        operacion: str,
        tipo: str,
        track_id: int,
        certificacion: str | None = None,
    ) -> Any:
        """
        Código de reemplazo de un libro IECV, para poder rectificarlo.

        Solo para períodos de 201707 hacia atrás.

        :param str emisor: RUT del emisor de los documentos.
        :param str periodo: Período del registro (AAAAMM).
        :param str operacion: `'VENTA'` o `'COMPRA'`.
        :param str tipo: `'MENSUAL'` o `'RECTIFICA'`.
        :param int track_id: Identificador del envío del libro a
            reemplazar.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, código de reemplazo del libro.
        :rtype: dict
        """
        url = self._build_url(
            '/sii/dte/iecv/codigo_reemplazo/%(emisor)s/%(periodo)s'
            '/%(operacion)s/%(tipo)s/%(track_id)s'
            % {
                'emisor': emisor,
                'periodo': periodo,
                'operacion': operacion,
                'tipo': tipo,
                'track_id': track_id,
            },
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return response.json()
