# 2025-0813 PP modified using class USRLED
  # Technically, max_brightness will be an unsigned integer value. However,
  # since we never actually parse it, and writing to the file needs conversion
  # back to string anyway, it is better to just keep it as string
# 2025-0806 PP added a count in print
import time
from sysfs import Device
from pathlib import Path


class USRLED():
    LEDPATH = "/sys/class/leds/beaglebone:green:usr"

    def __init__(self, usrled=4):
        LED = Path(self.LEDPATH + str(usrled))
        print(f"usrled: {LED}")  # DEBUG
        self._number_of_led = usrled  # PP: useful?
        self._led = Device(path=LED)
        self._max_brightness = self._led.sysfs("max_brightness")
        self._brightness = self._led.sysfs("brightness")

    def on(self, brightness=None):
        """
         on() - turn on the usrled
             brightness, string: the brightness of the led, "0".."255"(?)
         see remark about type of brightness in header
        """
        b = self._max_brightness.read_str() if brightness is None else str(brightness)
        self._brightness.write_str(b)

    def off(self):
        """
         off() - turn off the usrled
         see remark about type of brightness in header
        """
        self._brightness.write_str("0")

    def blinks(self, cycles=5):
        count = 0  # counter
        for blinks in range(cycles):
            count += 1
            print(f"{count} - ON", end=' ... ', flush=True)  # print immediately
            led.on()  # max brightness
            time.sleep(1) # 1 second on

            led.off()
            print("OFF")
            time.sleep(1) # 1 second off

    @property
    def id(self):
        return self._number_of_led

    def __str__(self):
        return f"USRLED({self.id})"




# test/demo
if __name__ == "__main__":
    led = USRLED(4)
    print(led)
    led.blinks(5)
