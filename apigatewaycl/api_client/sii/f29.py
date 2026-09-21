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
Módulo para el Formulario 29 (F29) del SII.

Para más información sobre la API, consulte la `documentación completa
del Formulario 29 <https://developers.apigateway.cl/>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class F29(ApiBase):
    """
    Cliente para consultas del Formulario 29 (F29) del SII.

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

    def obtener_estados(self) -> Any:
        """
        Consulta integral de fiscalización del Formulario 29.

        Para cada período, indica si fue declarado y su estado (sin
        observaciones, con observaciones, con observaciones
        justificadas, o sin declaración presentada).

        :return: Listado de períodos con su estado de declaración.
        :rtype: list[dict]
        """
        # TODO: Implementar.

    def detalles_declaracion(self, folio: str) -> Any:
        """
        Detalles de una declaración del Formulario 29 por folio.

        :param str folio: Folio del formulario 29.
        :return: Folio, período, fecha/hora, estado e historial de la
            declaración.
        :rtype: dict
        """
        # TODO: Implementar.

    def declaraciones_listado(self, periodo: str) -> Any:
        """
        Listado de declaraciones del Formulario 29 por período.

        :param str periodo: Período a consultar (AAAA o AAAA-MM).
        :return: Listado de declaraciones (período, folio, RUT, fecha
            y estado) del período.
        :rtype: list[dict]
        """
        # TODO: Implementar.

    def certificado_solemne_pdf(self, folio: str) -> Any:
        """
        Descarga el PDF del Certificado Solemne del Formulario 29.

        :param str folio: Folio del certificado solemne.
        :return: Contenido del PDF del certificado solemne.
        :rtype: bytes
        """
        # TODO: Implementar.

    def formulario_compacto_pdf(self, folio: str) -> Any:
        """
        Descarga el PDF del formulario compacto del Formulario 29.

        :param str folio: Folio del formulario compacto.
        :return: Contenido del PDF del formulario compacto.
        :rtype: bytes
        """
        # TODO: Implementar.
