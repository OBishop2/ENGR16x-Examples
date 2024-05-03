# IMUSensor.py

# Created by Noah Grzegorek on behalf of the ENGR 16X Teaching Team

### DO NOT MODIFY CODE IN THIS FILE ###

# This is the code for Grove - IMU 9DOF (ICM20600+AK09918).
# (https://www.seeedstudio.com/Grove-IMU-9DOF-ICM20600-AK0991-p-3157.html)
# which is 9 Degrees of Freedom IMU (Inertial measurement unit) with
# gyroscope, accelerometer and electronic compass, implemented by
# two chips LCM20600 and AK09918.
#
# Author: Peter Yang <turmary@126.com>
#
# Grove.py is the library for Grove Base Hat which used to
# connect grove sensors for raspberry pi.
#
'''
## License

The MIT License (MIT)

Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2018  Seeed Technology Co.,Ltd. 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

### ENGR 161X STUDENTS IGNORE THIS CODE ###

from ctypes import *
from ctypes import util
import sys
from grove.i2c import Bus

ICM20600_I2C_ADDR0   = 0x68
ICM20600_I2C_ADDR1   = 0x69

ICM20600_RANGE_250_DPS, \
ICM20600_RANGE_500_DPS, \
ICM20600_RANGE_1K_DPS,  \
ICM20600_RANGE_2K_DPS   = 0, 1, 2, 3

ICM20600_RANGE_2G, \
ICM20600_RANGE_4G, \
ICM20600_RANGE_8G, \
ICM20600_RANGE_16G = 0, 1, 2, 3

ICM20600_GYRO_RATE_8K_BW_3281, \
ICM20600_GYRO_RATE_8K_BW_250,  \
ICM20600_GYRO_RATE_1K_BW_176,  \
ICM20600_GYRO_RATE_1K_BW_92,   \
ICM20600_GYRO_RATE_1K_BW_41,   \
ICM20600_GYRO_RATE_1K_BW_20,   \
ICM20600_GYRO_RATE_1K_BW_10,   \
ICM20600_GYRO_RATE_1K_BW_5     = 0, 1, 2, 3, 4, 5, 6, 7

ICM20600_ACC_RATE_4K_BW_1046,\
ICM20600_ACC_RATE_1K_BW_420, \
ICM20600_ACC_RATE_1K_BW_218, \
ICM20600_ACC_RATE_1K_BW_99,  \
ICM20600_ACC_RATE_1K_BW_44,  \
ICM20600_ACC_RATE_1K_BW_21,  \
ICM20600_ACC_RATE_1K_BW_10,  \
ICM20600_ACC_RATE_1K_BW_5    = 0, 1, 2, 3, 4, 5, 6, 7

ICM20600_ACC_AVERAGE_4, \
ICM20600_ACC_AVERAGE_8, \
ICM20600_ACC_AVERAGE_16,\
ICM20600_ACC_AVERAGE_32 = 0, 1, 2, 3

ICM20600_GYRO_AVERAGE_1,  \
ICM20600_GYRO_AVERAGE_2,  \
ICM20600_GYRO_AVERAGE_4,  \
ICM20600_GYRO_AVERAGE_8,  \
ICM20600_GYRO_AVERAGE_16, \
ICM20600_GYRO_AVERAGE_32, \
ICM20600_GYRO_AVERAGE_64, \
ICM20600_GYRO_AVERAGE_128 = 0, 1, 2, 3, 4, 5, 6, 7

ICM20600_ICM_SLEEP_MODE,     \
ICM20600_ICM_STANDYBY_MODE,  \
ICM20600_ICM_ACC_LOW_POWER,  \
ICM20600_ICM_ACC_LOW_NOISE,  \
ICM20600_ICM_GYRO_LOW_POWER, \
ICM20600_ICM_GYRO_LOW_NOISE, \
ICM20600_ICM_6AXIS_LOW_POWER,\
ICM20600_ICM_6AXIS_LOW_NOISE = 0, 1, 2, 3, 4, 5, 6, 7

__c_module = "akicm" # doesnt work

try:
    _ = util.find_library(__c_module) # doesnt work
    # print(_)
    _akicm = cdll.LoadLibrary("libakicm.so")
    # print(_akicm)
except Exception:
    print("Error: module lib{}.so unusable, please install lib{}".
          format(__c_module, __c_module))
    sys.exit(1)

class ICM20600Cfg(Structure):
    _fields_ = [("gyro_range", c_uint16), \
                ("gyro_rate",  c_uint16), \
                ("gyro_aver",  c_uint16), \
                ("acc_range",  c_uint16), \
                ("acc_rate",   c_uint16), \
                ("acc_aver",   c_uint16), \
                ("power",      c_uint16), \
                ("divider",    c_uint16)  ]

class GroveIMU9DOFICM20600(object):
    def __init__(self, addr = ICM20600_I2C_ADDR1):
        self._dev = _akicm.rpi_icm20600_alloc()
        dev_path = "/dev/i2c-{}".format(Bus().bus)
        icm20600_cfg = ICM20600Cfg(ICM20600_RANGE_2K_DPS,
                                ICM20600_GYRO_RATE_1K_BW_176,
                                ICM20600_GYRO_AVERAGE_1,
                                ICM20600_RANGE_16G,
                                ICM20600_ACC_RATE_1K_BW_420,
                                ICM20600_ACC_AVERAGE_4,
                                ICM20600_ICM_6AXIS_LOW_POWER,
				0)

        dev_path = dev_path.encode('utf-8') # SEED STUDIO SHOULD HIRE SETH MCCONKEY

        _akicm.rpi_icm20600_init(self._dev,
                             dev_path,
                             addr,
                             byref(icm20600_cfg))

    def __del__(self):
        _akicm.rpi_icm20600_free(self._dev)

    def get_temperature(self):
        t = c_double()
        _akicm.rpi_icm20600_get_temperature(self._dev, byref(t))
        return t.value

    def get_accel(self):
        x, y, z = c_double(), c_double(), c_double()
        _akicm.rpi_icm20600_get_accel(self._dev,
                                  byref(x), byref(y), byref(z))
        return x.value, y.value, z.value

    def get_gyro(self):
        x, y, z = c_double(), c_double(), c_double()
        _akicm.rpi_icm20600_get_gyro(self._dev,
                                  byref(x), byref(y), byref(z))
        return x.value, y.value, z.value

    temperature = get_temperature



AK09918_I2C_ADDR	 = 0x0C

AK09918_POWER_DOWN       = 0x00
AK09918_NORMAL           = 0x01
AK09918_CONTINUOUS_10HZ  = 0x02
AK09918_CONTINUOUS_20HZ  = 0x04
AK09918_CONTINUOUS_50HZ  = 0x06
AK09918_CONTINUOUS_100HZ = 0x08
AK09918_SELF_TEST        = 0x10

AK09918_ERR_OK               = 0 # OK
AK09918_ERR_DOR              = 1 # data skipped
AK09918_ERR_NOT_RDY          = 2 # not ready
AK09918_ERR_TIMEOUT          = 3 # read/write timeout
AK09918_ERR_SELFTEST_FAILED  = 4 # self test failed
AK09918_ERR_OVERFLOW         = 5 # sensor overflow, means |x|+|y|+|z| >= 4912uT
AK09918_ERR_WRITE_FAILED     = 6 # fail to write
AK09918_ERR_READ_FAILED      = 7 # fail to read

class GroveIMU9DOFAK09918(object):
    def __init__(self, addr = AK09918_I2C_ADDR):
        self._dev = _akicm.rpi_ak09918_alloc()
        dev_path = "/dev/i2c-{}".format(Bus().bus)

        dev_path = dev_path.encode('utf-8') # SEED STUDIO SHOULD HIRE SETH MCCONKEY

        _akicm.rpi_ak09918_init(self._dev,
                             dev_path,
                             addr,
                             AK09918_NORMAL)

    def __del__(self):
        _akicm.rpi_ak09918_free(self._dev)

    def mode(self, mode = None):
        if not mode is None:
            _akicm.rpi_ak09918_set_mode(self._dev, mode)
        return _akicm.rpi_ak09918_get_mode(self._dev)

    def reset(self):
        return _akicm.rpi_ak09918_reset(self._dev)

    def is_ready(self):
        if _akicm.rpi_ak09918_is_ready(self._dev) == AK09918_ERR_OK:
            return True
        return False

    def is_skip(self):
        r = _akicm.rpi_ak09918_is_skip(self._dev)
        return (r == AK09918_ERR_DOR)

    def get_magnet(self):
        x, y, z = c_double(), c_double(), c_double()
        _akicm.rpi_ak09918_read(self._dev,
                                  byref(x), byref(y), byref(z))
        return x.value, y.value, z.value

    def get_magnet_raw(self):
        x, y, z = c_double(), c_double(), c_double()
        _akicm.rpi_ak09918_read_raw(self._dev,
                                  byref(x), byref(y), byref(z))
        return x.value, y.value, z.value

    def err_string(self, errval):
        return _akicm.rpi_ak09918_err_string(errval)

### END OF CODE TO IGNORE FOR 161X STUDENTS ###


### IMPORTANT CODE FOR ENGR 161X STUDENTS ###

# Class combining all sensor functionality into one class for ease of use
class IMUSensor(object):

    # This sensor utilizes two different chips and they are initialized here so all functions can be called easily
    def __init__(self):
        self.icmChip = GroveIMU9DOFICM20600()
        self.akChip = GroveIMU9DOFAK09918()
        self.akChip.mode(AK09918_CONTINUOUS_100HZ)

    # Function returns a three dimensional vector of the respective x, y, and z acceleration values (M/S^2)
    def getAccel(self):
        return (tuple(x / 100 for x in self.icmChip.get_accel()))
    
    # Function returns a three dimensional vector of the respective x, y, and z gyroscope values (Degrees/Second)
    def getGyro(self):
        return self.icmChip.get_gyro()

    # Function returns a three dimensional vector of the respective x, y, and z magnetic values (Micro-Teslas)
    def getMag(self):
        return self.akChip.get_magnet()