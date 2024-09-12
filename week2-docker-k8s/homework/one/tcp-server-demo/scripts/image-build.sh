#! /bin/bash
docker rmi `docker images | grep tcp-server-demo | awk '{print $3}'` && \
docker build -t yasyx/tcp-server-demo:v1.0 . && \
docker push yasyx/tcp-server-demo:v1.0