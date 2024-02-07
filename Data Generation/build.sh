#!/bin/bash

docker login 
docker build --tag amirrze/generation:v2.0.0 . -f Dockerfile
docker push amirrze/generation:v2.0.0