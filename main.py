from machine import I2C, Pin
from ads1115 import ADS1115
import time

i2c = I2C(1, scl=Pin(22), sda=Pin(21))
ads = ADS1115(i2c, pga=1)
shunt_resistance = 1.0

while True:
    try:
        raw_a0 = ads.single_ended(0)
        bus_voltage = ads.raw_voltage(raw_a0)

        raw_a1 = ads.single_ended(1)
        voltage_a1 = ads.raw_voltage(raw_a1)

        shunt_voltage = bus_voltage - voltage_a1
        current = shunt_voltage / shunt_resistance

        print("{:.6f},{:.6f},{:.6f}".format(shunt_voltage, bus_voltage, current))

    except Exception as e:
        print("Error al leer sensor:", e)

    time.sleep(0.05)


