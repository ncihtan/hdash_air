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

# Build the Docker Lambda Image
docker_lambda_build:
	docker buildx build -f Dockerfile.lambda --platform linux/arm64 --provenance=false -t hdash-lambda:latest .
	@echo "AWS Lambda Docker image created"

# Run the Docker Lambda Container
docker_run_lambda:
	docker run --platform linux/arm64 -p 9000:8080 hdash-lambda:latest
	# curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'

# Push the Docker lambda image to AWS Elastic Container Registry (ECR)
docker_lambda_push:
	docker tag hdash-lambda:latest 507652762357.dkr.ecr.us-east-1.amazonaws.com/hdash-lambda:latest
	docker push 507652762357.dkr.ecr.us-east-1.amazonaws.com/hdash-lambda:latest
	@echo "Lambda Docker image pushed to AWS"

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

