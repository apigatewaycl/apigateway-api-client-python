Cliente API Gateway para Python
===============================

.. image:: https://badge.fury.io/py/libredte.api-client.svg
    :target: https://pypi.python.org/pypi/libredte.api-client
.. .. image:: https://img.shields.io/pypi/status/libredte.api-client.svg
    :target: https://pypi.python.org/pypi/libredte.api-client
.. .. image:: https://img.shields.io/pypi/pyversions/libredte.api-client.svg
    :target: https://pypi.python.org/pypi/libredte.api-client
.. .. image:: https://img.shields.io/pypi/l/libredte.api-client.svg
    :target: https://raw.githubusercontent.com/LibreDTE/libredte-api-client-python/master/COPYING

Cliente para realizar la integración con los servicios web de API Gateway (www.apigateway.cl) desde Python.

Este código está liberado bajo licencia `LGPL <http://www.gnu.org/licenses/lgpl-3.0.en.html>`_.
O sea, puede ser utilizado tanto en software libre como en software privativo.

Instalación
-----------

Instalar desde PIP con:

.. code:: shell

    $ sudo pip install libredte.api-client

Actualización
-------------

Actualizar desde PIP con:

.. code:: shell

    $ sudo pip install libredte.api-client --upgrade

Cliente genérico vs clientes específicos
----------------------------------------

Este cliente de API Gateway tiene 2 formas de acceder a los recursos:

-   Cliente genérico: es un cliente que permite consumir de manera sencilla cualquier
    recurso de la API. Que actualmente exista o sea añadido en el futuro. Esto se logra
    porque el cliente recibe los nombres de los recursos, la parte de la URL que permite
    acceder al servicio web solicitado. Se proveen métodos que sólo sirven para acceder
    a la API de manera genérica, pero no para hacer acciones específicas ni obtener los
    datos en un formato específico. Este cliente es el que entrega mayor flexibilidad, ya
    que cada programador decide qué recursos desea consumir y cómo desea obtener los datos.

-   Clientes específicos: son clases que permiten acceder de forma más natural a los
    recursos de la API. Al instanciar la clase, se tendrán métodos sencillos con parámetros
    para consumir la API. Sin ser necesario preocuparse de recordar o buscar en la
    documentación el nombre de los recursos que se deben consumir. Además de entregar los
    datos ya "listos" para ser usados en vez de tener que preocuparse de qué método del
    cliente genérico usar para obtenerlos en el formato requerido.

Autenticación en API Gateway
----------------------------

Lo más simple es usar una variable de entorno con el *access token* de www.apigateway.cl:

.. code:: shell

    export LIBREDTE_API_TOKEN=""

Si no se desea usar una variable de entorno, al crear los objetos clientes se
deberá indicar el *access token*. Ejemplo con el cliente genérico:

.. code:: python

    cliente_libredte = LibreDTE(ACCESS_TOKEN)

El siguiente es un ejemplo con el cliente específico de Rcv, se pasan los datos
obligatorios de RUT y clave del usuario y además se pasa el *access token* de
la API.

.. code:: python

    cliente_rcv = Rcv(USUARIO_RUT, USUARIO_CLAVE, api_token = ACCESS_TOKEN)

Si se usan variables de entorno, en ambos ejemplos se puede omitir el *access token*.

Desarrolladores (ayuda mental)
------------------------------

Modificar el cliente de la API:

.. code:: shell

    $ git clone https://github.com/LibreDTE/apigateway-client-python
    $ cd apigateway-client-python
    $ sudo pip install -e .

Crear el paquete que se desea distribuir:

.. code:: shell

    $ sudo python setup.py sdist

Publicar el paquete a distribuir:

.. code:: shell

    $ twine upload dist/*

Más información en `<http://python-packaging-user-guide.readthedocs.io/en/latest/distributing>`_
