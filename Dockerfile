FROM python:3.8-alpine
RUN mkdir -p -m 770 /etc/arbiterd /opt/arbiterd && \
    addgroup --system --gid 42473 libvirt && \
    addgroup --gid 42436 nova && \
    adduser -h /opt/arbiterd -D arbiterd && \
    addgroup arbiterd nova && \
    addgroup arbiterd libvirt
COPY container/entrypoint.sh dist/arbiterd*.whl /opt/arbiterd/
RUN apk add --no-cache --virtual \
      build-deps \
      libvirt-dev \
      python3-dev \
      pkgconfig \
      gcc \
      build-base \
      musl-dev && \
  python3.8 -m pip install /opt/arbiterd/arbiterd*.whl && \
  apk del build-deps && apk add --no-cache libvirt-libs sudo && \
  echo "arbiterd ALL=(ALL) NOPASSWD: /usr/local/bin/arbiterd-static" > /etc/sudoers.d/arbiterd && \
  wget https://github.com/Yelp/dumb-init/releases/download/v1.2.2/dumb-init_1.2.2_amd64 \
  -O /usr/local/bin/dumb-init && \
  chmod +x /usr/local/bin/dumb-init && \
  chown arbiterd:arbiterd /etc/arbiterd /opt/arbiterd
USER arbiterd
WORKDIR /opt/arbiterd
ENTRYPOINT [ "dumb-init", "--" ]
CMD [ "sh", "./entrypoint.sh" ]
