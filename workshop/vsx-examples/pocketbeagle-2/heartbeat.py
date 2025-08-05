# 2025-0718 program activated when user logins (~/.profile)
# 2025-0718 PP USR3 trigger=USB-HOST
# 2025-0704 PP program a heartbeat on USR1
import time
from sysfs import Device
from pathlib import Path

USRID = 1   #USER-LED number (1..4)
print(f"trigger 'Heartbeat' on LED USR{USRID}")
LED  = Path(f"/sys/class/leds/beaglebone:green:usr{USRID}")
led1 = Device(path=LED)

USRID = 3   #USER-LED 3 -> USB-HOST trigger (debug)
print(f"trigger 'USB-HOST' on LED USR{USRID}")
LED = Path(f"/sys/class/leds/beaglebone:green:usr{USRID}")
led3 = Device(path=LED)

# helper function
def set_trigger(led, value):
    trigger = led.sysfs("trigger")
    #DEBUG: print(f"trigger={trigger}")
    trigger.write_str(value)

# reset triggers
set_trigger(led1, "none")  # trigger=none
set_trigger(led3, "none")  # trigger=none
time.sleep(0.5)  # trial-error/required?: wait

# set triggers
set_trigger(led1, "heartbeat")
set_trigger(led3, "usb-host")

print('done!')
