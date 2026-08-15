Pruebas Unitarias
=================

Las pruebas utilizan un archivo llamado `test.env`, que sirve para definir todas las variables de entorno
necesarias para ejecutar estas pruebas.

Estas pruebas utilizan `unittest`, se ejecutan con el archivo `run.py`, y dependiendo de cómo se configure
`test.env`, se pueden omitir ciertas pruebas. Asegúrate de definir las siguientes variables en `test.env`,
o no podrás efectuar la mayoría de las pruebas:

 - `APIGATEWAY_API_URL`
 - `APIGATEWAY_API_TOKEN`
 - `TEST_CONTRIBUYENTE_IDENTIFICADOR`
 - `TEST_CONTRIBUYENTE_CLAVE`
 - `TEST_USUARIO_IDENTIFICADOR`
 - `TEST_USUARIO_CLAVE`
 - `TEST_PORTAL_MIPYME_CONTRIBUYENTE_RUT`

Para ejecutar las pruebas unitarias, debes ejecutar el siguiente código en consola desde la raíz del proyecto:

.. code:: shell

    python tests/run.py

Si quieres ejecutar una prueba específica, deberás especificar el nombre y ruta:

.. code:: shell

    python tests/run.py sii.actividades.test_listar_actividades_economicas
    python tests/run.py sii.bhe_emitidas.test_listar_bhes_emitidas

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