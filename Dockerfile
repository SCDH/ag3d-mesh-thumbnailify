FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y blender

COPY tn.py /var/tn/tn.py
WORKDIR /var/tn/data


ENTRYPOINT ["blender", "--background", "--python", "../tn.py", "--"]
