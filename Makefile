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

# Build the Docker Fargate Image
# On Mac, this will create an ARM64 image, compatible with AWS Graviton2.
docker_fargate_build:
	docker build -f Dockerfile.fargate -t hdash .
	@echo "Fargate Docker image created"

# Push the Docker hdash image to AWS Elastic Container Registry (ECR)
docker_fargate_push:
	docker tag hdash:latest 507652762357.dkr.ecr.us-east-1.amazonaws.com/hdash:latest
	docker push 507652762357.dkr.ecr.us-east-1.amazonaws.com/hdash:latest
	@echo "Docker image pushed to AWS"

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

