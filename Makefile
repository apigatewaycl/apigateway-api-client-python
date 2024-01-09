all: install dist

install:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

dist:
	python3 setup.py sdist

upload: dist
	twine upload dist/*

tests: install
	python tests/run.py

docs:
	sphinx-apidoc -o docs apigatewaycl && sphinx-build -b html docs docs/html

clean:
	rm -rf dist apigatewaycl.egg-info apigatewaycl/__pycache__ apigatewaycl/*.pyc
