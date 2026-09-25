#
# API Gateway: Cliente de API en Python - Pruebas Unitarias.
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

import unittest
from datetime import datetime, timedelta
from os import getenv
from zoneinfo import ZoneInfo

import pytest

from apigatewaycl.api_client import ApiException
from apigatewaycl.api_client.sii.eboleta import EboletaEmitidas

pytestmark = pytest.mark.readonly


class TestObtenerDocumentoEboleta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verbose = bool(int(getenv('TEST_VERBOSE', '0')))
        identificador = getenv(
            'TEST_CONTRIBUYENTE_IDENTIFICADOR',
            '',
        ).strip()
        clave = getenv('TEST_CONTRIBUYENTE_CLAVE', '').strip()
        if not (identificador and clave):
            raise unittest.SkipTest(
                'Se requieren TEST_CONTRIBUYENTE_IDENTIFICADOR y '
                'TEST_CONTRIBUYENTE_CLAVE.'
            )
        cls.contribuyente = getenv(
            'TEST_EBOLETA_CONTRIBUYENTE',
            '',
        ).strip()
        if not cls.contribuyente:
            raise unittest.SkipTest(
                'TEST_EBOLETA_CONTRIBUYENTE no configurado (RUT sin '
                'puntos ni dígito verificador).'
            )
        cls.client = EboletaEmitidas(identificador, clave)
        hoy = datetime.now(ZoneInfo('America/Santiago')).date()
        cls.date_from = getenv(
            'TEST_EBOLETA_DESDE',
            (hoy - timedelta(days=30)).isoformat(),
        ).strip()
        cls.date_to = getenv('TEST_EBOLETA_HASTA', hoy.isoformat()).strip()

    def _primera_boleta(self):
        documentos = self.client.documentos(
            self.contribuyente,
            self.date_from,
            self.date_to,
        )['data']
        boletas = documentos.get('data') or documentos
        if not boletas:
            self.skipTest(
                'la API no devolvió boletas con las cuales probar.',
            )
        return boletas[0]

    def test_obtener_documento_eboleta(self):
        try:
            boleta = self._primera_boleta()
            documento = self.client.documento(
                self.contribuyente,
                boleta['folio'],
                boleta['dte'],
                boleta['fecha'],
            )['data']

            self.assertIsNotNone(documento)

            if self.verbose:
                print('test_documento(): documento', documento)
        except (ApiException, KeyError) as e:
            self.fail('%(t)s: %(e)s' % {'t': type(e).__name__, 'e': e})
