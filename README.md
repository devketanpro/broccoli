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

3. Build the Docker image using the following command:

```commandline
make build
```

4. Once the image is built, run the Docker container using the following command:

```commandline
make run
```

5. The project will now be running on  `localhost:8000` .

## Cleaning Up

To remove the Docker image created for this project, use the following command:

```commandline
make clean
```

## Conclusion

You have successfully set up and run the **broccoli** project using Docker. Feel free to explore and modify the code to
suit your needs. If you encounter any issues or have any questions, please reach out to the project maintainers.