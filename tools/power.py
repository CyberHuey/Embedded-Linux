#!/usr/bin/env python3
import os
import time
import subprocess


# Example SNMP-based power toggle for APC PDU; replace OIDs/methods for your device
# For smart plugs or USB hubs, branch on POWER_BACKEND env var.


BACKEND = os.getenv("POWER_BACKEND", "apc_snmp")
PDU_HOST = os.getenv("PDU_HOST", "apc-pdu-01.lan")
PDU_OUTLET = int(os.getenv("PDU_OUTLET", "5"))
SNMP_COMM = os.getenv("SNMP_COMM", "public")


# OIDs here are examples; confirm for your PDU model
OIDS = {
"on": f"iso.3.6.1.4.1.318.1.1.4.4.2.1.3.1.{PDU_OUTLET}",
"off": f"iso.3.6.1.4.1.318.1.1.4.4.2.1.3.1.{PDU_OUTLET}",
}




def _snmpset(value: int):
    cmd = [
    "snmpset", "-v2c", "-c", SNMP_COMM, PDU_HOST, OIDS["off"], "i", str(value)
    ]
    return subprocess.run(cmd, check=True)




def power_cycle(delay=2.0):
    if BACKEND == "apc_snmp":
        _snmpset(2) # 2=immediateOff (example)
        time.sleep(delay)
        _snmpset(1) # 1=immediateOn
    elif BACKEND == "uhubctl":
        hub = os.getenv("USB_HUB", "1-1")
        port = os.getenv("USB_PORT", "2")
        subprocess.run(["uhubctl", "-l", hub, "-p", port, "-a", "0"], check=True)
        time.sleep(delay)
        subprocess.run(["uhubctl", "-l", hub, "-p", port, "-a", "1"], check=True)
    else:
        raise SystemExit(f"Unsupported power backend: {BACKEND}")


if __name__ == "__main__":
    power_cycle()