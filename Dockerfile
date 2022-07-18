FROM python:3.8.2-alpine3.11

RUN apk add --no-cache \
  bash \
  g++ \
  gcc \
  linux-headers

COPY . hs-test-python
RUN pip3 install --no-cache-dir ./hs-test-python

WORKDIR /hs-test-python
ENV PYTHONPATH=.

CMD ["bin/bash"]
