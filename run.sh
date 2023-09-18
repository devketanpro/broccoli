#!/bin/bash

docker build -t season-insight-app .
docker run -p 8000:8000 -v .:/app season-insight-app
