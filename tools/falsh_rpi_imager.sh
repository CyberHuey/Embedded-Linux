#!/usr/bin/env bash
set -euo pipefail
IMG=${1:-images/rpi4/raspios-lite.img}
DEV=${2:-/dev/sdX}


sudo umount ${DEV}* || true
sudo bmaptool copy "${IMG}" "${DEV}"
sync