#!/bin/sh
sudo rm -rf output/*

podman run --privileged --rm -it -v /home/sean/repos/arbiterd/vendor:/vendor \
-v /home/sean/repos/arbiterd/tools/ooo-tcib/output:/output:rw \
tcib build-images

for ct in output/*/Dockerfile; do
    echo $ct | awk -F / '{cmd="podman build -f " $0 " -t " $2":current-tripleo"; system(cmd)}' ;
done
