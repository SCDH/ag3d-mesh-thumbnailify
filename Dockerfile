FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y blender

WORKDIR /var/tn
COPY tn.py tn.py

ENTRYPOINT ["blender", "--background", "--python", "/var/tn/tn.py", "--"]
