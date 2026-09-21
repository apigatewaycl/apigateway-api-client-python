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
<https://developers.apigateway.cl/#ef1f7d54-2e86-4732-bb91-d3448b383d66>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class Rcv(ApiBase):
    """
    Cliente para el Registro de Compras y Ventas (RCV) de la API.

    Proporciona métodos para obtener resúmenes y detalles de compras
    y ventas.

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

    def compras_resumen(
        self, receptor: str, periodo: str, estado: str = 'REGISTRO'
    ) -> Any:
        """
        Obtiene un resumen de las compras de un receptor en un periodo.

        :param str receptor: RUT del receptor de las compras.
        :param str periodo: Período de tiempo de las compras.
        :param str estado: Estado de las compras ('REGISTRO',
            'PENDIENTE', 'NO_INCLUIR', 'RECLAMADO').
        :return: Respuesta JSON con el resumen de compras.
        :rtype: list[dict]
        """
        url = (
            '/sii/rcv/compras/resumen/%(receptor)s/%(periodo)s/%(estado)s'
            % {'receptor': receptor, 'periodo': periodo, 'estado': estado}
        )
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def compras_detalle(
        self,
        receptor: str,
        periodo: str,
        dte: int = 0,
        estado: str = 'REGISTRO',
        tipo: str | None = None,
    ) -> Any:
        """
        Obtiene detalles de las compras para un receptor en un periodo.

        :param str receptor: RUT del receptor de las compras.
        :param str periodo: Período de tiempo de las compras.
        :param int dte: Tipo de DTE.
        :param str estado: Estado de las compras ('REGISTRO',
            'PENDIENTE', 'NO_INCLUIR', 'RECLAMADO').
        :param str tipo: Tipo de formato de respuesta ('rcv_csv' o
            'rcv').
        :return: Respuesta JSON con detalles de las compras.
        :rtype: list[dict]
        """
        es_registro = dte == 0 and estado == 'REGISTRO'
        tipo = 'rcv_csv' if es_registro else tipo or 'rcv'
        url = (
            '/sii/rcv/compras/detalle/'
            '%(receptor)s/%(periodo)s/%(dte)s/%(estado)s?tipo=%(tipo)s'
            % {
                'receptor': receptor,
                'periodo': periodo,
                'dte': dte,
                'estado': estado,
                'tipo': tipo,
            }
        )
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def compras_set_tipo_transaccion(
        self,
        receptor: str,
        periodo: str,
        documentos: list[dict[str, Any]],
        certificacion: str | None = None,
    ) -> Any:
        """
        Asigna el tipo de transacción y código de IVA a compras del RCV.

        Cada elemento de `documentos` lleva `emisor`, `dte`, `folio`,
        `tipo_transaccion` (1 a 6) y `codigo_iva`.

        :param str receptor: RUT del receptor de los documentos.
        :param str periodo: Período del registro (AAAAMM).
        :param list documentos: Documentos a los que asignar el tipo
            de transacción.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: Vacío cuando la asignación fue exitosa.
        :rtype: None
        """
        # TODO: Implementar.

    def ventas_set_resumen(
        self,
        emisor: str,
        periodo: str,
        documentos: list[dict[str, Any]],
        certificacion: str | None = None,
    ) -> Any:
        """
        Asigna un resumen de documentos emitidos al registro de ventas.

        Útil para agregar mensualmente el resumen de boletas emitidas.
        Cada elemento de `documentos` lleva `det_tipo_doc`,
        `det_nro_doc`, `det_mnt_neto`, `det_mnt_iva`, `det_mnt_exe` y
        `det_mnt_total`.

        :param str emisor: RUT del emisor de los documentos.
        :param str periodo: Período de emisión de los documentos
            (AAAAMM).
        :param list documentos: Resumen de documentos a asignar.
        :param str certificacion: `'0'` producción, `'1'` certificación.
        :return: `True` si el resumen fue asignado.
        :rtype: bool
        """
        # TODO: Implementar.

    def ventas_resumen(self, emisor: str, periodo: str) -> Any:
        """
        Obtiene un resumen de las ventas de un emisor en un periodo.

        :param str emisor: RUT del emisor de las ventas.
        :param str periodo: Período de tiempo de las ventas.
        :return: Respuesta JSON con el resumen de ventas.
        :rtype: list[dict]
        """
        url = '/sii/rcv/ventas/resumen/%(emisor)s/%(periodo)s' % {
            'emisor': emisor,
            'periodo': periodo,
        }
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def ventas_detalle(
        self,
        emisor: str,
        periodo: str,
        dte: int = 0,
        tipo: str | None = None,
    ) -> Any:
        """
        Obtiene detalles de las ventas para un emisor en un periodo.

        :param str emisor: RUT del emisor de las ventas.
        :param str periodo: Período de tiempo de las ventas.
        :param int dte: Tipo de DTE.
        :param str tipo: Tipo de formato de respuesta ('rcv_csv' o
            'rcv').
        :return: Respuesta JSON con detalles de las ventas.
        :rtype: list[dict]
        """
        tipo = 'rcv_csv' if dte == 0 else tipo or 'rcv'
        url = (
            '/sii/rcv/ventas/detalle/%(emisor)s/%(periodo)s/%(dte)s'
            '?tipo=%(tipo)s'
            % {
                'emisor': emisor,
                'periodo': periodo,
                'dte': dte,
                'tipo': tipo,
            }
        )
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def compras_async_solicitar(
        self,
        receptor: str,
        periodo: str,
        dte: int = 0,
        estado: str = 'REGISTRO',
    ) -> Any:
        """
        Solicita el envío de los detalles de las compras de un receptor.

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

        :return: Respuesta JSON con la solicitud de envío.
        :rtype: dict
        """
        url = '/sii/rcv/compras/async/solicitar'
        url += '/%(receptor)s/%(periodo)s/%(dte)s/%(estado)s' % {
            'receptor': receptor,
            'periodo': periodo,
            'dte': dte,
            'estado': estado,
        }
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def compras_async_estado(
        self,
        receptor: str,
        periodo: str,
        id_solicitud: str,
        dte: int = 0,
        estado: str = 'REGISTRO',
    ) -> Any:
        """
        Obtiene el estado de la solicitud de los detalles de las compras.

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

        :return: Respuesta JSON con el estado de la solicitud.
        :rtype: dict
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
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def compras_async_detalle(
        self,
        receptor: str,
        periodo: str,
        id_solicitud: str,
        dte: int = 0,
        estado: str = 'REGISTRO',
    ) -> Any:
        """
        Obtiene los detalles de las compras de un receptor en un periodo.

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

        :return: Respuesta JSON con los detalles de las compras.
        :rtype: dict
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
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def ventas_async_solicitar(
        self,
        emisor: str,
        periodo: str,
        dte: int = 0,
    ) -> Any:
        """
        Solicita el envío de los detalles de las ventas de un emisor.

        :param emisor: RUT del emisor de las ventas formato 12345678-9.
        :type emisor: str

        :param periodo: Período de tiempo de las ventas formato YYYYMM.
        :type periodo: str

        :param dte: Tipo de DTE formato 0 para todos los tipos de DTE
            o el tipo de DTE.
        :type dte: int

        :return: Respuesta JSON con la solicitud de envío.
        :rtype: dict
        """
        url = '/sii/rcv/ventas/async/solicitar'
        url += '/%(emisor)s/%(periodo)s/%(dte)s' % {
            'emisor': emisor,
            'periodo': periodo,
            'dte': dte,
        }
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def ventas_async_estado(
        self,
        emisor: str,
        periodo: str,
        id_solicitud: str,
        dte: int = 0,
    ) -> Any:
        """
        Obtiene el estado de la solicitud de los detalles de las ventas.

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

        :return: Respuesta JSON con el estado de la solicitud.
        :rtype: dict
        """
        url = '/sii/rcv/ventas/async/estado/%(emisor)s'
        url += '/%(periodo)s/%(id_solicitud)s/%(dte)s'
        url = url % {
            'emisor': emisor,
            'periodo': periodo,
            'id_solicitud': id_solicitud,
            'dte': dte,
        }
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()

    def ventas_async_detalle(
        self,
        emisor: str,
        periodo: str,
        id_solicitud: str,
        dte: int = 0,
    ) -> Any:
        """
        Obtiene los detalles de las ventas de un emisor.

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

        :return: Respuesta JSON con los detalles de las ventas.
        :rtype: dict
        """
        url = '/sii/rcv/ventas/async/detalle/%(emisor)s'
        url += '/%(periodo)s/%(id_solicitud)s/%(dte)s'
        url = url % {
            'emisor': emisor,
            'periodo': periodo,
            'id_solicitud': id_solicitud,
            'dte': dte,
        }
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(url, data=body)
        return response.json()
