# class LightSensor on the TechLab cape

#2025-0805 PP add threshold as argument in constructor
#2025-0804 PP restructured example -> class LightSensor

from time import sleep
from sysfs import Device


class LightSensor:
    THRESHOLD = 2000
    DEV_NAME = "ad7291"

    # setup lightsensor (adc) of the TechLab cape
    # 2025-0804 PP not sure if dev_name should be an argument
    def __init__(self, threshold=THRESHOLD, dev_name=DEV_NAME):
        # Reading values from ADC directly
        self._adc = Device(name=dev_name)
        self._threshold = threshold

    # returns raw reading of ldr
    @property
    def raw(self):
        return self._adc.sysfs("in_voltage0_raw").read_float()

    # returns in_voltage_scale of ldr
    @property
    def scale(self):
        return self._adc.sysfs("in_voltage_scale").read_float()

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
       self._threshold = value



if __name__ == "__main__":
    try:
        #lightsensor = LightSensor(dev_name="ad7291")
        lightsensor = LightSensor()  # default threshold and fixed ADC on Techlab cape

        # test a user threshold
        #user_threshold = 3000  # user-suplied threshold
        #lightsensor.threshold = user_threshold

        print(f"Light/Dark threshold: {lightsensor.threshold}")

        while True:
            scaled = lightsensor.raw * lightsensor.scale
            print(f"scaled voltage: {scaled:4.0f}", end='... ')

            now = "Light" if scaled > lightsensor.threshold else "Dark"
            print(now)

            sleep(0.5)

    except KeyboardInterrupt:
        print("user interrupted...")
    finally:
        print('done!')
