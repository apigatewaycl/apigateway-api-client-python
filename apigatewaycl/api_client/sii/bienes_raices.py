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
Módulo para Bienes Raíces del SII.

Para más información sobre la API, consulte la `documentación completa
de Bienes Raíces <https://developers.apigateway.cl/>`_.
"""

from __future__ import annotations

from typing import Any

from .. import ApiBase


class BienesRaices(ApiBase):
    """
    Cliente para consultas de Bienes Raíces del SII.

    La mayoría de los recursos son públicos (solo requieren la llave de
    la API). `propiedades_contribuyente()` es la excepción: requiere
    autenticación con certificado digital, mediante `identificador`
    (cert-data o file-data) y `clave` (pkey-data o file-pass) al
    instanciar la clase.
    """

    def comunas(self) -> Any:
        """
        Listado de comunas de los bienes raíces.

        :return: Comunas con su código CONARA/SII, nombre, región,
            código y descripciones.
        :rtype: list[dict]
        """
        # TODO: Implementar.

    def comuna(self, comuna: str) -> Any:
        """
        Datos de una comuna de los bienes raíces, por nombre.

        :param str comuna: Nombre de la comuna a buscar.
        :return: Código CONARA/SII, nombre, región, código y
            descripciones de la comuna.
        :rtype: dict
        """
        # TODO: Implementar.

    def propiedades_rol(self, comuna: int, manzana: int, predio: int) -> Any:
        """
        Propiedades de un bien raíz por su rol (comuna/manzana/predio).

        :param int comuna: Código de la comuna.
        :param int manzana: Número de manzana.
        :param int predio: Número de predio.
        :return: Listado de propiedades con identificación del rol,
            ubicación, inscripción, avalúos y contribuciones.
        :rtype: list[dict]
        """
        # TODO: Implementar.

    def propiedades_contribuyente(self) -> Any:
        """
        Propiedades del contribuyente autenticado.

        Requiere autenticación con certificado digital (no admite
        RUT y clave).

        :return: Listado de propiedades con identificación del rol,
            ubicación, inscripción, avalúos y contribuciones.
        :rtype: list[dict]
        """
        # TODO: Implementar.

    def certificado_avaluo_fiscal_simple_data(
        self, comuna: int, manzana: int, predio: int, eac: int
    ) -> Any:
        """
        Datos del certificado de avalúo fiscal simple de un bien raíz.

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Datos generales, avalúo, fecha de emisión y
            resultado de la consulta.
        :rtype: dict
        """
        # TODO: Implementar.

    def certificado_avaluo_fiscal_previo_data(
        self, comuna: int, manzana: int, predio: int, eac: int
    ) -> Any:
        """
        Datos del certificado de avalúo fiscal previo de un bien raíz.

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Datos generales, avalúo, fecha de emisión y
            resultado de la consulta.
        :rtype: dict
        """
        # TODO: Implementar.

    def certificado_antecedentes_data(
        self, comuna: int, manzana: int, predio: int, eac: int
    ) -> Any:
        """
        Datos del certificado de antecedentes de un bien raíz.

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Datos generales, avalúos, contribuciones, avalúo
            actualizado y fecha de emisión.
        :rtype: dict
        """
        # TODO: Implementar.

    def certificado_avaluo_fiscal_simple_pdf(
        self, comuna: int, manzana: int, predio: int, eac: int
    ) -> Any:
        """
        PDF del certificado de avalúo fiscal simple de un bien raíz.

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Contenido del PDF del certificado.
        :rtype: bytes
        """
        # TODO: Implementar.

    def certificado_avaluo_fiscal_previo_pdf(
        self, comuna: int, manzana: int, predio: int, eac: int
    ) -> Any:
        """
        PDF del certificado de avalúo fiscal previo de un bien raíz.

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Contenido del PDF del certificado.
        :rtype: bytes
        """
        # TODO: Implementar.

    def certificado_antecedentes_pdf(
        self, comuna: int, manzana: int, predio: int, eac: int
    ) -> Any:
        """
        PDF del certificado de antecedentes de un bien raíz.

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Contenido del PDF del certificado.
        :rtype: bytes
        """
        # TODO: Implementar.
