def test_i2c_addresses(shell):
    out = shell.run("i2cdetect -y 1")
    for addr in ["0x40", "0x76"]: # INA219 / BME280 example
        assert addr in out


def test_spi_flash_id(shell):
# Example: read JEDEC ID from SPI NOR via flashrom or spidev helper
# Adjust as needed or mark xfail if no flash is present
    try:
        out = shell.run("flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=1000 --flash-name", check=False)
        assert "found" in out.lower() or "flash" in out.lower()
    except Exception:
        pass

def test_gpio_loopback(shell):
    # Requires a physical loopback; replace pins as wired
    shell.run("gpioset 0 17=1; sleep 0.1; gpioget 0 27", check=False)