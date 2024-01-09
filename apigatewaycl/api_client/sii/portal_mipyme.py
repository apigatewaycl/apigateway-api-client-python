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
Módulo para consultas al Portal MIPYME del SII.

Para más información sobre la API, consulte la `documentación completa <https://developers.apigateway.cl/#d545a096-09be-4c9e-8d12-7b86b6bf1be6>`_.
"""

from .. import ApiBase

class PortalMipyme(ApiBase):
    """
    Base para los clientes específicos del Portal Mipyme.

    :param str usuario_rut: RUT del usuario.
    :param str usuario_clave: Clave del usuario.
    :param kwargs: Argumentos adicionales.
    """
    def __init__(self, usuario_rut, usuario_clave, **kwargs):
        super().__init__(usuario_rut=usuario_rut, usuario_clave=usuario_clave, **kwargs)

class Contribuyentes(PortalMipyme):
    """
    Cliente específico para interactuar con los endpoints de contribuyentes del Portal Mipyme.

    :param str usuario_rut: RUT del usuario.
    :param str usuario_clave: Clave del usuario.
    :param kwargs: Argumentos adicionales.
    """
    def info(self, contribuyente, emisor, dte=33):
        """
        Obtiene información de un contribuyente específico.

        :param str contribuyente: RUT del contribuyente.
        :param str emisor: RUT del emisor del DTE.
        :param int dte: Tipo de DTE.
        :return: Datos del contribuyente.
        :rtype: dict
        """
        body = {
            'auth': self._get_auth_pass()
        }
        r = self.client.post(f'/sii/mipyme/contribuyentes/info/{contribuyente}/{emisor}/{dte}', body)
        return r.json()

class Dte(PortalMipyme):
    """
    Base para los clientes específicos de DTE del Portal Mipyme.
    Incluye constantes para diferentes estados de DTE.

    :param str usuario_rut: RUT del usuario.
    :param str usuario_clave: Clave del usuario.
    :param kwargs: Argumentos adicionales.
    """
    ESTADO_EMITIDO = 'EMI' # Documento emitido
    ESTADO_BORRADOR = 'PRV' # Borrador (pre-view) de documento
    ESTADO_CERTIFICADO_RECHAZADO = 'DCD' # Certificado rechazado
    ESTADO_EMISOR_INVALIDO = 'DEI' # RUT emisor inválido
    ESTADO_FOLIO_INVALIDO = 'DFI' # Folio DTE inválido
    ESTADO_INCOMPLETO = 'DIN' # Incompleto
    ESTADO_FIRMA_SIN_PERMISO = 'DPF' # Sin permiso de firma
    ESTADO_FIRMA_RECHAZADA = 'DRF' # DTE rechazado por firma
    ESTADO_RECEPTOR_INVALIDO = 'DRI' # RUT receptor inválido
    ESTADO_REPETIDO = 'DRR' # Rechazado por repetido
    ESTADO_INICIALIZADO = 'INI' # DTE inicializado
    ESTADO_ACEPTADO = 'RAC' # DTE aceptado por receptor
    ESTADO_DISCREPANCIAS = 'RAD' # DTE aceptado con discrepancias
    ESTADO_NO_RECIBIDO = 'RNR' # DTE no recibido por receptor
    ESTADO_RECIBIDO = 'RRC' # DTE recibido por receptor
    ESTADO_ACEPTADO_LEY_19983 = 'RAL' # DTE aceptado Ley 19.983
    ESTADO_RECHAZADO_RECEPTOR = 'RRH' # DTE rechazado por receptor
    ESTADO_SIN_REPAROS = 'RSR' # Recibido sin reparos

    def get_codigo_dte(self, tipo):
        """
        Obtiene el código correspondiente al tipo de DTE.

        :param str tipo: Tipo de DTE.
        :return: Código del DTE.
        :rtype: str
        """
        return self.DTE_TIPOS[tipo] if tipo in self.DTE_TIPOS else tipo.replace(' ', '-')

class DteEmitidos(Dte):
    """
    Cliente específico para gestionar DTE emitidos en el Portal Mipyme.

    :param str usuario_rut: RUT del usuario.
    :param str usuario_clave: Clave del usuario.
    :param kwargs: Argumentos adicionales.
    """
    def documentos(self, emisor, filtros={}):
        """
        Obtiene documentos de DTE emitidos por un emisor.

        :param str emisor: RUT del emisor.
        :param dict filtros: Filtros adicionales para la consulta.
        :return: Documentos de DTE emitidos.
        :rtype: list[dict]
        """
        body = {
            'auth': self._get_auth_pass(),
            'filtros': filtros
        }
        r = self.client.post(f'/sii/mipyme/emitidos/documentos/{emisor}', body)
        return r.json()

    def pdf(self, emisor, dte, folio=None):
        """
        Obtiene el PDF de un DTE emitido.

        :param str emisor: RUT del emisor.
        :param str dte: Tipo de DTE o código del DTE emitido si no se pasa folio.
        :param str folio: Número de folio del DTE (opcional).
        :return: Contenido del PDF del DTE emitido.
        :rtype: bytes
        """
        body = {
            'auth': self._get_auth_pass()
        }
        resource = f'/sii/mipyme/emitidos/pdf/{emisor}/{dte}/{folio}' if folio else f'/sii/mipyme/emitidos/pdf/{emisor}/{dte}'
        r = self.client.post(resource, body)
        return r.content

    def xml(self, emisor, dte, folio):
        """
        Obtiene el XML de un DTE emitido.

        :param str emisor: RUT del emisor.
        :param str dte: Tipo de DTE.
        :param str folio: Número de folio del DTE.
        :return: Contenido del XML del DTE emitido.
        :rtype: str
        """
        body = {
            'auth': self._get_auth_pass()
        }
        r = self.client.post(f'/sii/mipyme/emitidos/xml/{emisor}/{dte}/{folio}', body)
        return r.text

class DteRecibidos(Dte):
    """
    Cliente específico para gestionar DTE recibidos en el Portal Mipyme.
    Proporciona métodos para obtener documentos, PDF y XML de DTE recibidos.

    :param str usuario_rut: RUT del usuario.
    :param str usuario_clave: Clave del usuario.
    :param kwargs: Argumentos adicionales.
    """

    def documentos(self, receptor, filtros={}):
        """
        Obtiene documentos de DTE recibidos por un receptor.

        :param str receptor: RUT del receptor.
        :param dict filtros: Filtros adicionales para la consulta.
        :return: Documentos de DTE recibidos.
        :rtype: list[dict]
        """
        body = {
            'auth': self._get_auth_pass(),
            'filtros': filtros
        }
        r = self.client.post(f'/sii/mipyme/recibidos/documentos/{receptor}', body)
        return r.json()

    def pdf(self, receptor, emisor, dte, folio=None):
        """
        Obtiene el PDF de un DTE recibido.

        :param str receptor: RUT del receptor.
        :param str emisor: RUT del emisor.
        :param str dte: Tipo de DTE o código del DTE recibido si no se pasa folio.
        :param str folio: Número de folio del DTE (opcional).
        :return: Contenido del PDF del DTE recibido.
        :rtype: bytes
        """
        body = {
            'auth': self._get_auth_pass()
        }
        resource = f'/sii/mipyme/recibidos/pdf/{receptor}/{emisor}/{dte}/{folio}' if folio else f'/sii/mipyme/recibidos/pdf/{receptor}/{emisor}/{dte}'
        r = self.client.post(resource, body)
        return r.content

    def xml(self, receptor, emisor, dte, folio):
        """
        Obtiene el XML de un DTE recibido.

        :param str receptor: RUT del receptor.
        :param str emisor: RUT del emisor.
        :param str dte: Tipo de DTE.
        :param str folio: Número de folio del DTE.
        :return: Contenido del XML del DTE recibido.
        :rtype: str
        """
        body = {
            'auth': self._get_auth_pass()
        }
        r = self.client.post(f'/sii/mipyme/recibidos/xml/{receptor}/{emisor}/{dte}/{folio}', body)
        return r.text
