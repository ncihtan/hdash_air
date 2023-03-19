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

freeze:
	pip freeze > requirements.txt

lint:
	$(PY_LINT) $(PROJ_SLUG)
	$(PY_LINT) tests
	$(FLAKE8) $(PROJ_SLUG)
	$(FLAKE8) tests

format:
	$(FORMATTER) $(PROJ_SLUG)
	$(FORMATTER) tests

test:  prepare
	python3 -s -m pytest tests/

deploy:
	cp -R hdash $(AIRFLOW_HOME)
	cp hdash/dags/*.py $(AIRFLOW_HOME)/dags

clean:
	rm -rf deploy