FROM python:3.8.2-alpine3.11

COPY . hs-test-python
RUN pip3 install --no-cache-dir ./hs-test-python

RUN apk add bash

WORKDIR /hs-test-python
ENV PYTHONPATH=.

CMD ["bin/bash"]
