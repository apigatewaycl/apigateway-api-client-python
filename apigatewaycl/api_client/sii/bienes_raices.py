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
de Bienes Raíces <https://www.apigateway.cl/docs>`_.
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

    :param str identificador: Identificador del contribuyente
        (opcional, sólo lo usa `propiedades_contribuyente()`).
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

        Ambos son opcionales: salvo `propiedades_contribuyente()`,
        todos los recursos de bienes raíces son públicos.
        """
        argumentos: dict[str, str] = dict(kwargs)
        if identificador and clave:
            argumentos['identificador'] = identificador
            argumentos['clave'] = clave
        super().__init__(
            **argumentos,  # type: ignore[arg-type]
        )

    def _certificado(
        self,
        certificado: str,
        formato: str,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
    ) -> Any:
        """
        Consulta un certificado de un bien raíz, por su rol.

        Los seis certificados comparten la misma ruta: sólo cambian el
        tipo de certificado y el formato de salida.

        :param str certificado: `'avaluo_fiscal_simple'`,
            `'avaluo_fiscal_previo'` o `'antecedentes'`.
        :param str formato: `'data'` para JSON, `'pdf'` para el PDF.
        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, datos del certificado, o el contenido del PDF.
        :rtype: dict | bytes
        """
        url = (
            '/sii/bienes_raices/certificados/%(certificado)s/%(formato)s'
            '/%(comuna)s/%(manzana)s/%(predio)s/%(eac)s'
            % {
                'certificado': certificado,
                'formato': formato,
                'comuna': comuna,
                'manzana': manzana,
                'predio': predio,
                'eac': eac,
            }
        )
        response = self.client.get(url)
        if formato == 'pdf':
            return response.content
        return response.json()

    def comunas(self) -> Any:
        """
        Listado de comunas de los bienes raíces.

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, comunas con su código CONARA/SII, nombre, región, código
            y descripciones.
        :rtype: dict
        """
        response = self.client.get('/sii/bienes_raices/comunas')
        return response.json()

    def comuna(self, comuna: str) -> Any:
        """
        Datos de una comuna de los bienes raíces, por nombre.

        :param str comuna: Nombre de la comuna a buscar.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, código CONARA/SII, nombre, región, código y
            descripciones de la comuna.
        :rtype: dict
        """
        body = {'filtros': {'comuna': comuna}}
        response = self.client.post('/sii/bienes_raices/comuna', data=body)
        return response.json()

    def propiedades_rol(
        self,
        comuna: int,
        manzana: int,
        predio: int,
    ) -> Any:
        """
        Propiedades de un bien raíz por su rol (comuna/manzana/predio).

        :param int comuna: Código de la comuna.
        :param int manzana: Número de manzana.
        :param int predio: Número de predio.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de propiedades con identificación del rol,
            ubicación, inscripción, avalúos y contribuciones.
        :rtype: dict
        """
        url = (
            '/sii/bienes_raices/propiedades/rol'
            '/%(comuna)s/%(manzana)s/%(predio)s'
            % {'comuna': comuna, 'manzana': manzana, 'predio': predio}
        )
        response = self.client.get(url)
        return response.json()

    def propiedades_contribuyente(self) -> Any:
        """
        Propiedades del contribuyente autenticado.

        Requiere autenticación con certificado digital (no admite
        RUT y clave).

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de propiedades con identificación del rol,
            ubicación, inscripción, avalúos y contribuciones.
        :rtype: dict
        """
        body = {'auth': self._get_auth_pass()}
        response = self.client.post(
            '/sii/bienes_raices/propiedades/contribuyente',
            data=body,
        )
        return response.json()

    def certificado_avaluo_fiscal_simple_data(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
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
        return self._certificado(
            'avaluo_fiscal_simple',
            'data',
            comuna,
            manzana,
            predio,
            eac,
        )

    def certificado_avaluo_fiscal_previo_data(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
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
        return self._certificado(
            'avaluo_fiscal_previo',
            'data',
            comuna,
            manzana,
            predio,
            eac,
        )

    def certificado_antecedentes_data(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
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
        return self._certificado(
            'antecedentes',
            'data',
            comuna,
            manzana,
            predio,
            eac,
        )

    def certificado_avaluo_fiscal_simple_pdf(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
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
        return self._certificado(
            'avaluo_fiscal_simple',
            'pdf',
            comuna,
            manzana,
            predio,
            eac,
        )

    def certificado_avaluo_fiscal_previo_pdf(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
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
        return self._certificado(
            'avaluo_fiscal_previo',
            'pdf',
            comuna,
            manzana,
            predio,
            eac,
        )

    def certificado_antecedentes_pdf(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
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
        return self._certificado(
            'antecedentes',
            'pdf',
            comuna,
            manzana,
            predio,
            eac,
        )
