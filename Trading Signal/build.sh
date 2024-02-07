#!/bin/bash

docker login 
docker build --tag amirrze/trading:v2.0.0 . -f Dockerfile
docker push amirrze/trading:v2.0.0