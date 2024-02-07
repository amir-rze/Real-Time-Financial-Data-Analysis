#!/bin/bash

docker login
docker build --tag amirrze/aggregation:v1.0.0 . -f Dockerfile
docker push amirrze/aggregation:v1.0.0