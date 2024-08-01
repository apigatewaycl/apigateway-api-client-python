API Gateway: Cliente de API en Python
=====================================

.. image:: https://badge.fury.io/py/apigatewaycl.svg
    :target: https://pypi.org/project/apigatewaycl
.. image:: https://img.shields.io/pypi/status/apigatewaycl.svg
    :target: https://pypi.org/project/apigatewaycl
.. image:: https://img.shields.io/pypi/pyversions/apigatewaycl.svg
    :target: https://pypi.org/project/apigatewaycl
.. image:: https://img.shields.io/pypi/l/apigatewaycl.svg
    :target: https://raw.githubusercontent.com/apigatewaycl/apigateway-api-client-python/master/COPYING

Cliente para realizar la integración con los servicios web de `API Gateway <https://www.apigateway.cl>`_ desde Python.

Instalación y actualización
---------------------------

Instalar usando un entorno virtual y PIP con:

.. code:: shell

    python3 -m venv venv
    source venv/bin/activate
    pip install apigatewaycl

Actualizar usando PIP con:

.. code:: shell

    pip install apigatewaycl --upgrade

Cliente genérico vs clientes específicos
----------------------------------------

Este cliente de API Gateway tiene 2 formas de acceder a los recursos de la API:

1.  Cliente genérico: es un cliente que permite consumir de manera sencilla cualquier
    recurso de la API. Que actualmente exista o sea añadido en el futuro. Esto se logra
    porque el cliente recibe los nombres de los recursos, la parte de la URL que permite
    acceder al servicio web solicitado. Se proveen métodos que sólo sirven para acceder
    a la API de manera genérica, pero no para hacer acciones específicas ni obtener los
    datos en un formato específico. Este cliente es el que entrega mayor flexibilidad, ya
    que cada programador decide qué recursos desea consumir y cómo desea obtener los datos.

2.  Clientes específicos: son clases que permiten acceder de forma más natural a los
    recursos de la API. Al instanciar la clase, se tendrán métodos sencillos con parámetros
    para consumir la API. Sin ser necesario preocuparse de recordar o buscar en la
    documentación el nombre de los recursos que se deben consumir. Además de entregar los
    datos ya "listos" para ser usados en vez de tener que preocuparse de qué método del
    cliente genérico usar para obtenerlos en el formato requerido.

Autenticación en API Gateway
----------------------------

Lo más simple, y recomendado, es usar una variable de entorno con el
`token del usuario <https://apigateway.cl/dashboard#api-auth>`_, la cual será
reconocida automáticamente por el cliente:

.. code:: shell

    export APIGATEWAY_API_TOKEN="aquí-tu-token-de-usuario"

Si no se desea usar una variable de entorno, al instanciar los objetos se
deberá indicar el token del usuario. Ejemplo con el cliente genérico:

.. code:: python

    import apigatewaycl
    APIGATEWAY_API_TOKEN = "aquí-tu-token-de-usuario"
    client = apigatewaycl.api_client.ApiClient(APIGATEWAY_API_TOKEN)

El siguiente es un ejemplo con el cliente específico de Rcv. Primero se pasan
los datos obligatorios de RUT y clave del usuario. Luego además se pasa el token
delusuario de la API.

.. code:: python

    import apigatewaycl
    APIGATEWAY_API_TOKEN = "aquí-tu-token-de-usuario"
    SII_USUARIO_RUT = ""
    SII_USUARIO_CLAVE = ""
    rcv_client = Rcv(SII_USUARIO_RUT, SII_USUARIO_CLAVE, api_token = APIGATEWAY_API_TOKEN)

Si se usan variables de entorno, en ambos ejemplos se puede omitir el argumento `api_token`.

Pruebas
-------

Las pruebas utilizan un archivo llamado `test.env`, que sirve para definir todas las variables de entorno
necesarias para ejecutar estas pruebas.

Estas pruebas utilizan `unittest`, se ejecutan con el archivo `run.py`, y dependiendo de cómo se configure
`test.env`, se pueden omitir ciertas pruebas. Asegúrate de definir las siguientes variables en `test.env`,
o no podrás efectuar la mayoría de las pruebas:

 - `APIGATEWAY_API_URL`
 - `APIGATEWAY_API_TOKEN`
 - `TEST_CONTRIBUYENTE_RUT`
 - `TEST_CONTRIBUYENTE_CLAVE`
 - `TEST_USUARIO_RUT`
 - `TEST_USUARIO_CLAVE`
 - `TEST_PORTAL_MIPYME_CONTRIBUYENTE_RUT`

Para ejecutar las pruebas unitarias, debes ejecutar el siguiente código en consola desde la raíz del proyecto:

.. code:: shell

    python tests/run.py

Si quieres ejecutar una prueba específica, deberás especificar el nombre y ruta:

.. code:: shell

    python tests/run.py sii.test_actividades_economicas.TestSiiActividadesEconomicas.test_listado

Para ejecutar otros ejemplos, deberás reemplazar desde `test_actividades_economicas` para adelante por el nombre
y ruta de alguna de las otras pruebas descritas posteriormente.

A continuación se pondrán instrucciones de cómo probar el cliente de API de Python:

* `test_actividades_economicas`:
    * `test_listado()`:
        - Prueba que permite obtener un listado de todas las Actividades económicas del SII por omisión.
        - Ruta completa: `sii.test_actividades_economicas.TestSiiActividadesEconomicas.test_listado`
        - Variables necesarias: `Ninguna`
        - Variable de ejecución: `Ninguna`
    * `test_listado_primera_categoria()`:
        - Prueba que permite obtener un listado de todas las Actividades económicas de primera categoría del SII.
        - Ruta completa: `sii.test_actividades_economicas.TestSiiActividadesEconomicas.test_listado_primera_categoria`
        - Variables necesarias: `Ninguna`
        - Variable de ejecución: `Ninguna`
    * `test_listado_segunda_categoria()`:
        - Prueba que permite obtener un listado de todas las Actividades económicas de segunda categoría del SII.
        - Ruta completa: `sii.test_actividades_economicas.TestSiiActividadesEconomicas.test_listado_segunda_categoria`
        - Variables necesarias: `Ninguna`
        - Variable de ejecución: `Ninguna`
* `test_bhe_emitidas`:
    * `test_documentos()`
        - Prueba que permite obtener todas las BHE emitidas por un contribuyente.
        - Ruta completa: `sii.test_bhe_emitidas.TestSiiBheEmitidas.test_documentos`
        - Variables necesarias: `Ninguna`
        - Variable de ejecución: `Ninguna`
    * `test_pdf()`
        - Prueba que permite obtener el PDF de una BHE emitida.
        - Ruta completa: `sii.test_bhe_emitidas.TestSiiBheEmitidas.test_pdf`
        - Variables necesarias: `TEST_PERIODO`
        - Variable de ejecución: `len(documentos)`
    * `test_emitir()`
        - Prueba que permite emitir una BHE.
        - Ruta completa: `sii.test_bhe_emitidas.TestSiiBheEmitidas.test_emitir`
        - Variables necesarias: `TEST_BHE_EMITIDAS_RECEPTOR_RUT`, `TEST_BHE_EMITIDAS_FECHA_EMISION`
        - Variable de ejecución: `TEST_BHE_EMITIDAS_RECEPTOR_RUT`
    * `test_email()`
        - Prueba que permite enviar un email a un destinatario con su BHE emitida.
        - Ruta completa: `sii.test_bhe_emitidas.TestSiiBheEmitidas.test_email`
        - Variables necesarias: `TEST_BHE_EMITIDAS_BOLETA_CODIGO`, `TEST_BHE_EMITIDAS_RECEPTOR_EMAIL`
        - Variable de ejecución: `TEST_BHE_EMITIDAS_BOLETA_CODIGO`, `TEST_BHE_EMITIDAS_RECEPTOR_EMAIL`
    * `test_anular()`
        - Prueba que permite anular una BHE emitida.
        - Ruta completa: `sii.test_bhe_emitidas.TestSiiBheEmitidas.test_anular`
        - Variables necesarias: `TEST_BHE_EMITIDAS_BOLETA_NUMERO`
        - Variable de ejecución: `TEST_BHE_EMITIDAS_BOLETA_NUMERO`

Licencia
--------

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
`GNU Lesser General Public License <http://www.gnu.org/licenses/lgpl.html>`_.

Enlaces
-------

- `Sitio web API Gateway <https://www.apigateway.cl>`_.
- `Código fuente en GitHub <https://github.com/apigatewaycl/apigateway-api-client-python>`_.
- `Paquete en PyPI <https://pypi.org/project/apigatewaycl>`_.
- `Documentación en Read the Docs <https://apigatewaycl.readthedocs.io/es/latest>`_.
