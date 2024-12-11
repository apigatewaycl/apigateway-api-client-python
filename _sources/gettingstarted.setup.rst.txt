Configuración
=============

Antes de empezar a utilizar el cliente de API de API Gateway Python, deberás considerar lo siguiente:

1. El tipo de cliente a utilizar.
2. Autenticación requerida para su uso.

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
del usuario de la API.

.. code:: python

    import apigatewaycl
    APIGATEWAY_API_TOKEN = "aquí-tu-token-de-usuario"
    SII_USUARIO_RUT = ""
    SII_USUARIO_CLAVE = ""
    rcv_client = Rcv(SII_USUARIO_RUT, SII_USUARIO_CLAVE, api_token = APIGATEWAY_API_TOKEN)

Si se usan variables de entorno, en ambos ejemplos se puede omitir el argumento `api_token`.
