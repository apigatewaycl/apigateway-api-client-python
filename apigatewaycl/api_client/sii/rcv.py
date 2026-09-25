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
Módulo para interactuar con el Registro de Compra y Venta del SII.

Para más información sobre la API, consulte la `documentación completa
del RCV
<https://www.apigateway.cl/docs>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase, ApiResponse


class Rcv(ApiBase):
    """
    Cliente para el Registro de Compras y Ventas (RCV) de la API.

    Proporciona métodos para obtener resúmenes y detalles de compras
    y ventas.

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

    def compras_resumen(
        self,
        receptor: str,
        periodo: str,
        estado: str = 'REGISTRO',
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene un resumen de las compras de un receptor en un periodo.

        Respuesta (ejemplo)::

            {
              "data": {
                "respEstado": {
                  "codRespuesta": 0,
                  "msgeRespuesta": null,
                  "codError": null
                },
                "data": [
                  {
                    "dcvCodigo": 1234,
                    "dcvNombreTipoDoc": "Factura Electrónica",
                    "dcvOperacion": null,
                    "dcvTipoIngresoDoc": "DET_ELE",
                    "rsmnCodigo": 1234,
                    "...": "..."
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param str receptor: RUT del receptor de las compras.
        :param str periodo: Período de tiempo de las compras.
        :param str estado: Estado de las compras ('REGISTRO',
            'PENDIENTE', 'NO_INCLUIR', 'RECLAMADO').
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'json'`.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, resumen de compras.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = self._build_url(
            '/sii/rcv/compras/resumen/%(receptor)s/%(periodo)s/%(estado)s'
            % {'receptor': receptor, 'periodo': periodo, 'estado': estado},
            certificacion=certificacion,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def compras_detalle(
        self,
        receptor: str,
        periodo: str,
        dte: int = 0,
        estado: str = 'REGISTRO',
        tipo: str | None = None,
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> ApiResponse[list[dict[str, Any]] | dict[str, Any]] | bytes:
        """
        Obtiene detalles de las compras para un receptor en un periodo.

        Respuesta (ejemplo, dte=0 y estado 'REGISTRO')::

            {
              "data": [
                {
                  "dte": "33",
                  "tipo_transaccion": "Del Giro",
                  "rut": "76192083-9",
                  "razon_social": "EMPRESA PROVEEDORA SPA",
                  "folio": "123",
                  "fecha": "2026-08-23",
                  "fecha_recepcion": "2026-08-23 11:37:20",
                  "fecha_acuse": null,
                  "...": "..."
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        Respuesta (ejemplo, un dte específico)::

            {
              "data": {
                "respEstado": {
                  "codRespuesta": 0,
                  "msgeRespuesta": null,
                  "codError": null
                },
                "data": [
                  {
                    "cambiarTipoTran": true,
                    "dcvCodigo": 1234,
                    "dcvEstadoContab": null,
                    "descTipoTransaccion": "Del Giro",
                    "detAnulado": null,
                    "...": "..."
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param str receptor: RUT del receptor de las compras.
        :param str periodo: Período de tiempo de las compras.
        :param int dte: Tipo de DTE.
        :param str estado: Estado de las compras ('REGISTRO',
            'PENDIENTE', 'NO_INCLUIR', 'RECLAMADO').
        :param str tipo: Tipo de formato de respuesta ('rcv_csv' o
            'rcv').
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'json'` o `'csv'`.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, detalles de las compras: con `dte=0` y estado
            `'REGISTRO'` una lista de documentos; en otro caso un dict
            con `respEstado` y, en `data`, la lista de documentos. Con
            `formato` `'csv'` se entrega el archivo crudo, sin
            decodificar.
        :rtype: ApiResponse[list[dict[str, Any]] | dict[str, Any]] | bytes
        """
        es_registro = dte == 0 and estado == 'REGISTRO'
        tipo = 'rcv_csv' if es_registro else tipo or 'rcv'
        url = self._build_url(
            '/sii/rcv/compras/detalle/%(receptor)s/%(periodo)s/%(dte)s'
            '/%(estado)s'
            % {
                'receptor': receptor,
                'periodo': periodo,
                'dte': dte,
                'estado': estado,
            },
            tipo=tipo,
            certificacion=certificacion,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        # Con `csv` la API responde el archivo tal cual, no JSON.
        if formato == 'csv':
            return response.content
        return self._json(response)

    def compras_set_tipo_transaccion(
        self,
        receptor: str,
        periodo: str,
        documento: dict[str, Any],
        certificacion: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Asigna el tipo de transacción y código de IVA a una compra del RCV.

        Se envía un solo documento, que debe estar en el Registro de
        Compras del período; el resto mantiene su tipo de transacción.
        Lleva `emisor`, `dte` (33, 34, 43, 46, 56 o 61), `folio`,
        `tipo_transaccion` (1 a 7) y `codigo_iva`, que debe ser uno de
        los permitidos para ese `tipo_transaccion`.

        Respuesta (ejemplo)::

            {
              "data": {
                "codigo": 0,
                "mensaje": "Carga de cambios de tipo de compra re...",
                "estado": "ok",
                "reparos": [],
                "errores": []
              },
              "metadata": {"timestamp": "..."}
            }

        :param str receptor: RUT del receptor del documento.
        :param str periodo: Período del registro (AAAAMM).
        :param dict documento: Documento al que asignar el tipo de
            transacción.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Respuesta de la API, con `data` y `metadata`. En `data`,
            el resultado del SII, donde `codigo` `0` indica éxito. Si el
            SII rechaza el documento, la API responde con error.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = self._build_url(
            '/sii/rcv/compras/set_tipo_transaccion/%(receptor)s/%(periodo)s'
            % {'receptor': receptor, 'periodo': periodo},
            certificacion=certificacion,
        )
        body = {
            'auth': self._get_auth(),
            'documento': documento,
        }
        response = self.client.post(url, data=body)
        return self._json(response)

    def ventas_set_resumen(
        self,
        emisor: str,
        periodo: str,
        documentos: list[dict[str, Any]],
        certificacion: str | None = None,
        graba_con_reparos: bool | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Asigna un resumen de documentos emitidos al registro de ventas.

        Útil para agregar mensualmente el resumen de boletas emitidas.
        Cada elemento de `documentos` lleva `det_tipo_doc`,
        `det_nro_doc`, `det_mnt_neto`, `det_mnt_iva`, `det_mnt_exe` y
        `det_mnt_total`. Los comprobantes de pago electrónico (48)
        llevan además `canalTransacc` y, si corresponde,
        `codRznModifica` y `txtRznModifica`.

        Respuesta (ejemplo)::

            {
              "data": {
                "contribuyente": "76192083-9",
                "periodo": 202608,
                "resumenes": [
                  {"tipo_doc": 48, "canal": 0, "registros_modificados": 1}
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor de los documentos.
        :param str periodo: Período de emisión de los documentos
            (AAAAMM).
        :param list documentos: Resumen de documentos a asignar.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param bool graba_con_reparos: Con `False` el SII rechaza el
            resumen si encuentra reparos (la API responde con error). Sin
            indicarlo se aplica el valor por defecto de la API (`True`):
            el resumen se graba aunque tenga reparos.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, el `contribuyente`, el `periodo` y en `resumenes`
            cada resumen grabado (tipo de documento, canal de venta y
            registros modificados por el SII).
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = self._build_url(
            '/sii/rcv/ventas/set_resumen/%(emisor)s/%(periodo)s'
            % {'emisor': emisor, 'periodo': periodo},
            certificacion=certificacion,
        )
        body: dict[str, Any] = {
            'auth': self._get_auth(),
            'documentos': documentos,
        }
        if graba_con_reparos is not None:
            body['graba_con_reparos'] = graba_con_reparos
        response = self.client.post(url, data=body)
        return self._json(response)

    def ventas_resumen(
        self,
        emisor: str,
        periodo: str,
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene un resumen de las ventas de un emisor en un periodo.

        Respuesta (ejemplo)::

            {
              "data": {
                "respEstado": {
                  "codRespuesta": 0,
                  "msgeRespuesta": null,
                  "codError": null
                },
                "data": [
                  {
                    "dcvCodigo": 1234,
                    "dcvNombreTipoDoc": "Factura Electrónica",
                    "dcvOperacion": null,
                    "dcvTipoIngresoDoc": "DET_ELE",
                    "rsmnCodigo": 1234,
                    "...": "..."
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor de las ventas.
        :param str periodo: Período de tiempo de las ventas.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'json'`.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, `respEstado` con el estado de la consulta al SII
            y, en `data`, el resumen por tipo de documento.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = self._build_url(
            '/sii/rcv/ventas/resumen/%(emisor)s/%(periodo)s'
            % {'emisor': emisor, 'periodo': periodo},
            certificacion=certificacion,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def ventas_detalle(
        self,
        emisor: str,
        periodo: str,
        dte: int = 0,
        tipo: str | None = None,
        certificacion: str | None = None,
        formato: str | None = None,
    ) -> ApiResponse[list[dict[str, Any]] | dict[str, Any]] | bytes:
        """
        Obtiene detalles de las ventas para un emisor en un periodo.

        Respuesta (ejemplo, dte=0)::

            {
              "data": [
                {
                  "dte": "33",
                  "tipo_transaccion": "Del Giro",
                  "rut": "12345678-9",
                  "razon_social": "CLIENTE EJEMPLO",
                  "folio": "123",
                  "fecha": "2026-09-20",
                  "fecha_recepcion": "2026-09-20 22:47:31",
                  "fecha_acuse": null,
                  "...": "..."
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        Respuesta (ejemplo, un dte específico)::

            {
              "data": {
                "respEstado": {
                  "codRespuesta": 0,
                  "msgeRespuesta": null,
                  "codError": null
                },
                "data": [
                  {
                    "cambiarTipoTran": false,
                    "dcvCodigo": 1234,
                    "dcvEstadoContab": null,
                    "descTipoTransaccion": "Del Giro",
                    "detAnulado": null,
                    "...": "..."
                  }
                ]
              },
              "metadata": {"timestamp": "..."}
            }

        :param str emisor: RUT del emisor de las ventas.
        :param str periodo: Período de tiempo de las ventas.
        :param int dte: Tipo de DTE.
        :param str tipo: Tipo de formato de respuesta ('rcv_csv' o
            'rcv').
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :param str formato: `'json'` o `'csv'`.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, detalles de las ventas: con `dte=0` una lista de
            documentos; con un `dte` específico un dict con `respEstado`
            y, en `data`, la lista de documentos. Con `formato` `'csv'`
            se entrega el archivo crudo, sin decodificar.
        :rtype: ApiResponse[list[dict[str, Any]] | dict[str, Any]] | bytes
        """
        tipo = 'rcv_csv' if dte == 0 else tipo or 'rcv'
        url = self._build_url(
            '/sii/rcv/ventas/detalle/%(emisor)s/%(periodo)s/%(dte)s'
            % {'emisor': emisor, 'periodo': periodo, 'dte': dte},
            tipo=tipo,
            certificacion=certificacion,
            formato=formato,
        )
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        # Con `csv` la API responde el archivo tal cual, no JSON.
        if formato == 'csv':
            return response.content
        return self._json(response)

    def compras_async_solicitar(
        self,
        receptor: str,
        periodo: str,
        dte: int = 0,
        estado: str = 'REGISTRO',
        certificacion: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Solicita el envío de los detalles de las compras de un receptor.

        Respuesta (ejemplo)::

            {
              "data": {
                "id": 1234,
                "uuid": "1234567890",
                "dte": 33,
                "estado": "REGISTRO",
                "creada": "2025-01-01 12:00:00",
                "terminada": "2025-01-01 12:00:00",
                "seccion": "COMPRA",
                "registros": 100
              },
              "metadata": {"timestamp": "..."}
            }

        :param receptor: RUT del receptor de las compras formato
            12345678-9.
        :type receptor: str

        :param periodo: Período de tiempo de las compras formato YYYYMM.
        :type periodo: str

        :param dte: Tipo de DTE formato 0 para todos los tipos de DTE
            o el tipo de DTE.
        :type dte: int

        :param estado: Estado de las compras ('REGISTRO', 'PENDIENTE',
            'NO_INCLUIR', 'RECLAMADO').
        :type estado: str

        :param certificacion: `'0'` producción, `'1'` certificación.
        :type certificacion: str

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, solicitud de envío.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/rcv/compras/async/solicitar'
        url += '/%(receptor)s/%(periodo)s/%(dte)s/%(estado)s' % {
            'receptor': receptor,
            'periodo': periodo,
            'dte': dte,
            'estado': estado,
        }
        url = self._build_url(url, certificacion=certificacion)
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def compras_async_estado(
        self,
        receptor: str,
        periodo: str,
        id_solicitud: str,
        dte: int = 0,
        estado: str = 'REGISTRO',
        certificacion: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene el estado de la solicitud de los detalles de las compras.

        Respuesta (ejemplo)::

            {
              "data": {
                "id": "1234567890",
                "uuid": "1234567890",
                "dte": 33,
                "estado": "REGISTRO",
                "creada": "2025-01-01 12:00:00",
                "terminada": "2025-01-01 12:00:00",
                "seccion": "COMPRA",
                "registros": 100
              },
              "metadata": {"timestamp": "..."}
            }

        :param receptor: RUT del receptor de las compras formato
            12345678-9.
        :type receptor: str

        :param periodo: Período de tiempo de las compras formato YYYYMM.
        :type periodo: str

        :param id_solicitud: ID de la solicitud de envío de los
            detalles de las compras.
        :type id_solicitud: str

        :param dte: Tipo de DTE formato 0 para todos los tipos de DTE
            o el tipo de DTE.
        :type dte: int

        :param estado: Estado de las compras ('REGISTRO', 'PENDIENTE',
            'NO_INCLUIR', 'RECLAMADO').
        :type estado: str

        :param certificacion: `'0'` producción, `'1'` certificación.
        :type certificacion: str

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, estado de la solicitud.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/rcv/compras/async/estado/%(receptor)s'
        url += '/%(periodo)s/%(id_solicitud)s/%(dte)s/%(estado)s'
        url = url % {
            'receptor': receptor,
            'periodo': periodo,
            'id_solicitud': id_solicitud,
            'dte': dte,
            'estado': estado,
        }
        url = self._build_url(url, certificacion=certificacion)
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def compras_async_detalle(
        self,
        receptor: str,
        periodo: str,
        id_solicitud: str,
        dte: int = 0,
        estado: str = 'REGISTRO',
        certificacion: str | None = None,
    ) -> ApiResponse[list[dict[str, Any]]]:
        """
        Obtiene los detalles de las compras de un receptor en un periodo.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "dte": 33,
                  "tipo_transaccion": "Del Giro",
                  "rut": "12345-0",
                  "razon_social": "RAZON SOCIAL DE LA EMPRESA",
                  "folio": "10518",
                  "fecha": "2025-09-01",
                  "fecha_recepcion": "2025-09-01 10:52:28",
                  "fecha_acuse": "2025-09-01 13:39:33",
                  "...": "..."
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        :param receptor: RUT del receptor de las compras formato
            12345678-9.
        :type receptor: str

        :param periodo: Período de tiempo de las compras formato YYYYMM.
        :type periodo: str

        :param id_solicitud: ID de la solicitud de envío de los
            detalles de las compras.
        :type id_solicitud: str

        :param dte: Tipo de DTE formato 0 para todos los tipos de DTE
            o el tipo de DTE.
        :type dte: int

        :param estado: Estado de las compras ('REGISTRO', 'PENDIENTE',
            'NO_INCLUIR', 'RECLAMADO').
        :type estado: str

        :param certificacion: `'0'` producción, `'1'` certificación.
        :type certificacion: str

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, detalles de las compras.
        :rtype: ApiResponse[list[dict[str, Any]]]
        """
        url = '/sii/rcv/compras/async/detalle/%(receptor)s'
        url += '/%(periodo)s/%(id_solicitud)s/%(dte)s/%(estado)s'
        url = url % {
            'receptor': receptor,
            'periodo': periodo,
            'id_solicitud': id_solicitud,
            'dte': dte,
            'estado': estado,
        }
        url = self._build_url(url, certificacion=certificacion)
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def ventas_async_solicitar(
        self,
        emisor: str,
        periodo: str,
        dte: int = 0,
        certificacion: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Solicita el envío de los detalles de las ventas de un emisor.

        Respuesta (ejemplo)::

            {
              "data": {
                "id": 1234,
                "uuid": "1234567890",
                "dte": 33,
                "estado": "REGISTRO",
                "creada": "2025-01-01 12:00:00",
                "terminada": "2025-01-01 12:00:00",
                "seccion": "VENTA",
                "registros": 100
              },
              "metadata": {"timestamp": "..."}
            }

        :param emisor: RUT del emisor de las ventas formato 12345678-9.
        :type emisor: str

        :param periodo: Período de tiempo de las ventas formato YYYYMM.
        :type periodo: str

        :param dte: Tipo de DTE formato 0 para todos los tipos de DTE
            o el tipo de DTE.
        :type dte: int

        :param certificacion: `'0'` producción, `'1'` certificación.
        :type certificacion: str

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, solicitud de envío.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/rcv/ventas/async/solicitar'
        url += '/%(emisor)s/%(periodo)s/%(dte)s' % {
            'emisor': emisor,
            'periodo': periodo,
            'dte': dte,
        }
        url = self._build_url(url, certificacion=certificacion)
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def ventas_async_estado(
        self,
        emisor: str,
        periodo: str,
        id_solicitud: str,
        dte: int = 0,
        certificacion: str | None = None,
    ) -> ApiResponse[dict[str, Any]]:
        """
        Obtiene el estado de la solicitud de los detalles de las ventas.

        Respuesta (ejemplo)::

            {
              "data": {
                "id": "1234567890",
                "uuid": "1234567890",
                "dte": 33,
                "estado": "REGISTRO",
                "creada": "2025-01-01 12:00:00",
                "terminada": "2025-01-01 12:00:00",
                "seccion": "VENTA",
                "registros": 100
              },
              "metadata": {"timestamp": "..."}
            }

        :param emisor: RUT del emisor de las ventas formato 12345678-9.
        :type emisor: str

        :param periodo: Período de tiempo de las ventas formato YYYYMM.
        :type periodo: str

        :param id_solicitud: ID de la solicitud de envío de los
            detalles de las ventas de un emisor.
        :type id_solicitud: str

        :param dte: Tipo de DTE formato 0 para todos los tipos de DTE
            o el tipo de DTE.
        :type dte: int

        :param certificacion: `'0'` producción, `'1'` certificación.
        :type certificacion: str

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, estado de la solicitud.
        :rtype: ApiResponse[dict[str, Any]]
        """
        url = '/sii/rcv/ventas/async/estado/%(emisor)s'
        url += '/%(periodo)s/%(id_solicitud)s/%(dte)s'
        url = url % {
            'emisor': emisor,
            'periodo': periodo,
            'id_solicitud': id_solicitud,
            'dte': dte,
        }
        url = self._build_url(url, certificacion=certificacion)
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)

    def ventas_async_detalle(
        self,
        emisor: str,
        periodo: str,
        id_solicitud: str,
        dte: int = 0,
        certificacion: str | None = None,
    ) -> ApiResponse[list[dict[str, Any]]]:
        """
        Obtiene los detalles de las ventas de un emisor.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "dte": 33,
                  "tipo_transaccion": "Del Giro",
                  "rut": "1234-0",
                  "razon_social": "RAZON SOCIAL DE LA EMPRESA",
                  "folio": "12414",
                  "fecha": "2025-09-01",
                  "fecha_vencimiento": null,
                  "fecha_recepcion": "2025-09-01 08:01:43",
                  "...": "..."
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        :param emisor: RUT del emisor de las ventas formato 12345678-9.
        :type emisor: str

        :param periodo: Período de tiempo de las ventas formato YYYYMM.
        :type periodo: str

        :param id_solicitud: ID de la solicitud de envío de los
            detalles de las ventas de un emisor.
        :type id_solicitud: str

        :param dte: Tipo de DTE formato 0 para todos los tipos de DTE
            o el tipo de DTE.
        :type dte: int

        :param certificacion: `'0'` producción, `'1'` certificación.
        :type certificacion: str

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, detalles de las ventas.
        :rtype: ApiResponse[list[dict[str, Any]]]
        """
        url = '/sii/rcv/ventas/async/detalle/%(emisor)s'
        url += '/%(periodo)s/%(id_solicitud)s/%(dte)s'
        url = url % {
            'emisor': emisor,
            'periodo': periodo,
            'id_solicitud': id_solicitud,
            'dte': dte,
        }
        url = self._build_url(url, certificacion=certificacion)
        body = {'auth': self._get_auth()}
        response = self.client.post(url, data=body)
        return self._json(response)
