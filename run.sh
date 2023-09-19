#!/bin/bash

docker build -t broccoli .
docker run -p 8000:8000 -v broccoli:/app broccoli
