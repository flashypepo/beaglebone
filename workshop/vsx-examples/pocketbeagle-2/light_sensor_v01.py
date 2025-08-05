# 2025-0804 PP restructured example
# 2025-0804 PP make sure $PYTHONPATH contains folder 'lib' of folder 'pocketbeagle-2'
# Reading values from ADC directly

from time import sleep
from sysfs import Device

THRESHOLD = 2000

# setup an adc
def setup_adc():
    DEV_NAME = "ad7291"
    adc = Device(name=DEV_NAME)
    return adc


# returns raw reading of ldr
def get_ldr_raw(sensor):
    ldr_raw = sensor.sysfs("in_voltage0_raw").read_float()
    return ldr_raw


# returns in_voltage_scale of ldr
def get_scale(sensor):
    scale = sensor.sysfs("in_voltage_scale").read_float()
    return scale


try:
    adc = setup_adc()
    print(f"Light/Dark threshold: {THRESHOLD}")
    while True:
        ldr_raw = get_ldr_raw(adc)
        scale = get_scale(adc)
        scaled = ldr_raw * get_scale(adc)
        print(f"inv_voltage0_raw_scaled: {scaled:4.0f}", end='... ')

        now = "Light" if scaled > THRESHOLD else "Dark"
        print(now)
        #if scaled > THRESHOLD:
        #    print("Light")
        #else:
        #    print("Dark")
        sleep(0.5)

except KeyboardInterrupt:
    print("user interrupted...")

finally:
    print('done!')
