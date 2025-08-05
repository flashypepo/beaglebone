# 2025-0802 PP modified LED path: multi-led -> rgb:, experiments with colors, add keyboardinterrupt

# 2025-0804 $PYTHONPATH must contain  folder 'lib' in folder 'pocketbeagle-2'
from sysfs import Device
from pathlib import Path
from time import sleep

# PP modified: LED = Path("/sys/devices/platform/techlab-led/leds/multi-led/")
LED = Path("/sys/devices/platform/techlab-led/leds/rgb:/")
DELAY = 0.05

led = Device(path=LED)
brightness = led.sysfs('brightness')
max_brightness = led.sysfs('max_brightness').read_int()
print(f"max.brightness = {max_brightness}")

# Set intensity to a single color
# 2025-0804 PP modified - color scheme is strange (RED and BLUE)
BLUE  = '255 0 0'
GREEN = '0 255 0'
RED   = '0 0 255'
color = GREEN  #BLUE  #RED  # select the color
#led.sysfs('multi_intensity').write('255 0 0')  # blue
#led.sysfs('multi_intensity').write('0 255 0')  # green
#led.sysfs('multi_intensity').write('0 0 255')   # red
led.sysfs('multi_intensity').write(color)   # show color

try:
    while True:
        for i in range(5, max_brightness, 5):
            brightness.write(i)
            sleep(DELAY)

        for i in range(max_brightness, -1, -5):
            brightness.write(i)
            sleep(DELAY)

except KeyboardInterrupt:
    brightness.write(0)  # LED off

finally:
    print('done!')

