"""
This example demonstrates reading GPIO Buttons using the GPIO Keys kernel driver

== WORK_IN_PROGRESS==

2025-0813 PP left and right button do work, however skipped button events 
             - event 'release' works best!
             - somehow it has to do with read_evt()
2025-0812 PP added class Button and methods inspired by Adafruit learning guide
             "Python Debouncer Library for Buttons and Sensors"
2025-0805 PP added LEFT button, exception handling, print on PRESSED
"""
from chardev import CharDev

# class Buttons
class Buttons:
    BUTTONS_NAME = "buttons"
    RIGHT_CODE  = 106
    LEFT_CODE  = 105  # 2025-0805 PP - using libraries/chardev.py!

    def __init__(self, code):
        assert code in [self.LEFT_CODE, self.RIGHT_CODE], f"Buttons: illegal code {code}"
        self._btn = CharDev.input_device_by_name(self.BUTTONS_NAME)
        self._code = code

    def __str__(self):
        return f"Buttons({self._code})"

    # value: returns evt.value
    @property
    def value(self):
        evt = self._btn.read_evt()
        #print(f"value `evt`: ({evt.code}, {evt.value})")
        return evt.value

    # code: returns True if correct button is pressed/released
    @property
    def code(self):
        evt = self._btn.read_evt()
        #print(f"code `evt`: ({evt.code}, {evt.value})")
        return evt.code == self._code

    # fell: returns True when button is pressed
    @property
    def fell(self):
        evt = self._btn.read_evt()
        #print(f"fell evt: ({evt.code}, {evt.value})")
        if evt.code == self._code:
            status = "pressed" if evt.value == 0 else "released"
            print(f"fell {self._code} {status}: ({evt.code}, {evt.value})")
            return evt.value == 0

    # rose: returns True when button is released
    @property
    def rose(self):
        evt = self._btn.read_evt()
        #print(f"rose evt: ({evt.code}, {evt.value})")
        if evt.code == self._code:
            status = "pressed" if evt.value == 0 else "released"
            print(f"rose {self._code} {status}: ({evt.code}, {evt.value})")
            return evt.value == 1


# test
try:
    left_btn = Buttons(code=Buttons.LEFT_CODE)
    right_btn = Buttons(code=Buttons.RIGHT_CODE)
    print(f"Left button: {left_btn}")
    print(f"Right button: {right_btn}")

    print("Waiting for Input")
    while True:
        #if left_btn.code and left_btn.fell:  # left-button pressed
        if left_btn.code and left_btn.rose:  # left-button released
            print("Left")

        #if right_btn.code and right_btn.fell:   #  right-button pressed
        if right_btn.code and right_btn.rose:  #  right-button released
            print("Right")

except KeyboardInterrupt:
    print("user interrupted...")

finally:
    print('done!')
