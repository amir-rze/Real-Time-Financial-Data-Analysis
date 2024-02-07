#!/bin/bash

docker login 
docker build --tag amirrze/ingestion:v1.0.0 . -f Dockerfile
docker push amirrze/ingestion:v1.0.0