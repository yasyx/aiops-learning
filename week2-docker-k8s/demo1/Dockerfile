# syntax=docker/dockerfile:1

FROM ubuntu:latest

LABEL org.opencontainers.image.authors="chengzilong237@gmail.com"


RUN apt-get update && apt install -y nginx 


CMD [ "nginx","-g","daemon off;" ]

