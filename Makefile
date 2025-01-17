all: dist

dist:
	python3 setup.py sdist

upload: dist
	twine upload dist/*

install-dev:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

tests: install-dev
	python tests/run.py

tests_readonly:
	python3 tests/run.py sii.actividades.test_listar_actividades_economicas
	python3 tests/run.py sii.contribuyentes.test_obtener_situacion_tributaria
	python3 tests/run.py sii.indicadores_uf.test_obtener_uf_anual
	python3 tests/run.py sii.indicadores_uf.test_obtener_uf_mensual
	python3 tests/run.py sii.indicadores_uf.test_obtener_uf_diario

docs:
	sphinx-apidoc -o docs apigatewaycl && sphinx-build -b html docs docs/_build/html

clean:
	rm -rf dist apigatewaycl.egg-info apigatewaycl/__pycache__ apigatewaycl/*.pyc
