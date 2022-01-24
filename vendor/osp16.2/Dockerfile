FROM registry.redhat.io/rhosp-rhel8/openstack-nova-compute:latest
USER "root"
COPY I5dca10acde0eff554ed139587aefaf2f5fad2ca5.diff apply_arbirterd_patch.sh /tmp/
RUN /tmp/apply_arbirterd_patch.sh
USER "nova"
