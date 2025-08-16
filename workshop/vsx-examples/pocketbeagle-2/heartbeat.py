# 2025-0816 add clear_led(), clear_leds()
# 2025-0814 rewrote heartbeat to use class USRLED
# 2025-0718 program activated when user logins (~/.profile)
import time
from usrled import USRLED


# helper: setup a USR-LED for a specific trigger
def setup_led(n, trigger="none"):
    # USER-LED number PocketBeagle-2 : (1, 2, 3, 4)
    assert n in range(1,5), f"illegal USR-LED number '{n}'"
    assert trigger in USRLED.TRIGGERS, f"Illegal trigger '{trigger}'"
    led = USRLED(n)
    # DEBUG: print(led)
    led.trigger = trigger
    if trigger == "none":
        led.off()  # LED OFF
    # DEBUG: print(f"USR-LED {n} has trigger {trigger}")


# helper: clears a USR-LED
def clear_led(n):
    assert n in range(1,5), f"illegal USR-LED number '{n}'"
    setup_led(n=n, trigger='none')


# helper: clears all USR-LEDs
def clear_leds():
    for i in range(1, 5):
        clear_led(n)


# execute
if __name__ == "__main__":
    try:
        clear_led(1)   # setup_led(n=1, trigger="none")
        clear_led(3)   # setup_led(n=3, trigger="none")

        time.sleep(5)  # wait for possible user Ctrl-C

        setup_led(n=1, trigger="heartbeat")
        setup_led(n=3, trigger="usb-host")

    except KeyboardInterrupt:
        # clear LEDS
        clear_led(1)
        clear_led(3)

    finally:
        print('done!')

