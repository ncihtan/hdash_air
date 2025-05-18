PROJ_SLUG = hdash
CLI_NAME = hdash
PY_VERSION = 3.8
PY_LINT = pylint
PY_RIGHT = pyright
FLAKE8 = flake8
FORMATTER = black

# Prepare directories
prepare:
	mkdir -p deploy
	mkdir -p deploy/images
	mkdir -p tests/out

# Generate new requirements.txt dependencies file.
freeze:
	pip freeze > requirements.txt

# Run flake8 on all code
flake8:
	$(FLAKE8) $(PROJ_SLUG)
	$(FLAKE8) tests

# Run Pyright on all code
pyright:
	$(PY_RIGHT)

# Reformat all code via Black
format:
	$(FORMATTER) $(PROJ_SLUG)
	$(FORMATTER) tests

# Run all unit tests
test: prepare
	pytest -v -m "not smoke" tests

# Run smoke tests that require external dependencies, e.g. database, synapse, buckets.
smoke:
	pytest -v -m "smoke" tests

# Deploy to Apache Airflow Dev Directory
deploy:
	cp -R hdash $(AIRFLOW_DEV_HOME)
	cp hdash/dags/*.py $(AIRFLOW_DEV_HOME)/dags

# Deploy to Google Cloud Composer DAG Bucket
gcp:
	gsutil cp -r hdash $(HDASH_CLOUD_COMPOSER_DAG)
	gsutil cp hdash/dags/*.py $(HDASH_CLOUD_COMPOSER_DAG)

# Clean things up
clean:
	rm -rf deploy
