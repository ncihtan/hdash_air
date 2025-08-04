PROJ_SLUG = hdash
CLI_NAME = hdash
PY_VERSION = 3.8
PY_LINT = pylint
PY_RIGHT = pyright
FLAKE8 = flake8
FORMATTER = black

# Prepare directories
prepare:
	mkdir -p tests/out

# Generate new requirements.txt dependencies file.
freeze:
	pip freeze > requirements.txt

# Build the Docker Image for Linux/amd64
build_amd64:
	docker build --platform linux/amd64 -t hdash .

# Push to AWS Elastic Container Registry (ECR)
docker_push:
	docker tag hdash:latest 507652762357.dkr.ecr.us-east-1.amazonaws.com/hdash:latest
	docker push 507652762357.dkr.ecr.us-east-1.amazonaws.com/hdash:latest

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
