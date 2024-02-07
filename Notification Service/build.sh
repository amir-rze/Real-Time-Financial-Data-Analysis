#!/bin/bash

docker login 
docker build --tag amirrze/notification:v2.0.0 . -f Dockerfile
docker push amirrze/notification:v2.0.0