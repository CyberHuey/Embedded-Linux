import re
import pytest


@pytest.mark.timeout(600)
def test_cpu_mem_baseline(shell):
    # Quick sanity: stress-ng for 10s and capture bogomips-like indicators
    shell.run("stress-ng --cpu 4 --vm 2 --vm-bytes 64M --timeout 10 --metrics-brief")


@pytest.mark.timeout(300)
def test_network_iperf_lan(shell):
    # Requires an iperf3 server reachable at env IPERF_SERVER
    import os
    srv = os.getenv("IPERF_SERVER", "10.0.1.2")
    out = shell.run(f"iperf3 -c {srv} -t 5 -J", check=False)
    assert 'end' in out or 'bits_per_second' in out