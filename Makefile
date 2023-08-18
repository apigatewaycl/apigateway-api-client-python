all: install dist

install:
	pip install -e .

dist:
	python setup.py sdist

upload: dist
	twine upload dist/*

clean:
	rm -rf dist libredte.egg-info libredte/__pycache__ libredte/*.pyc ejemplos/*.pdf
