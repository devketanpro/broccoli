# Define the Docker app name
APP_NAME = broccoli

# Define the Docker build command
DOCKER_BUILD = docker build -t $(APP_NAME) .

DOCKER_CLEAN = ./clean.sh

# Define the Docker run command
DOCKER_RUN = docker container run -p 3000:3000 --env-file=.env -v $(APP_NAME):/app  $(APP_NAME)

# Define the Pytest run command
PYTEST_RUN = docker run --rm -v $(APP_NAME):/app $(APP_NAME) pipenv run pytest --cov=app --cov-report=html --cov-report=xml --cov-report=term-missing --cov-fail-under=100

# Define the rule to build the Docker image
build:
	$(DOCKER_BUILD)

# Define the rule to run the Docker container
run:
	$(DOCKER_RUN)

test:
	$(PYTEST_RUN)

# Define a clean rule to remove the Docker image
clean:
	$(DOCKER_CLEAN)