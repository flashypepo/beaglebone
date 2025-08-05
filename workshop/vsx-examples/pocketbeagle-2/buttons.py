"""
This example demonstrates reading GPIO Buttons using the GPIO Keys kernel driver
2025-0805 PP added LEFT button, exception handling
"""
from chardev import CharDev

BUTTONS_NAME = "buttons"
RIGHT_CODE = 106
LEFT_CODE  = 105  # 2025-0805 PP - using libraries/chardev.py!

try:
    btn = CharDev.input_device_by_name(BUTTONS_NAME)
    print("Waiting for Input")

    while True:
        evt = btn.read_evt()

        # We use value to only print on pressed (not released) <- PP: WRONG!
        # PP: button PRESSED : evt.value=0
        #     button RELEASED: evt.value=1
        # see DEBUG in ../lib/chardev.py
        if evt.code == RIGHT_CODE and evt.value == 1:
            print("Right")
        #elif evt.code == LEFT_CODE and evt.value == 0:  # left-button pressed
        elif evt.code == LEFT_CODE and evt.value == 1:
            print("Left")
        else:
            pass

except KeyboardInterrupt:
    print("user interrupted...")

finally:
    print('done!')
