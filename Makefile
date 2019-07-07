.PHONY: clean clean-test clean-pyc clean-build docs help
# .DEFAULT_GOAL := help

clean: clean-build clean-pyc clean-test

test: test-py2 test-py3
	python3 -m robot.rebot \
	  --outputdir  tests/results \
	  tests/results/py2/output.xml \
	  tests/results/py2/demo/output.xml \
	  tests/results/py3/output.xml \
	  tests/results/py3/demo/output.xml

test-py3:
	python3 -m robot \
	    --argumentfile tests/conf/default.args \
	    --name  "Python 3 Tests" \
	    --outputdir tests/results/py3 \
	    --variable BROWSER:chrome \
	    tests

test-py2:
	python2 -m robot \
	    --argumentfile tests/conf/default.args \
	    --name  "Python 2 Tests" \
	    --outputdir tests/results/py2 \
	    --variable BROWSER:chrome \
	    tests

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test:
	rm -rf tests/results/*

release: clean dist
	twine upload dist/*

dist: clean
	python setup.py sdist
	ls -l dist


