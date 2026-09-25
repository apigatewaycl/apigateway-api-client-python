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

from typing import Any, cast

from .. import ApiBase, ApiResponse


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
    ) -> ApiResponse[dict[str, Any]]:
        """
        Verifica si un contribuyente está autorizado para emitir DTE.

        Respuesta (ejemplo)::

            {
              "data": {
                "autorizado": true,
                "direccion_regional": "VI",
                "documentos": [
                  {
                    "autorizado": "2016-03-01",
                    "codigo": 39,
                    "desautorizado": null,
                    "descripcion": "BOLETA ELECTRONICA"
                  }
                ],
                "razon_social": "API Gateway",
                "resolucion": {"fecha": "2014-08-22", "numero": 80},
                "rut": "76192083-9",
                "software": "mercado"
              },
              "metadata": {"timestamp": "..."}
            }

        :param str rut: RUT del contribuyente a verificar.
        :param bool certificacion: Indica si se consulta en ambiente
            de certificación (opcional).
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, estado de autorización.
        :rtype: ApiResponse[dict[str, Any]]
        """
        certificacion_flag = 1 if certificacion else 0
        url = (
            '/sii/dte/contribuyentes/autorizado/%(rut)s'
            '?certificacion=%(certificacion_flag)s'
            % {'rut': rut, 'certificacion_flag': certificacion_flag}
        )
        response = self.client.get(url)
        return self._json(response)

    def datos(
        self,
        contribuyente: str,
        certificacion: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Datos privados del contribuyente autenticado.

        Incluye resolución de autorización, correos y software de
        facturación declarado.

        Respuesta (ejemplo)::

            {
              "data": {
                "rut": "12345678-9",
                "autorizado": "2025-02-25",
                "razon_social": "RAZON SOCIAL SPA",
                "resolucion": {"numero": 99, "fecha": "2014-10-21"},
                "emails": {
                  "administrador": "admin@example.com",
                  "sii": "sii@example.com",
                  "intercambio": "intercambio@example.com"
                },
                "software": {"nombre": "SII", "url": "www.example.com"}
              },
              "metadata": {"timestamp": "..."}
            }

        :param str contribuyente: RUT del contribuyente.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos privados del contribuyente.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/datos/%(contribuyente)s'
            % {'contribuyente': contribuyente},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def set_datos(
        self,
        contribuyente: str,
        datos: dict[str, Any],
        certificacion: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Actualiza los datos privados del contribuyente (emails, software).

        Respuesta (ejemplo)::

            {
              "data": {
                "data": {
                  "rut": "12345678-9",
                  "autorizado": "2019-12-23",
                  "razon_social": "RAZON SOCIAL SPA",
                  "resolucion": {"numero": 0, "fecha": "2019-12-23"},
                  "emails": {
                    "administrador": "admin@example.com",
                    "sii": "sii@example.com",
                    "intercambio": "dte@example.com"
                  },
                  "software": {"nombre": "LIBREDTE", "url": "www.libredte.cl"}
                }
              },
              "metadata": {"timestamp": "..."}
            }

        :param str contribuyente: RUT del contribuyente a actualizar.
        :param dict datos: Datos a actualizar (`emails`, `software`).
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos privados del contribuyente, ya actualizados.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/set_datos/%(contribuyente)s'
            % {'contribuyente': contribuyente},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth(), 'datos': datos}
        response = self.client.post(url, data=body)
        return self._json(response)

    def usuarios(
        self,
        rut: str,
        certificacion: str | None = None,
    ) -> ApiResponse[list[dict[str, Any]]]:
        """
        Listado de usuarios autorizados de un contribuyente.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "nombre": "Juan",
                  "permisos": {
                    "administrador": true,
                    "anular_folios": true,
                    "consultar": true,
                    "enviar": true,
                    "firmar": true,
                    "...": "..."
                  },
                  "run": "1-9"
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        :param str rut: RUT del contribuyente a consultar.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de usuarios, con nombre, RUN y permisos.
        :rtype: ApiResponse[list[dict[str, Any]]]
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/usuarios/%(rut)s' % {'rut': rut},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def set_usuario(
        self,
        contribuyente: str,
        usuario: dict[str, Any],
        certificacion: str | None = None,
    ) -> ApiResponse[list[dict[str, Any]]]:
        """
        Asigna un usuario autorizado, o modifica sus permisos si ya existe.

        `usuario` lleva `run` y `permisos`, con las claves booleanas
        `administrador`, `solicitar_folios`, `anular_folios`, `firmar`,
        `enviar` y `consultar`; las que no vengan cuentan como `False`.
        Para eliminar un usuario se envían todos los permisos en `False`:
        no hay un recurso aparte para eliminar.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "run": "66666666-6",
                  "nombre": "Juan",
                  "permisos": {
                    "administrador": true,
                    "solicitar_folios": true,
                    "anular_folios": true,
                    "firmar": true,
                    "enviar": true,
                    "...": "..."
                  }
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        :param str contribuyente: RUT del contribuyente a actualizar.
        :param dict usuario: Usuario a asignar (`run` y `permisos`).
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`. En `data`,
            la lista completa de usuarios autorizados después del cambio
            (no solo el enviado), con sus permisos.
        :rtype: ApiResponse[list[dict[str, Any]]]
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/set_usuario/%(contribuyente)s'
            % {'contribuyente': contribuyente},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth(), 'usuario': usuario}
        response = self.client.post(url, data=body)
        return self._json(response)

    def autorizacion_certificado(
        self,
        rut: str,
        certificacion: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Estado de autorización de un contribuyente, con certificado.

        A diferencia de `autorizacion()` (`GET`, pública), esta
        variante requiere certificado digital y agrega el correo
        electrónico de intercambio del contribuyente a la respuesta.

        Respuesta (ejemplo)::

            {
              "data": {
                "autorizado": true,
                "direccion_regional": "VI",
                "documentos": [
                  {
                    "autorizado": "2015-09-01",
                    "codigo": 33,
                    "desautorizado": null,
                    "descripcion": "FACTURA ELECTRONICA"
                  }
                ],
                "emails": {"intercambio": {"email": "dte@example.com"}},
                "razon_social": "API Gateway",
                "resolucion": {"fecha": "2014-08-22", "numero": 80},
                "rut": "76192083-9",
                "software": "mercado"
              },
              "metadata": {"timestamp": "..."}
            }

        :param str rut: RUT del contribuyente a consultar.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, autorización, resolución, dirección regional, software
            declarado, email de intercambio y documentos autorizados.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = self._build_url(
            '/sii/dte/contribuyentes/autorizado/%(rut)s' % {'rut': rut},
            certificacion=certificacion,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def autorizados(
        self,
        certificacion: str | None = None,
        dia: str | None = None,
        formato: str | None = None,
    ) -> ApiResponse[list[dict[str, Any]]] | bytes:
        """
        Descarga masiva de contribuyentes autorizados a emitir DTE.

        Descarga la base completa del SII (cercana a un millón de
        registros, cientos de MB, hasta 15 minutos). No es para
        consultas puntuales de un RUT — para eso usar `autorizacion()`
        o `autorizacion_certificado()`.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "rut": "76192083-9",
                  "razon_social": "API Gateway",
                  "resolucion_numero": "80",
                  "resolucion_fecha": "2014-08-22",
                  "email": "dte@example.com",
                  "url": "www.example.com"
                }
              ],
              "metadata": {"timestamp": "..."}
            }

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
        :rtype: ApiResponse[list[dict[str, Any]]] | bytes
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
            return self._json(response)
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
    ) -> ApiResponse[dict[str, Any]]:
        """
        Verifica la validez de un DTE emitido.

        Respuesta (ejemplo)::

            {
              "data": {
                "status": "DOK",
                "detalle": "Documento recibido por el SII. Datos ...",
                "track_id": 321421421521,
                "razon_social": "SASCO SPA"
              },
              "metadata": {"timestamp": "..."}
            }

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
        :rtype: ApiResponse[dict[str, Any]]
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
        return self._json(response)

    def estado_envio(
        self,
        emisor: str,
        track_id: int,
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> ApiResponse[dict[str, Any]] | str:
        """
        Estado del envío de un XML de DTE al SII.

        Solo consulta envíos de empresas a las que el usuario
        autenticado con certificado digital tenga acceso.

        Respuesta (ejemplo)::

            {
              "data": {
                "documentos": {
                  "33": {
                    "aceptados": 1,
                    "dte": 33,
                    "informados": 1,
                    "rechazados": 0,
                    "reparos": 0,
                    "...": "..."
                  }
                },
                "emisor": "76192083-9",
                "estado": "Envio Procesado [EPR].",
                "track_id": "1234"
              },
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor de los documentos.
        :param int track_id: Identificador del envío.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'json'` o `'html'`.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, estado del envío y resumen de documentos por tipo de
            DTE. Con `formato='html'` se entrega el HTML del SII como
            `str`, sin `data` ni `metadata`.
        :rtype: ApiResponse[dict[str, Any]] | str
        """
        url = self._build_url(
            '/sii/dte/emitidos/estado_envio/%(emisor)s/%(track_id)s'
            % {'emisor': emisor, 'track_id': track_id},
            certificacion=certificacion,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        # Con `formato='html'` la API responde el HTML como una cadena
        # JSON, sin `data` ni `metadata`.
        if formato == 'html':
            return cast(str, response.json())
        return self._json(response)


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
    ) -> ApiResponse[dict[str, Any]]:
        """
        Código de reemplazo de un libro IECV, para poder rectificarlo.

        Solo para períodos de 201707 hacia atrás.

        Respuesta (ejemplo)::

            {
              "data": {"codigo_reemplazo": "1234567890"},
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor de los documentos.
        :param str periodo: Período del registro (AAAAMM).
        :param str operacion: `'VENTA'` o `'COMPRA'`.
        :param str tipo: `'MENSUAL'` o `'RECTIFICA'`.
        :param int track_id: Identificador del envío del libro a
            reemplazar.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, código de reemplazo del libro.
        :rtype: ApiResponse[dict[str, Any]]
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
        return self._json(response)
