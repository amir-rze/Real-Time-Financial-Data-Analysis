#!/bin/bash

docker login
docker build --tag amirrze/streaming:v2.0.0 . -f Dockerfile
docker push amirrze/streaming:v2.0.0