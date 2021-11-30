
FROM python:3.8-alpine
COPY dist/arbiterd*.whl /opt/arbiterd/
RUN apk add --no-cache --virtual build-deps libvirt-dev python3-dev pkgconfig \
  gcc build-base musl-dev  &&  python3.8 -m pip install /opt/arbiterd/arbiterd*.whl \
  && apk del build-deps && apk add --no-cache libvirt-libs
