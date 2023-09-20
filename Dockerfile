# Use the official Python image for Python 3.10
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install pipenv
RUN pipenv install

# Expose the port that FastAPI will run on (default is 3000)
EXPOSE 3000

# Define the command to run your FastAPI application
CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
