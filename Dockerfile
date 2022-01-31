FROM python:3.8-alpine
RUN mkdir -p /opt/arbiterd
COPY / /opt/arbiterd
RUN apk add --no-cache --virtual build-deps libvirt-dev python3-dev pkgconfig \
  gcc git build-base musl-dev  &&  python3.8 -m pip install /opt/arbiterd/ \
  && apk del build-deps && apk add --no-cache libvirt-libs
