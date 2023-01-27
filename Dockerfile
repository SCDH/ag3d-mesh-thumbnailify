FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y python3-numpy blender

COPY tn.py /var/tn/tn.py
WORKDIR /var/tn/data


ENTRYPOINT ["blender", "--background", "--python", "../tn.py", "--"]
