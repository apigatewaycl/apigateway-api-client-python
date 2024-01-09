all: dist

dist:
	python3 setup.py sdist

upload: dist
	twine upload dist/*

install-dev:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

tests: install-dev
	python tests/run.py

docs:
	sphinx-apidoc -o docs apigatewaycl && sphinx-build -b html docs docs/_build/html

clean:
	rm -rf dist apigatewaycl.egg-info apigatewaycl/__pycache__ apigatewaycl/*.pyc
