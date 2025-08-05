# 2025-0804 PP add try-except, $PYTHONPATH

from sysfs import Device
from pathlib import Path
from time import sleep

#PP modified: LED = Path("/sys/devices/platform/techlab-led/leds/multi-led/")
LED = Path("/sys/devices/platform/techlab-led/leds/rgb:/")
DELAY = 0.05
MAX_INTENSITY = 255

led = Device(path=LED)

max_brightness = led.sysfs("max_brightness").read_str()
# Set brightness to max from the start
led.sysfs("brightness").write(max_brightness)

multi_intensity = led.sysfs("multi_intensity")

# PP add color choices
def BLUE(i):
    return f"{i} 0 0"

def GREEN(i):
    return f"0 {i} 0"

def RED(i):
    return f"0 0 {i}"

color = RED  #GREEN  #BLUE  # select color
try:
    while True:
        for i in range(5, MAX_INTENSITY, 5):
            #multi_intensity.write(f"{i} 0 0")
            multi_intensity.write(color(i))
            sleep(DELAY)

        for i in range(MAX_INTENSITY, -1, -5):
            #multi_intensity.write(f"{i} 0 0")
            multi_intensity.write(color(i))
            sleep(DELAY)

except KeyboardInterrupt:
    multi_intensity.write("0 0 0")  # LED off

finally:
    print("done!")

