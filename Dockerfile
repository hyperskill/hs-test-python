FROM python:3.9.13-alpine3.16

RUN apk add --no-cache \
  bash \
  g++ \
  gcc \
  linux-headers

COPY . hs-test-python
RUN pip3 install --no-cache-dir ./hs-test-python

WORKDIR /hs-test-python
ENV PYTHONPATH=.

CMD ["bash"]
