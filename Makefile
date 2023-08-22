all: install dist

install:
	\
	python3 -m venv venv; \
	source venv/bin/activate; \
	pip install -r requirements.txt; \

dist:
	python3 setup.py sdist

upload: dist
	twine upload dist/*

clean:
	rm -rf dist libredte.egg-info libredte/__pycache__ libredte/*.pyc ejemplos/*.pdf
