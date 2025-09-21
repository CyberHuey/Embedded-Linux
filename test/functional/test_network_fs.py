def test_network_connectivity(shell):
    shell.run("ping -c 2 8.8.8.8")
    shell.run("ping -c 2 $(ip route | awk '/default/{print $3}')")

def test_filesystem_health(shell):
    out = shell.run("df -hT | awk '{print $1, $2, $6}'")
    assert "/" in out
    shell.run("sudo dmesg | tail -n 200", check=False)