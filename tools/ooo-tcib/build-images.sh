#!/bin/bash
openstack tripleo container image build --config-file /vendor/containers.yaml --config-path /vendor --skip-build --work-dir /work
mv $(realpath /work/$(ls /work))/* /output
