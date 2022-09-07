FROM python:3.6-alpine3.15

RUN apk add --no-cache \
  bash \
  g++ \
  gcc \
  linux-headers

RUN pip install --no-cache-dir \
  matplotlib \
  seaborn  \
  pandas  \
  numpy

COPY . hs-test-python
RUN pip3 install --no-cache-dir ./hs-test-python

WORKDIR /hs-test-python
ENV PYTHONPATH=.

CMD ["bash"]
