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

import requests

from .. import ApiBase, Respuesta


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
    ) -> requests.Response:
        """
        Consulta un certificado de un bien raíz, por su rol.

        Los seis certificados comparten la misma ruta: sólo cambian el
        tipo de certificado y el formato de salida. Entrega la respuesta
        sin procesar para que cada método público tome el JSON o el PDF
        según corresponda.

        :param str certificado: `'avaluo_fiscal_simple'`,
            `'avaluo_fiscal_previo'` o `'antecedentes'`.
        :param str formato: `'data'` para JSON, `'pdf'` para el PDF.
        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Respuesta HTTP de la API.
        :rtype: requests.Response
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
        return self.client.get(url)

    def comunas(self) -> Respuesta[list[dict[str, Any]]]:
        """
        Listado de comunas de los bienes raíces.

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "codigoConaraSii": 5406,
                  "nombre": "ALGARROBO",
                  "regional": 5,
                  "codigo": 0,
                  "descripcion": null,
                  "descCorta": null
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, comunas con su código CONARA/SII, nombre, región, código
            y descripciones.
        :rtype: dict
        """
        response = self.client.get('/sii/bienes_raices/comunas')
        return self._json(response)

    def comuna(self, comuna: str) -> Respuesta[dict[str, Any]]:
        """
        Datos de una comuna de los bienes raíces, por nombre.

        Respuesta (ejemplo)::

            {
              "data": {
                "codigoConaraSii": 6205,
                "nombre": "SANTA CRUZ",
                "regional": 6,
                "codigo": 0,
                "descripcion": null,
                "descCorta": null
              },
              "metadata": {"timestamp": "..."}
            }

        :param str comuna: Nombre de la comuna a buscar.
        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, código CONARA/SII, nombre, región, código y
            descripciones de la comuna.
        :rtype: dict
        """
        body = {'filtros': {'comuna': comuna}}
        response = self.client.post('/sii/bienes_raices/comuna', data=body)
        return self._json(response)

    def propiedades_rol(
        self,
        comuna: int,
        manzana: int,
        predio: int,
    ) -> Respuesta[list[dict[str, Any]]]:
        """
        Propiedades de un bien raíz por su rol (comuna/manzana/predio).

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "comunaCnp": 6205,
                  "manzanaCnp": 123,
                  "predioCnp": 6,
                  "idRol": 0,
                  "comunaActual": 0,
                  "manzanaActual": 0,
                  "predioActual": 0,
                  "ultimoEacAplicado": 14,
                  "...": "..."
                }
              ],
              "metadata": {"timestamp": "..."}
            }

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
        return self._json(response)

    def propiedades_contribuyente(self) -> Respuesta[list[dict[str, Any]]]:
        """
        Propiedades del contribuyente autenticado.

        Requiere autenticación con certificado digital (no admite
        RUT y clave).

        Respuesta (ejemplo)::

            {
              "data": [
                {
                  "comunaCnp": 6205,
                  "manzanaCnp": 123,
                  "predioCnp": 6,
                  "idRol": 0,
                  "comunaActual": 0,
                  "manzanaActual": 0,
                  "predioActual": 0,
                  "ultimoEacAplicado": 14,
                  "...": "..."
                }
              ],
              "metadata": {"timestamp": "..."}
            }

        :return: Respuesta de la API, con `data` y `metadata`.
            En `data`, listado de propiedades con identificación del rol,
            ubicación, inscripción, avalúos y contribuciones.
        :rtype: dict
        """
        body = {'auth': self._get_auth()}
        response = self.client.post(
            '/sii/bienes_raices/propiedades/contribuyente',
            data=body,
        )
        return self._json(response)

    def certificado_avaluo_fiscal_simple_data(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
    ) -> Respuesta[dict[str, Any]]:
        """
        Datos del certificado de avalúo fiscal simple de un bien raíz.

        Respuesta (ejemplo)::

            {
              "data": {
                "datos_generales": {
                  "comuna": "SANTA CRUZ",
                  "rol": "00133-00026",
                  "direccion": "DANIEL BARROS GONZALEZ 121",
                  "destino": "HABITACIONAL",
                  "folio": "V189304624",
                  "codigo_verificacion": "312dqsdf-4978-4b68-859f-5f743c9a03fb"
                },
                "avaluo": {
                  "semestre": "segundo",
                  "año": 2025,
                  "total": 123456789.0
                },
                "fecha_emision": "12 de Diciembre de 2005",
                "error": null,
                "success": false
              },
              "metadata": {"timestamp": "..."}
            }

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Datos generales, avalúo, fecha de emisión y
            resultado de la consulta.
        :rtype: dict
        """
        response = self._certificado(
            'avaluo_fiscal_simple',
            'data',
            comuna,
            manzana,
            predio,
            eac,
        )
        return self._json(response)

    def certificado_avaluo_fiscal_previo_data(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
    ) -> Respuesta[dict[str, Any]]:
        """
        Datos del certificado de avalúo fiscal previo de un bien raíz.

        Respuesta (ejemplo)::

            {
              "data": {
                "datos_generales": {
                  "comuna": "SANTA CRUZ",
                  "rol": "00133-00026",
                  "direccion": "DANIEL BARROS GONZALEZ 121",
                  "destino": "HABITACIONAL",
                  "folio": "V189304624",
                  "codigo_verificacion": "312dqsdf-4978-4b68-859f-5f743c9a03fb"
                },
                "avaluo": {
                  "semestre": "segundo",
                  "año": 2025,
                  "total": 123456789.0
                },
                "fecha_emision": "12 de Diciembre de 2005",
                "error": null,
                "success": false
              },
              "metadata": {"timestamp": "..."}
            }

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Datos generales, avalúo, fecha de emisión y
            resultado de la consulta.
        :rtype: dict
        """
        response = self._certificado(
            'avaluo_fiscal_previo',
            'data',
            comuna,
            manzana,
            predio,
            eac,
        )
        return self._json(response)

    def certificado_antecedentes_data(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
    ) -> Respuesta[dict[str, Any]]:
        """
        Datos del certificado de antecedentes de un bien raíz.

        Respuesta (ejemplo)::

            {
              "data": {
                "datos_generales": {
                  "comuna": "CONCEPCIÓN",
                  "rol": "00321-00001",
                  "direccion": "AVENIDA ISLA DE MAIPO 3211",
                  "ubicacion": "URBANA",
                  "destino": "HABITACIONAL",
                  "serie": "NO AGRÍCOLA",
                  "semestre": null,
                  "folio": "00000000000000000000",
                  "...": "..."
                },
                "avaluos": {
                  "total": 125352123.0,
                  "exento": 125352123.0,
                  "afecto": 0.0,
                  "año_termino_exencion": 1988
                },
                "contribuciones": {
                  "neta": 0.0,
                  "sobretasa_sitios": 0.0,
                  "adicional": 0.0,
                  "sobretasa": 0.0,
                  "cuota_aseo": 0.0,
                  "total": 0.0
                },
                "avaluo_actualizado": 125352123.0,
                "fecha_emision": "16 de Diciembre de 2025"
              },
              "metadata": {"timestamp": "..."}
            }

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Datos generales, avalúos, contribuciones, avalúo
            actualizado y fecha de emisión.
        :rtype: dict
        """
        response = self._certificado(
            'antecedentes',
            'data',
            comuna,
            manzana,
            predio,
            eac,
        )
        return self._json(response)

    def certificado_avaluo_fiscal_simple_pdf(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
    ) -> bytes:
        """
        PDF del certificado de avalúo fiscal simple de un bien raíz.

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Contenido del PDF del certificado.
        :rtype: bytes
        """
        response = self._certificado(
            'avaluo_fiscal_simple',
            'pdf',
            comuna,
            manzana,
            predio,
            eac,
        )
        return response.content

    def certificado_avaluo_fiscal_previo_pdf(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
    ) -> bytes:
        """
        PDF del certificado de avalúo fiscal previo de un bien raíz.

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Contenido del PDF del certificado.
        :rtype: bytes
        """
        response = self._certificado(
            'avaluo_fiscal_previo',
            'pdf',
            comuna,
            manzana,
            predio,
            eac,
        )
        return response.content

    def certificado_antecedentes_pdf(
        self,
        comuna: int,
        manzana: int,
        predio: int,
        eac: int,
    ) -> bytes:
        """
        PDF del certificado de antecedentes de un bien raíz.

        :param int comuna: Código de la comuna.
        :param int manzana: Código de la manzana.
        :param int predio: Código del predio.
        :param int eac: Último EAC aplicado.
        :return: Contenido del PDF del certificado.
        :rtype: bytes
        """
        response = self._certificado(
            'antecedentes',
            'pdf',
            comuna,
            manzana,
            predio,
            eac,
        )
        return response.content
