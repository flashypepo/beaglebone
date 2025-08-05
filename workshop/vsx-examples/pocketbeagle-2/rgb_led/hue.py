"""
This example generates different color hues on the RGB LED
2025-0802 PP: modified Path, add try-except
"""
from sysfs import Device
from pathlib import Path
from time import sleep


def wheel(pos: int) -> tuple[int, int, int]:
    if pos < 85:
        return (255 - pos * 3, 0, pos * 3)
    elif pos < 170:
        pos -= 85
        return (0, pos * 3, 255 - pos * 3)
    else:
        pos -= 170
        return (pos * 3, 255 - pos * 3, 0)


# PP modified: LED = Path("/sys/devices/platform/techlab-led/leds/multi-led/")
LED = Path("/sys/devices/platform/techlab-led/leds/rgb:/")
DELAY = 0.01

led = Device(path=LED)

max_brightness = led.sysfs("max_brightness").read_str()
# Set brightness to max from the start
led.sysfs("brightness").write(max_brightness)

multi_intensity = led.sysfs("multi_intensity")

try:
    while True:
        for i in range(0, 256):
            val = ' '.join(map(str, wheel(i)))
            #DEBUG: print(f"val={val}")
            multi_intensity.write(val)
            sleep(DELAY)

except KeyboardInterrupt:
    multi_intensity.write("0 0 0")  # LED off

finally:
    print("done!")
