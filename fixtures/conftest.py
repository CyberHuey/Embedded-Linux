import os
import time
import pexpect
import pytest
import paramiko


PDU_BACKEND = os.getenv("POWER_BACKEND", "apc_snmp")
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
SERIAL_BAUD = int(os.getenv("SERIAL_BAUD", "115200"))
DUT_IP = os.getenv("DUT_IP", "10.0.1.101")
SSH_USER = os.getenv("SSH_USER", "root")
SSH_PASS = os.getenv("SSH_PASS", "")


@pytest.fixture(scope="session")
def power():
    class Power:
        def cycle(self):
            os.system("python3 tools/power.py")
    return Power()


@pytest.fixture()
def serial():
    child = pexpect.spawn(
    f"picocom -b {SERIAL_BAUD} {SERIAL_PORT}", timeout=60
    )
    yield child
    try:
        child.sendcontrol('a'); child.send('x')
    except Exception:
        pass


@pytest.fixture()
def boot_to_shell(power, serial):
    power.cycle()
    serial.expect(["login:", "#", ":~#", "\$"], timeout=120)
    # auto-login systems may drop directly to shell
    return True


@pytest.fixture()
def shell():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for _ in range(30):
        try:
            ssh.connect(DUT_IP, username=SSH_USER, password=SSH_PASS, timeout=5)
            break
        except Exception:
            time.sleep(2)
    else:
        raise RuntimeError("SSH unreachable after timeout")


    def run(cmd, check=True):
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode()
        err = stderr.read().decode()
        rc = stdout.channel.recv_exit_status()
        if check and rc != 0:
            raise RuntimeError(f"cmd failed ({rc}): {cmd}\n{err}")
        return out

    yield type("Shell", (), {"run": run})
    ssh.close()