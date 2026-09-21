"""Carga `tests/test.env` (no versionado) antes de correr los tests.

`tests/run.py` (el runner viejo) llamaba `load_dotenv()` a mano — con
`pytest` como runner nadie lo hacía todavía, así que las variables de
`tests/test.env` (token, RUT de prueba, etc.) no llegaban a los tests.
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / 'test.env')
