Cliente API de LibreDTE para Python
===================================

.. image:: https://badge.fury.io/py/libredte.api-client.svg
    :target: https://pypi.python.org/pypi/libredte.api-client
.. .. image:: https://img.shields.io/pypi/status/libredte.api-client.svg
    :target: https://pypi.python.org/pypi/libredte.api-client
.. .. image:: https://img.shields.io/pypi/pyversions/libredte.api-client.svg
    :target: https://pypi.python.org/pypi/libredte.api-client
.. .. image:: https://img.shields.io/pypi/l/libredte.api-client.svg
    :target: https://raw.githubusercontent.com/LibreDTE/libredte-api-client-python/master/COPYING

Cliente para realizar la integración con los servicios web de la API de LibreDTE desde Python.

Este código está liberado bajo licencia `LGPL <http://www.gnu.org/licenses/lgpl-3.0.en.html>`_.
O sea, puede ser utilizado tanto en software libre como en software privativo.

Instalación
-----------

Instalar desde PIP con:

.. code:: shell

    $ sudo pip install libredte.api-client

Si estás en Microsoft Windows, debes instalar además
`pypiwin32 <https://pypi.python.org/pypi/pypiwin32>`_.

Actualización
-------------

Actualizar desde PIP con:

.. code:: shell

    $ sudo pip install libredte.api-client --upgrade

Desarrolladores (ayuda mental)
------------------------------

Modificar el cliente de la API:

.. code:: shell

    $ git clone https://github.com/LibreDTE/libredte-api-client-python
    $ cd libredte-api-client-python
    $ sudo pip install -e .

Crear el paquete que se desea distribuir:

.. code:: shell

    $ sudo python setup.py sdist

Publicar el paquete a distribuir:

.. code:: shell

    $ twine upload dist/*

Más información en `<http://python-packaging-user-guide.readthedocs.io/en/latest/distributing>`_
