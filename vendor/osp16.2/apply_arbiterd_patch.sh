#!/bin/bash
set -ex
dnf install -y patch patchutils
# If you want to pick the patch from upstream right before the process, uncomment the following line:
#curl -L https://review.opendev.org/changes/openstack%2Fnova~821228/revisions/current/patch?download | base64 -d > /tmp/I5dca10acde0eff554ed139587aefaf2f5fad2ca5.diff
cat /tmp/I5dca10acde0eff554ed139587aefaf2f5fad2ca5.diff | filterdiff -x '*tests*' | patch -p1 -d /usr/lib/python3.*/site-packages -b
dnf remove -y patch patchutils
dnf clean all
