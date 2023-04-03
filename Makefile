AIRFLOW_HOME = ~/Desktop/astro
PROJ_SLUG = hdash
CLI_NAME = hdash
PY_VERSION = 3.8
PY_LINT = pylint
FLAKE8 = flake8
FORMATTER = black

check: format lint test

prepare:
	mkdir -p deploy
	mkdir -p deploy/images
	mkdir -p tests/out

freeze:
	pip freeze > requirements.txt

lint:
	$(PY_LINT) -j 0 $(PROJ_SLUG)
	$(PY_LINT) -j 0 tests

flake8:
	$(FLAKE8) $(PROJ_SLUG)
	$(FLAKE8) tests

format:
	$(FORMATTER) $(PROJ_SLUG)
	$(FORMATTER) tests

test: prepare
	pytest -v -m "not smoke" tests

smoke:
	pytest -v -m "smoke" tests

deploy:
	cp -R hdash $(AIRFLOW_HOME)
	cp hdash/dags/*.py $(AIRFLOW_HOME)/dags

clean:
	rm -rf deploy
