#!/usr/bin/env bash
set -euo pipefail


# TFTP root
sudo mkdir -p /srv/tftp && sudo chown -R tftp:tftp /srv/tftp || true
# NFS root
sudo mkdir -p /srv/nfs/rpi-rootfs
sudo bash -c 'echo "/srv/nfs/rpi-rootfs *(rw,sync,no_subtree_check,no_root_squash)" >> /etc/exports'
sudo exportfs -ra