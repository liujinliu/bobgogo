all:
	@echo "do nothing"

clean:
	rm -f `find . -type f -name '*.py[co]' `
	rm -fr */*.egg-info build dist
	rm -fr *.egg-info

build: clean
	python setup.py build_py bdist_wheel

install: build
	pip install dist/*.whl -U

uninstall:
	pip uninstall -y django-bobgogo

.PHONY : all clean build install uninstall
