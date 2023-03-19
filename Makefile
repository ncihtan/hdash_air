AIRFLOW_HOME = ~/Desktop/astro
PROJ_SLUG = hdash
CLI_NAME = hdash
PY_VERSION = 3.8
LINTER = flake8
FORMATTER = black

check: format lint test

prepare:
	mkdir -p deploy
	mkdir -p deploy/images

freeze:
	pip freeze > requirements.txt

lint:
	$(LINTER) $(PROJ_SLUG)
	$(LINTER) tests

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
