Ejemplos
========

Todos los ejemplos asumen que tienes el token de la API definido como
variable de entorno.

.. seealso::
    Para más información sobre este paso, referirse a la guía en
    Configuración.

Recuerda que los recursos que responden JSON entregan el cuerpo tal cual
lo envía la API, con ``data`` y ``metadata``.

Consultar un recurso público
----------------------------

Los indicadores y otros recursos públicos solo necesitan el token de la
plataforma: no requieren credenciales del contribuyente.

.. code-block:: python

    from apigatewaycl.api_client.sii.indicadores import Uf

    client = Uf()

    # El valor de la UF de un día. La respuesta trae la fecha
    # normalizada a AAAAMMDD como clave dentro de 'data'.
    respuesta = client.diario('2025-01-15')

    valores = respuesta['data']
    print('UF del 15-01-2025:', valores.get('20250115'))

    # 'metadata' trae los datos de la consulta, como la marca de tiempo.
    print('Consultado en:', respuesta['metadata']['timestamp'])

Autenticación con RUT y clave
-----------------------------

La mayoría de los recursos del SII requieren las credenciales del
contribuyente, que se pasan al instanciar la clase.

.. code-block:: python

    from os import getenv

    from apigatewaycl.api_client.sii.rcv import Rcv

    # RUT del contribuyente, sin puntos y con dígito verificador.
    identificador = getenv('SII_USUARIO_RUT', '12345678-9')
    clave = getenv('SII_USUARIO_CLAVE', 'claveSii')

    client = Rcv(identificador, clave)

    # Resumen de compras del período (AAAAMM).
    respuesta = client.compras_resumen(identificador, '202501')

    for resumen in respuesta['data'] or []:
        print(resumen)

Autenticación con certificado digital
-------------------------------------

Algunos recursos, como el CAF y los datos privados del contribuyente, no
admiten RUT y clave: exigen certificado digital. Se pasa en los mismos dos
argumentos, con el **certificado** en formato PEM como primer argumento y
la **llave privada**, también en PEM, como segundo.

Para obtener ambos desde tu firma electrónica (``.p12`` o ``.pfx``), sigue
el tutorial `Extraer el certificado y la clave privada con OpenSSL
<https://www.apigateway.cl/docs/tutoriales/extraer-pem>`_. Ese
procedimiento genera dos archivos, ``cert-data.txt`` y ``pkey-data.txt``,
que son los que se usan acá.

.. code-block:: python

    from pathlib import Path

    from apigatewaycl.api_client.sii.caf import Caf

    # Certificado: contiene uno o más bloques "BEGIN CERTIFICATE".
    certificado = Path('cert-data.txt').read_text()
    # Llave privada: "BEGIN PRIVATE KEY" o "BEGIN RSA PRIVATE KEY".
    llave_privada = Path('pkey-data.txt').read_text()

    client = Caf(certificado, llave_privada)

    # Folios timbrables y observaciones del SII, para facturas (33).
    respuesta = client.estado_timbraje('12345678-9', 33)

    datos = respuesta['data']
    print('Folios disponibles:', datos['dte']['folios_disponibles'])
    print('Contribuyente observado:', datos['contribuyente']['observado'])

.. note::
    El cliente reconoce el tipo de credencial por su contenido. Si el
    primer argumento es un RUT usa RUT y clave; si es un PEM lo toma
    como certificado y llave privada.

    Acepta el PEM tal como lo dejan los archivos del tutorial: en una
    sola línea con los saltos escapados, y con la cadena completa de
    certificación (varios bloques ``BEGIN CERTIFICATE``).

Descargar un archivo
--------------------

Los recursos que responden un archivo (PDF, XML, CSV o HTML) no entregan
JSON: devuelven el contenido sin decodificar, como ``bytes``. Por eso se
guardan en modo binario.

.. code-block:: python

    from apigatewaycl.api_client.sii.bhe import BheEmitidas

    client = BheEmitidas('12345678-9', 'claveSii')

    # El código de la boleta sale del listado del período.
    respuesta = client.documentos('12345678-9', '202501')
    boletas = respuesta['data']['boletas']

    pdf = client.pdf(boletas[0]['codigo'])

    with open('boleta.pdf', 'wb') as archivo:
        archivo.write(pdf)

Recorrer resultados paginados
-----------------------------

Los listados extensos vienen paginados. Según el recurso, la información
para avanzar está en ``data`` (por ejemplo ``n_paginas``) o en
``metadata`` (por ejemplo ``siguiente_pagina``, que vale ``None`` en la
última página).

.. code-block:: python

    from apigatewaycl.api_client.sii.bhe import BheEmitidas

    client = BheEmitidas('12345678-9', 'claveSii')

    boletas = []
    pagina = 1

    while True:
        datos = client.documentos('12345678-9', '202501', pagina)['data']
        if not datos:
            break
        boletas += datos['boletas']
        if pagina >= datos['n_paginas']:
            break
        pagina += 1

    print('Boletas del período:', len(boletas))

Manejar los errores
-------------------

Cualquier error de la API (credenciales inválidas, parámetros que faltan,
o un rechazo del propio SII) se levanta como ``ApiException``.

.. code-block:: python

    from apigatewaycl.api_client import ApiException
    from apigatewaycl.api_client.sii.contribuyentes import Contribuyentes

    client = Contribuyentes()

    try:
        respuesta = client.situacion_tributaria('12345678-9')
        print(respuesta['data'])
    except ApiException as error:
        # El mensaje incluye el detalle que entrega la API.
        print('Falló la consulta:', error)

Emitir una BHE
--------------

El siguiente es un ejemplo completo de cómo emitir un documento BHE.

Opcionalmente, puedes definir como variables de entorno el identificador y
la clave del SII, o definirlos directamente en el programa.

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
    respuesta = client.emitir(datos_bhe)

    # La API responde {'data': ..., 'metadata': {...}}: el resultado de
    # la emisión está en 'data'.
    emitir = respuesta['data']

    # Se despliega el resultado en consola, para confirmar.
    print('\nEMISION BOLETA: \n')
    print('\nEmitir BHE ejemplo: ', emitir, '\n')

.. seealso::
    Para saber más sobre los parámetros posibles y el cómo consumir los servicios de la API, referirse a la `documentación de API Gateway. <https://www.apigateway.cl/docs>`_
