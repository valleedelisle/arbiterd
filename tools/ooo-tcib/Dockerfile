FROM quay.io/tripleomastercentos9/openstack-tripleoclient:current-tripleo
ENV _BUILDAH_STARTED_IN_USERNS="" BUILDAH_ISOLATION=chroot
COPY build-images.sh /bin/build-images
RUN sudo mkdir -m 777 /work
