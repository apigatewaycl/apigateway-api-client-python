# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Agregar al PATH el código fuente del módulo apigatewaycl
import os
import sys
import tomllib
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'API Gateway: Cliente de API en Python'
author = 'API Gateway'

# La versión se lee de pyproject.toml para que no quede desfasada: antes
# estaba fija y la documentación siguió anunciando la 3 durante tres
# versiones mayores.
_pyproject = Path(__file__).parent.parent / 'pyproject.toml'
with _pyproject.open('rb') as _f:
    release = tomllib.load(_f)['project']['version']
version = release

copyright = '%(anio)s, API Gateway' % {
    'anio': datetime.now(tz=UTC).year,
}

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    # Publica el código fuente y agrega un enlace "[source]" en cada
    # clase y método: en un cliente de API sirve para ver qué URL arma
    # cada método sin salir de la documentación.
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

# Sin html_static_path: no hay recursos estáticos propios y apuntar a un
# directorio inexistente hacía que cada build emitiera un warning.
