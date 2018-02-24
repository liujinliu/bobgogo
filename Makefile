all:
	@echo "do nothing"

clean:
	rm -f `find . -type f -name '*.py[co]' `
	rm -fr */*.egg-info build dist
	rm -fr *.egg-info

build: clean
	python setup.py sdist --formats=zip bdist_wheel --universal
	cp -R docs build/

install: build
	pip install dist/*.whl -U

uninstall:
	pip uninstall -y django-bobgogo

.PHONY : all clean build install uninstall
