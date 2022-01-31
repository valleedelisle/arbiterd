FROM registry.redhat.io/rhosp-rhel8/openstack-nova-compute:latest
USER "root"
RUN rm -rf /etc/yum.repos.d/*
COPY *.repo /etc/yum.repos.d/
COPY I5dca10acde0eff554ed139587aefaf2f5fad2ca5.diff apply_arbiterd_patch.sh /tmp/
RUN /tmp/apply_arbiterd_patch.sh
USER "nova"
