"""
This example cycles through the base colors in the Color circle.
2025-0804 PP restructuring workshop folder and Python file
2025-0802 PP modified 'multi-led' >> 'rgb:' in folder techlab-led/leds
"""
# 2025-08 $PYTHONPATH must contain folder 'lib' in folder 'pocketbeagle-2'
from sysfs import Device
from pathlib import Path
from time import sleep

# 2025-08 modified: LED = Path("/sys/devices/platform/techlab-led/leds/multi-led/")
LED = Path("/sys/devices/platform/techlab-led/leds/rgb:/")
DELAY = 1

led = Device(path=LED)

max_brightness = led.sysfs("max_brightness").read_str()
# Set brightness to max from the start
led.sysfs("brightness").write(max_brightness)

multi_intensity = led.sysfs("multi_intensity")

try:
    while True:
        multi_intensity.write('255 0 0')  #blue
        sleep(DELAY)

        multi_intensity.write('0 255 0')  #green
        sleep(DELAY)

        multi_intensity.write('0 0 255')  #red
        sleep(DELAY)

except KeyboardInterrupt:
    multi_intensity.write('0 0 0')  # RGB-LED off

finally:
    print("bye!")
