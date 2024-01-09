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
Módulo para la emisión de Boletas de Terceros Electrónicas del SII.

Para más información sobre la API, consulte la `documentación completa <https://developers.apigateway.cl/#e08f50ab-5509-48ab-81ab-63fc8e5985e1>`_.
"""

from .. import ApiBase

class BteEmitidas(ApiBase):
    """
    Cliente específico para gestionar Boletas de Terceros Electrónicas (BTE) emitidas.

    Provee métodos para emitir, anular, y consultar información relacionada con BTEs.

    :param str usuario_rut: RUT del usuario.
    :param str usuario_clave: Clave del usuario.
    :param kwargs: Argumentos adicionales.
    """

    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super().__init__(usuario_rut=usuario_rut, usuario_clave=usuario_clave, **kwargs)

    def documentos(self, emisor, periodo):
        """
        Obtiene los documentos BTE emitidos por un emisor en un periodo específico.

        :param str emisor: RUT del emisor de las BTE.
        :param str periodo: Período de las BTE emitidas.
        :return: Respuesta JSON con los documentos BTE.
        :rtype: list[dict]
        """
        body = {
            'auth': self._get_auth_pass()
        }
        r = self.client.post(f'/sii/bte/emitidas/documentos/{emisor}/{periodo}', body)
        return r.json()

    def html(self, codigo):
        """
        Obtiene la representación HTML de una BTE emitida.

        :param str codigo: Código único de la BTE.
        :return: Contenido HTML de la BTE.
        :rtype: str
        """
        body = {
            'auth': self._get_auth_pass()
        }
        r = self.client.post(f'/sii/bte/emitidas/html/{codigo}', body)
        return r.content

    def emitir(self, datos):
        """
        Emite una nueva Boleta de Tercero Electrónica.

        :param dict datos: Datos de la boleta a emitir.
        :return: Respuesta JSON con la confirmación de la emisión de la BTE.
        :rtype: dict
        """
        body = {
            'auth': self._get_auth_pass(),
            'boleta': datos
        }
        r = self.client.post('/sii/bte/emitidas/emitir', body)
        return r.json()

    def anular(self, emisor, numero, causa=3, periodo=None):
        """
        Anula una BTE emitida.

        :param str emisor: RUT del emisor de la boleta.
        :param str numero: Número de la boleta.
        :param int causa: Causa de anulación.
        :param str periodo: Período de emisión de la boleta (opcional).
        :return: Respuesta JSON con la confirmación de la anulación.
        :rtype: dict
        """
        body = {
            'auth': self._get_auth_pass()
        }
        resource = f'/sii/bte/emitidas/anular/{emisor}/{numero}?causa={causa}'
        if periodo:
            resource += f'&periodo={periodo}'
        r = self.client.post(resource, body)
        return r.json()

    def receptor_tasa(self, emisor, receptor, periodo=None):
        """
        Obtiene la tasa de retención aplicada a un receptor por un emisor específico.

        :param str emisor: RUT del emisor de la boleta.
        :param str receptor: RUT del receptor de la boleta.
        :param str periodo: Período de emisión de la boleta (opcional).
        :return: Respuesta JSON con la tasa de retención.
        :rtype: dict
        """
        body = {
            'auth': self._get_auth_pass()
        }
        resource = f'/sii/bte/emitidas/receptor_tasa/{emisor}/{receptor}'
        if periodo:
            resource += f'?periodo={periodo}'
        r = self.client.post(resource, body)
        return r.json()
