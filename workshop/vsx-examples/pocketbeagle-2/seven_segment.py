# 2025-0805 PP solved bug: self._msg is an object and needs to call write(message)
# 2025-0804 PP bug: segments do not clear!
from time import sleep
from sysfs import Device
from pathlib import Path

# TECHLAB_SEVEN_SEGMENT_LEFT = Path("/sys/devices/platform/seven-segments-left/linedisp.1/")
# TECHLAB_SEVEN_SEGMENT_RIGHT = Path("/sys/devices/platform/seven-segments-right/linedisp.0/")

class SevenSegment():
    LEFT = "left"    # SEGMENT_LEFT
    RIGHT = "right"  # SEGMENT_RIGTH
    DEFAULT_SCROLL_SPEED = 1000    # default scroll-speed in ms

    def __init__(self, segment_part):
        assert segment_part in [self.LEFT, self.RIGHT], f"Wrong segment-part ('{segment_part}'), must be 'left' or 'right'"

        if segment_part == "left":
             TECHLAB_SEVEN_SEGMENT = Path("/sys/devices/platform/seven-segments-left/linedisp.1/")
        elif segment_part == "right":
             TECHLAB_SEVEN_SEGMENT = Path("/sys/devices/platform/seven-segments-right/linedisp.0/")
        else:
            print(f"{segment_part} should not happen!")
            raise Exception(f"invalid argument {segment_part}")

        self._name = segment_part  # save name of segment (left or right)
        self._segment = Device(path=TECHLAB_SEVEN_SEGMENT)
        self._msg  = self._segment.sysfs('message')
        self._scrollspeed = self._segment.sysfs('scroll_step_ms')
        self.init()

    def init(self):
        self._scrollspeed.write(self.DEFAULT_SCROLL_SPEED)  # set default scroll speed
        self._msg.write(' ')  # clear segment

    def write(self, message):
        self._msg.write(message)

    def clear(self):
        self.write(' ')       # clear segment
        self.scrollspeed = 0  # stop scrolling

    @property
    def scrollspeed(self):
        return self._scrollspeed.read_int()  # scroll speed in ms

    @scrollspeed.setter
    def scrollspeed(self, value):  # value in ms
        #DEBUG: print(dir(self))
        print(f"{self._name}: new scroll speed value '{value}'")  # debug
        assert value >= 0, f"segment '{self._name}' scroll speed value must be >= 0"
        self._scrollspeed.write(value)

    @property
    def segmentpart(self):
        return self._name




# test/sample
if __name__ == "__main__":

    # create left and right SevenSegment
    left = SevenSegment(SevenSegment.LEFT)
    right = SevenSegment(SevenSegment.RIGHT)
    print(f"{left.segmentpart}: scroll speed '{left.scrollspeed}'")
    print(f"{right.segmentpart}: scroll speed '{right.scrollspeed}'")

    clear_segments = True  # clears segments in nominal situations

    try:
        print("Countdown")
        # user defined scroll speed in ms
        left.scrollspeed = 500  # quicker
        right.scrollspeed = 500

        left.write('10000000000')
        right.write('09876543210')

        sleep(11)

    except AssertionError as ae:
        print(f"AssertionError: {ae}")

    except KeyboardInterrupt:
        print("user interrupt...")
        clear_segments = False

    finally:
        if clear_segments:
            print("clear segments...")
            left.clear()
            right.clear()
        print('done!')
