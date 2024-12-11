Ejemplo
=======

Ejemplo de listar BHEs
----------------------

El siguiente es un ejemplo básico de cómo obtener un listado de documentos BHE utilizando el cliente de API.

Para utilizar el cliente de API de API Gateway, deberás tener definido el token de API como variable de entorno.

.. seealso::
    Para más información sobre este paso, referirse al la guía en Configuración.

Opcionalmente, puedes definir como variables de entorno el identificador y la clave del SII, o definirlos directamente en el programa.

.. code-block:: python

    # Importaciones del cliente de API de API Gateway
    from os import getenv
    from datetime import datetime
    from apigatewaycl.api_client.sii.bhe import BheEmitidas

    # RUT de contribuyente SII sin puntos y con Dígito Verificador. (Reemplazar segundo valor si)
    identificador = getenv('TEST_USUARIO_IDENTIFICADOR', '12345678-9').strip()
    # Clave de contribuyente SII.
    clave = getenv('TEST_USUARIO_CLAVE', 'claveSii').strip()

    # Creación de nueva instancia de cliente de API
    client = BheEmitidas(identificador, clave)

    # RUT del emisor del BHE, sin puntos y con Dígito Verificador.
    contribuyente_rut = '12345678-9'
    # RUT del receptor, sin puntos y con Dígito Verificador.
    receptor_rut = '66666666-6'
    # Fecha de emisión de la BHE.
    fecha_emision = datetime.now().strftime("%Y-%m-%d")

    datos_bhe = {
        'Encabezado': {
            'IdDoc': {
                'FchEmis': fecha_emision,
                'TipoRetencion': BheEmitidas.RETENCION_EMISOR
            },
            'Emisor': {
                'RUTEmisor': contribuyente_rut
            },
            'Receptor': {
                'RUTRecep': receptor_rut,
                'RznSocRecep': 'Receptor generico',
                'DirRecep': 'Santa Cruz',
                'CmnaRecep': 'Santa Cruz'
            }
        },
        'Detalle': [
            {
                'NmbItem': 'Prueba integracion API Gateway 1',
                'MontoItem': 50
            },
            {
                'NmbItem': 'Prueba integracion API Gateway 2',
                'MontoItem': 100
            }
        ]
    }
    # Llamado al método de emitir en BheEmitidas().
    emitir = client.emitir(datos_bhe)

    # Se despliega el resultado en consola, para confirmar.
    print('\nBHE RECIBIDAS: \n')
    print('\nBHE Emitidas(): emitir', emitir, '\n')

.. seealso::
    Para saber más sobre los parámetros posibles y el cómo consumir los servicios de la API, referirse a la `documentación de API Gateway. <https://developers.apigateway.cl/>`_
