# Embedded Test Lab (Starter)


This is a production‑grade starter repository for a Linux-based embedded test lab using pytest + labgrid. It targets a small device pod (e.g., Raspberry Pi 4 or similar SBC) with serial console, network boot/SSH, and remote power control. Adapt the placeholders to your hardware.


## Prereqs
- Ubuntu 22.04+ test host
- Network PDU or smart plug (API/SNMP) OR USB hub controllable via `uhubctl`
- USB‑UART adapter


## Configure
- Edit `hardware/labgrid.yaml` and `.env` (or set env vars in CI)
```bash
python3 -m venv .venv source .venv/bin/activate pip install -r requirements.txt
```
- Create a udev rule to pin your serial device

## Wire the DUT
- USB‑UART from host → DUT UART0 (115200 8N1)
- Ethernet from DUT → managed switch/VLAN (DHCP or static)
- Power → network PDU outlet (or USB hub port controllable via uhubctl)
- Fill in hardware/labgrid.yaml with your PDU, serial port, and DUT IP.

## Install sys dep
```bash
sudo apt-get update && sudo apt-get install -y
python3-pip git tmux jq iperf3 fio stress-ng
openocd dfu-util fastboot tftp-hpa nfs-kernel-server
bmap-tools flashrom usbutils i2c-tools lm-sensors ethtool
socat ser2net
```

## Run smoke suite:
```bash
pytest -q tests/smoke -n auto --maxfail=1 --junitxml=artifacts/junit-smoke.xml
```

## Run
```bash
make venv deps
make smoke
```

---


## Notes & Next Steps
- Replace placeholder IPs, serial ports, and PDU details with your lab values.
- If you’re not using labgrid’s dispatcher yet, this repo still works standalone via the pytest fixtures.
- For a device farm, layer in LAVA or labgrid exporter/remote and a results DB (e.g., Influx/Grafana).
- Add logging shipping (Loki/ELK) and baseline thresholds for perf tests as your data accumulates.
