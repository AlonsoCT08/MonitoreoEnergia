from machine import I2C
import time

class ADS1115:
    PGA_RANGES = {
        0: 6.144,
        1: 4.096,
        2: 2.048,
        3: 1.024,
        4: 0.512,
        5: 0.256
    }

    def __init__(self, i2c, address=0x48, pga=1):
        self.i2c = i2c
        self.address = address
        self.config_reg = 0x01
        self.conversion_reg = 0x00
        self.pga = pga
        self.config = 0x8583

    def write_config(self, config):
        data = bytearray(3)
        data[0] = self.config_reg
        data[1] = (config >> 8) & 0xFF
        data[2] = config & 0xFF
        self.i2c.writeto(self.address, data)

    def read_conversion(self):
        data = self.i2c.readfrom_mem(self.address, self.conversion_reg, 2)
        raw = (data[0] << 8) | data[1]
        if raw > 0x7FFF:
            raw -= 0x10000
        return raw

    def build_config_diff_0_1(self, pga=None):
        if pga is None:
            pga = self.pga
        pga_bits = pga << 9

        config = 0
        config |= 0x8000  # OS bit (start conversion)
        config |= 0x0000  # MUX = 000 differential 0-1
        config |= pga_bits
        config |= 0x0100  # single-shot mode
        config |= 0x0080  # 128 SPS
        config |= 0x0003  # comparator disabled

        return config

    def build_config_single_ended(self, channel=0, pga=None):
        # channel: 0-3 (A0..A3)
        if pga is None:
            pga = self.pga
        pga_bits = pga << 9
        mux_bits = (0x04 + channel) << 12  # 100,101,110,111 for single-ended A0..A3

        config = 0
        config |= 0x8000  # OS bit
        config |= mux_bits
        config |= pga_bits
        config |= 0x0100  # single-shot mode
        config |= 0x0080  # 128 SPS
        config |= 0x0003  # comparator disabled

        return config

    def read_differential_0_1(self):
        config = self.build_config_diff_0_1()
        self.write_config(config)
        time.sleep_ms(10)
        return self.read_conversion()

    def read_single_ended(self, channel=0):
        config = self.build_config_single_ended(channel)
        self.write_config(config)
        time.sleep_ms(10)
        return self.read_conversion()

    def raw_to_voltage(self, raw):
        max_volt = self.PGA_RANGES.get(self.pga, 4.096)
        volts = raw * max_volt / 32768
        return volts

    def set_pga(self, pga):
        if pga in self.PGA_RANGES:
            self.pga = pga
        else:
            raise ValueError("PGA debe ser un valor entre 0 y 5")