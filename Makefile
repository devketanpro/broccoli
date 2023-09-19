# Define the target name
TARGET = broccoli

# Define the Docker image name
IMAGE_NAME = broccoli

# Define the Docker build command
DOCKER_BUILD = docker build -t $(IMAGE_NAME) .

# Define the Docker run command
DOCKER_RUN = docker run -p 8000:8000 -v broccoli:/app $(IMAGE_NAME)

# Define the rule to build the Docker image
build:
	$(DOCKER_BUILD)

# Define the rule to run the Docker container
run:
	$(DOCKER_RUN)

test:
	pytest --cov=app --cov-report=html

# Define a clean rule to remove the Docker image
clean:
	docker rmi -f $(IMAGE_NAME)