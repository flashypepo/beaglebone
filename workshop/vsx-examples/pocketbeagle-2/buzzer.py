"""
class Buzzer - to play a melody

Note: blocking - uses time.sleep()

2025-0816 PP new
"""
import asyncio
import time
from chardev import CharDev, InputKey
# melody
import melody

class Buzzer():
    OFF_NOTE = InputKey.with_freq(0)
    #?? TECHLAB_BUZZER_NAME = "pwm-beeper"

    def __init__(self):
        self._buzzer = CharDev.input_device_by_name("pwm-beeper")


    # melody must contain MELODY and WHOLE_NOTE
    #def play(self, melody):
    async def play(self, melody):
        try:
            print("Start Playing...")
            for t, d in melody.MELODY:
                note = InputKey.with_freq(int(t.freq)) if t else self.OFF_NOTE

                note_dur = melody.WHOLE_NOTE / abs(d)
                if d < 0:
                    note_dur *= 1.5

                self._buzzer.write_evt(note)
                #time.sleep(note_dur * 0.9 / 1000)
                await asyncio.sleep(note_dur * 0.9 / 1000)

                self._buzzer.write_evt(self.OFF_NOTE)
                await asyncio.sleep(note_dur * 0.1 / 1000)

        except KeyboardInterrupt:
            print("user interrupted...")
            self._buzzer.write_evt(self.OFF_NOTE)

        finally:
            print('done!')



if __name__ == "__main__":
    import melody

    buzzer = Buzzer()
    buzzer.play(melody)
