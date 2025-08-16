"""
techlabcape.py - demo of several devices on the TechLab cape using asyncio
(integrateis varies sample code)

2025-0814 PP new
"""
import time
import asyncio

from usrled import USRLED
from heartbeat import setup_led

# ============================================
#                  Tasks
# ============================================
# task for a USR-LED
async def usrled_task(lednr, trigger, delay=5, cycles=20):
    print(f"{time.strftime('%X')} - USR LED: led-nr={lednr}, trigger={trigger} started...")
    setup_led(n=lednr, trigger=trigger)
    count = 0
    while count < cycles:
        await asyncio.sleep(delay)
        count += 1
    # task is done
    setup_led(n=lednr, trigger="none")
    print(f"task USR-LED '{lednr}' done at {time.strftime('%X')}")


# task to blink a URS-LED
async def blinky_task(lednr, delay=2, cycles=5):
    print(f"{time.strftime('%X')} - USR LED: led-nr={lednr} start to blink...")
    led = USRLED(lednr)
    count = 0
    while count < cycles:   # True
        led.on()
        await asyncio.sleep(delay)
        led.off()
        await asyncio.sleep(delay)
        count += 1
    print(f"task blink USR-LED '{lednr}' done at {time.strftime('%X')}")


# task for the RGB-LED
from rgbled import RGBLed
#async def rgbleddemo(mode, delay=0.01, cycles=5):
async def rgbled_hue(delay=0.01, cycles=5):
    print(f"{time.strftime('%X')} - RGB-Led demo 'hue' started...")

    rgbled = RGBLed()
    # Set brightness to max from the start
    rgbled.brightness = 1
    #rgbled.brightness = 0.5  # factor to reduce the brightness
    # factor < 0.5 -> green is not visible, blue hardly, red okay.
    print(f"brightness: {rgbled.brightness}")

    print("cycle:", end=' ', flush=True)
    count = 0
    while count < cycles:
        print(f"{count}", end=', ', flush=True)
        for i in range(0, 256):
            val = ' '.join(map(str, rgbled.wheel(i)))
            #DEBUG: print(f"{val}", end=', ', flush=True)
            rgbled.intensity = val
        await asyncio.sleep(delay)
        count += 1
    print()
    rgbled.intensity = '0 0 0'  # RGBLed OFF
    print(f"RGB-LED demo 'hue' done at {time.strftime('%X')}")


# task for Seven-Segment display
async def seven_segmentdemo(mode=0, delay=1, cycles=5):
    print(f"{time.strftime('%X')} - Seven Segment demo '{mode}' started...")
    count = 0
    while count < cycles:   #True:
         #print(f"{time.strftime("%X")} - update {count+1} of seven-segment...")
         count += 1
         await asyncio.sleep(delay)
    print(f"Seven-segment demo '{mode}' done at {time.strftime('%X')}")


# task for accelerometer
from accelerometer import Accelerometer

async def accelerometerdemo(delay=1, cycles=15):
    print(f"{time.strftime('%X')} - demo accelerometer started every {delay} seconds...")
    imu = Accelerometer()  # default arguments for TechCape
    count = 0
    while count < cycles:   #True:
        accel = imu.acceleration  # get acceleration in direction x, y, z (either a tuple or dictionary)
        #DEBUG: print(f"accel = {accel}")
        print(
            #f"{time.strftime("%X")} Acceleration along X = {accel[0]:.2f} ms^2, Y = {accel[1]:.2f} ms^2, Z = {accel[2]:.2f} m^2"  # when returned as tuple
            f"{time.strftime("%X")} Acceleration along X = {accel['x']:.2f} ms^2, Y = {accel['y']:.2f} ms^2, Z = {accel['z']:2f} ms^2"
        )
        count += 1
        await asyncio.sleep(delay)
    # task finished
    print(f"Accelerometer demo done at {time.strftime('%X')}")


# task for lightmeter
from light_sensor import LightSensor

async def lightsensordemo(delay=1, cycles=5):
    print(f"{time.strftime('%X')} - demo lightsensor started every {delay} second...")
    lightsensor = LightSensor()
    print(f"\tLight/Dark threshold: {lightsensor.threshold}")

    count = 0
    while count < cycles:  #True:
        scaled = lightsensor.raw * lightsensor.scale
        print(f"{time.strftime('%X')} LightSensor - scaled voltage: {scaled:4.0f}", end='... ')
        now = "Light" if scaled > lightsensor.threshold else "Dark"
        print(now)
        count += 1
        await asyncio.sleep(delay)
    # task is finished
    print(f"Lightsensor demo done at {time.strftime('%X')}")


# task for buzzer
from chardev import CharDev, InputKey
from buzzer import Buzzer
#import melody

async def buzzer_task(melody, delay=1, cycle=1):
    print(f"{time.strftime('%X')} - buzzer started...")
    buzzer = Buzzer()
    #count = 0
    #while count < cycles:  #True:
    #     count += 1
    #     await asyncio.sleep(delay)
    await buzzer.play(melody)
    # task finished
    print(f"Buzzer task done at {time.strftime('%X')}")




async def main():
    import melody

    # rgbled_mode:  0: hue 1:cycle_color, 2:fade intensity,  3:fade brightness
    rgbled_mode = 0

    # usr_led_mode:  0: none 1:heartbeat, 2:usb-host, 3:heartbeat + usb-host
    triggers = {
        0: USRLED.TRIGGERS[0],   #none
        1: USRLED.TRIGGERS[1],   #usb-host
        2: USRLED.TRIGGERS[2],   #heartbeat
    }
    usrled_mode = 1
    # create tasks...
    task_accelerometer = asyncio.create_task(accelerometerdemo(delay=3))
    task_lightsensor = asyncio.create_task(lightsensordemo(delay=2, cycles=10))
    task_seven_segment = asyncio.create_task(seven_segmentdemo(delay=2))
    #TODO: task_rgbled = asyncio.create_task(rgbled_hue())
    task_heartbeat = asyncio.create_task(usrled_task(lednr=1, trigger=triggers[2], cycles=10))
    task_usbhost   = asyncio.create_task(usrled_task(lednr=3, trigger=triggers[1], cycles=5))
    task_blinky    = asyncio.create_task(blinky_task(lednr=4))
    task_buzzer    = asyncio.create_task(buzzer_task(melody))

    # start tasks...
    print("Start:", time.strftime("%X"))
    result = await asyncio.gather(
        task_accelerometer,
        task_lightsensor,
        task_seven_segment,
        #TODO: task_rgbled,
        task_heartbeat,
        task_usbhost,
        task_blinky,
        task_buzzer,
    )

    # all tasks are finished
    print("End:", time.strftime("%X"), end=" - ")
    #print(f"All tasks done: {all((task_accelerometer.done(), task_lightsensor.done()))}")
    done_tasks = all((
        task_accelerometer.done(),
        task_lightsensor.done(),
        task_seven_segment.done,
        #TODO: task_rgbled.done,
        task_heartbeat.done,
        task_usbhost.done,
        task_blinky.done,
        task_buzzer.done,
    ))
    print(f"All tasks done: {done_tasks}")
    return result


if __name__ == "__main__":
    print("Techlab cape demonstration...")
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print ("user interrupted...")

    finally:
        print('bye!')
