FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

# Install Python
RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install -y python3-pip

COPY ./antichess /app
WORKDIR /app

RUN pip3 install -r requirements.txt