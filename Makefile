# Define the target name
TARGET = season-insight-app

# Define the Docker image name
IMAGE_NAME = season-insight-app

# Define the Docker build command
DOCKER_BUILD = docker build -t $(IMAGE_NAME) .

# Define the Docker run command
DOCKER_RUN = docker run -p 8000:8000 -v .:/app $(IMAGE_NAME)

# Define the rule to build the Docker image
build:
	$(DOCKER_BUILD)

# Define the rule to run the Docker container
run:
	$(DOCKER_RUN)

# Define a clean rule to remove the Docker image
clean:
	docker rmi $(IMAGE_NAME)