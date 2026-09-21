.PHONY: install-dev lint format format-check typecheck test test-readonly test-risky check docs build upload clean

VENV = .venv
VENV_READY = $(VENV)/.installed

$(VENV_READY): pyproject.toml
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -e '.[dev]'
	touch $(VENV_READY)

install-dev: $(VENV_READY)

lint: $(VENV_READY)
	$(VENV)/bin/ruff check .

format: $(VENV_READY)
	$(VENV)/bin/ruff format .

format-check: $(VENV_READY)
	$(VENV)/bin/ruff format --check .

typecheck: $(VENV_READY)
	$(VENV)/bin/mypy

# Solo los tests `dummy` (deterministas, seguros) — esto es lo único
# que corre CI. `readonly` y `risky` quedan para correr a mano.
test: $(VENV_READY)
	$(VENV)/bin/pytest -v

# Tests de solo lectura contra la API real, pero que necesitan datos
# específicos de una cuenta de prueba (RCV/BHE con historial, etc.).
test-readonly: $(VENV_READY)
	$(VENV)/bin/pytest -v -m readonly

# Tests que EMITEN/ANULAN/ENVÍAN algo real (BHE, BTE, email) — nunca
# automático, requieren las variables de entorno específicas de cada
# caso (ver tests/test.env-dist) y se corren a mano, uno por uno.
test-risky: $(VENV_READY)
	$(VENV)/bin/pytest -v -m risky

check: lint format-check typecheck test

docs: $(VENV_READY)
	$(VENV)/bin/pip install -e '.[docs]'
	$(VENV)/bin/sphinx-apidoc -o docs apigatewaycl --force --separate
	$(VENV)/bin/sphinx-build -b html docs docs/_build/html

build: $(VENV_READY)
	$(VENV)/bin/python -m build

upload: build
	$(VENV)/bin/twine upload dist/*

clean:
	rm -rf dist build *.egg-info .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
