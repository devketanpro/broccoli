# Project Readme

This Readme provides instructions on how to run the **broccoli** project using Docker.

## Prerequisites

To run this project, ensure that you have the following prerequisites installed:

- Docker: [Download and install Docker](https://www.docker.com/get-started)

## Getting Started

Follow the steps below to run the **broccoli** project:

1. Clone the repository:

```commandline
git clone https://github.com/devketanpro/broccoli.git
```

2. Navigate to the project directory:

```commandline
cd broccoli
```

3. Update environment variables:

Also create `.env` from `.env.example` file and update API_KEY with valid value from [platform.openai.com](https://platform.openai.com/account/api-keys)

4. Build the Docker image using the following command:

```commandline
make build
```

5. Once the image is built, run the Docker container using the following command:

```commandline
make run
```

6. The project will now be running on  `localhost:3000` .

## Cleaning Up

To remove the Docker image created for this project, use the following command:

```commandline
make clean
```

## Quick start

After completing third point please execute below file.  
```commandline
source run.sh
```

## Run Tests

To start pytest testing please execute below command.
```commandline
make test
```

## Clean setup

For cleaning all containers, image, volume related to app please execute below command.
```commandline
make clean
```

## Conclusion

You have successfully set up and run the **broccoli** project using Docker. Feel free to explore and modify the code to
suit your needs. If you encounter any issues or have any questions, please reach out to the project maintainers.