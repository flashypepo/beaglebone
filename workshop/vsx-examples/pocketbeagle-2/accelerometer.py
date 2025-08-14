# 2025-0812 PP class Accelerometer
# ================================
from time import sleep
from sysfs import Device


class Accelerometer():
    DEV_NAME = "mma8453"

    def __init__(self, device=DEV_NAME):
        accel = Device(name=device)
        self._scale = accel.sysfs("in_accel_scale").read_float()
        print(f"scale: {self._scale}")  # DEBUG
        self._x_raw = accel.sysfs("in_accel_x_raw")
        self._y_raw = accel.sysfs("in_accel_y_raw")
        self._z_raw = accel.sysfs("in_accel_z_raw")

    @property
    def x(self):
        #print(f"x_raw: {self._x_raw.read_float()}")  # DEBUG
        return self._x_raw.read_float() * self._scale

    @property
    def y(self):
        #print(f"y_raw: {self._y_raw.read_float()}")  # DEBUG
        return self._y_raw.read_float() * self._scale

    @property
    def z(self):
        #print(f"z_raw: {self._z_raw.read_float()}")  # DEBUG
        return self._z_raw.read_float() * self._scale


    @property
    def acceleration(self):
        #return (self.x, self.y, self.z)  # as tuple
        return {'x': self.x, 'y': self.y, 'z':self.z}  # as dictionary


# test
if __name__ == "__main__":
    try:
        imu = Accelerometer()  # default arguments for TechCape
        #imu = Accelerometer(device=Accelerometer.DEV_NAME)  # when another cape is used ???
        while True:
            accel = imu.acceleration  # get acceleration in direction x, y, z (either a tuple or dictionary)
            #DEBUG: print(f"accel = {accel}")
            print(
                #f"Acceleration along X = {accel[0]:.2f} ms^2, Y = {accel[1]:.2f} ms^2, Z = {accel[2]:.2f} ms^2"  # when returned as tuple
                f"Acceleration along X = {accel['x']:.2f} ms^2, Y = {accel['y']:.2f} ms^2, Z = {accel['z']:.2f} ms^2"
            )
            sleep(1)

    except Exception as ex:
        print(f"EXCEPTION: {ex}")

    except KeyboardInterrupt:
        print("interrupted by user...")

    finally:
        print('done!')
