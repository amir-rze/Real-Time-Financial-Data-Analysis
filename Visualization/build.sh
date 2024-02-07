#!/bin/bash

docker login 
docker build --tag amirrze/visualization:v1.0.0 . -f Dockerfile
docker push amirrze/visualization:v1.0.0