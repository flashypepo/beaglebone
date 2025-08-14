"""
This example defines TechLab RGBLed

2025-0813 PP completed the animations fade etc.
TODO: separate class for animations
2025-0804 PP restructuring workshop folder and Python file
2025-0802 PP modified 'multi-led' >> 'rgb:' in folder techlab-led/leds
"""
from sysfs import Device
from pathlib import Path
from time import sleep


class RGBLed():
    # 2025-08 PP modified: LED = Path("/sys/devices/platform/techlab-led/leds/multi-led/")
    RGB_LED_SYS_PATH = "/sys/devices/platform/techlab-led/leds/rgb:/"

    def __init__(self):
        LED = Path(self.RGB_LED_SYS_PATH)
        self._led = Device(path=LED)
        self._max_brightness = self._led.sysfs("max_brightness")
        self._brightness = self._led.sysfs("brightness")
        self._multi_intensity = self._led.sysfs("multi_intensity")
        # initialise RGB-LED
        self.init()

    def init(self):
        # Set brightness to max from the start
        # type brightness is string not a number - see another example `usrled.py`.
        max_brightness = self._max_brightness.read_str()
        self._brightness.write(max_brightness)
        self._percentage = 1

    @property
    def intensity(self):
        return self._multi_intensity.read_str()

    @intensity.setter
    def intensity(self, value='0 0 0'):
        self._multi_intensity.write(str(value))

    @property
    def max_brightness(self):
        return self._max_brightness.read_str()

    @property
    def brightness(self):
        return self._brightness.read_str()

    @brightness.setter
    def brightness(self, value=1):
        assert 0 <= value <= 1, f"Value ({value}) must be in range [0..1]"
        self._percentage = value
        brightness = int(value * int(self.max_brightness))
        self._brightness.write(str(brightness))

    # =========================================
    # animations - should be different class
    # =========================================
    def color_cycle(self, colors, cycles=5):
        count = 1
        #TODO: brightness = self._percentage
        while count < cycles:  # True:
            print(f"{count}", end=' - ')
            for color in colors:
                #DEBUG:
                print(f"'{color}'", end=', ', flush=True)
                # scale the colors using brightness
                #print(f"{count} - '{color}'", end=', ')
                #new_color = tuple(c * brightness for c in color)  # reduced brightness color
                #print(f"reduced color - '{new_color}'")
                #rgbled.intensity(new_color)
                self.intensity = color
                sleep(DELAY)
            count += 1
        self.intensity = '0 0 0'  # RGBLed OFF

    def fade_intensity(self, cycles=5):
        print("fade_intensity...")
        DELAY = 0.05
        MAX_INTENSITY = 255

        # Set brightness to max from the start
        self.brightness = 1

        # PP color choices
        def BLUE(i=255):
            return f"{i} 0 0"

        def GREEN(i=255):
            return f"0 {i} 0"

        def RED(i=255):
            return f"0 0 {i}"

        color = BLUE  #RED  #GREEN  #BLUE  # select color function
        count = 1

        print(f"cycle color '{color()}':", end=' ', flush=True)
        while count < cycles + 1:
            print(f"{count}", end=', ', flush=True)
            # intensity up...
            for i in range(5, MAX_INTENSITY, 5):
                self.intensity = color(i)
                sleep(DELAY)

            # intensity down...
            for i in range(MAX_INTENSITY, -1, -5):
                self.intensity = color(i)
                sleep(DELAY)

            # next cycle
            count += 1
        print()
        self.intensity = '0 0 0'  # RGBLed OFF

    def fade_brightness(self, color, cycles=5):
        print("fade_brightness...")

        # set the color of the RGBLed
        self.intensity = color

        count = 1
        DELAY = 0.05
        max_brightness = int(self.max_brightness)  # values are strings from files!
        print(f"max brightness: {max_brightness}")

        while count < cycles + 1:
            print(f"{count}", end='... ', flush=True)
            # brightness up ...
            print("UP", end='... ', flush=True)
            for i in range (5, max_brightness, 5):
                 self.brightness = i / max_brightness
                 sleep(DELAY)

            # brightness down ...
            print("DOWN")
            for i in range(max_brightness, 5, -5):
                self.brightness = i / max_brightness
                sleep(DELAY)

            # next cycle
            count += 1
        self.intensity = '0 0 0'  # RGBLed OFF

    def hue(self, cycles=5):
        print("hue...")
        # helper wheel()
        def wheel(pos: int) -> tuple[int, int, int]:
            if pos < 85:
                return (255 - pos * 3, 0, pos * 3)
            elif pos < 170:
                pos -= 85
                return (0, pos * 3, 255 - pos * 3)
            else:
                pos -= 170
                return (pos * 3, 255 - pos * 3, 0)

        # Set brightness to max from the start
        #max_brightness = self.max_brightness
        self.brightness = 1  #max_brightness // max_brightness

        count = 1
        DELAY = 0.01
        print("cycle:", end=' ', flush=True)

        while count < cycles + 1:
            print(f"{count}", end=', ', flush=True)
            for i in range(0, 256):
                val = ' '.join(map(str, wheel(i)))
                #DEBUG: print(f"{val}", end=', ', flush=True)
                self.intensity = val
                sleep(DELAY)
            count += 1
        print()
        self.intensity = '0 0 0'  # RGBLed OFF


# test/demo animations
if __name__ == "__main__":
    rgbled = RGBLed()
    #rgbled.brightness = 0.5  # factor to reduce the brightness
    # factor < 0.5 -> green is not visible, blue hardly, red okay.
    print(f"brightness: {rgbled.brightness}")

    # PP color scheme is strange (RED and BLUE) -> DISCORD
    BLUE  = '255 0 0'
    GREEN = '0 255 0'
    RED   = '0 0 255'
    BLACK = '0 0 0'  # rgbled off
    DELAY = 1
    try:
        # cycle colors of RGBLed
        #rgbled.color_cycle(['255 0 0', '0 255 0', '0 0 255'], 5) # blue, green, red
        rgbled.color_cycle([BLUE, GREEN, RED, BLACK], 5) # blue, green, red, off
        sleep(DELAY)

        # fade intensity of RGBLed
        #rgbled.fade_intensity(color='255 0 0', cycles=5)
        rgbled.fade_intensity(cycles=5)
        sleep(DELAY)

        # fade brightness of RGBLed
        rgbled.fade_brightness(color=GREEN, cycles=5)
        sleep(DELAY)

        # cycle through hue colors of RGBLed
        rgbled.hue(cycles=5)
        sleep(DELAY)


    except KeyboardInterrupt:
        rgbled.intensity = BLACK  # RGB-LED off

    finally:
        print("bye!")
