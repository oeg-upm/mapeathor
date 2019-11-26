FROM ubuntu:18.04
MAINTAINER David Chaves<dachafra@gmail.com>

USER root

# Python 3.6
RUN apt-get update && \
    apt-get install -y --no-install-recommends nano wget git curl less psmisc && \
    apt-get install -y --no-install-recommends python3.6 python3-pip python3-setuptools && \
    pip3 install --upgrade pip && \
    apt-get clean


COPY . /Mapeathor
RUN cp /Mapeathor/run.sh .
RUN cd /Mapeathor/code && pip3 install -r requirements.txt 

CMD ["tail", "-f", "/dev/null"]
