from __future__ import division
from __future__ import print_function

# UltrasonicSensor.py

# Created by Noah Grzegorek on behalf of the ENGR 16X Teaching Team

### DO NOT MODIFY CODE IN THIS FILE ###

# This is the code for Grove - Ultrasonic Ranger
# (https://www.seeedstudio.com/Grove-Ultrasonic-Ranger-p-960.html)
# which is a non-contact distance measurement module which works with 40KHz sound wave. 
#
# This is the library for Grove Base Hat which used to connect grove sensors for raspberry pi.
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

import sys
import time
from grove.gpio import GPIO

# This usleep is to have used to have the sensor sleep for a certain amount of microseconds
usleep = lambda x: time.sleep(x / 1000000.0)

# These global variables are used as part of the distance calculations the sensor performs
_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

class UltrasonicSensor(object):
    def __init__(self, pin):
        self.dio = GPIO(pin)

    # This function calculates the distance that the nearest object it can detect is from the sensor in centimeters
    @property
    def getDist(self):
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)

        self.dio.dir(GPIO.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None

        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None

        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm

        return distance

# LineFinder.py

# Created by Noah Grzegorek on behalf of the ENGR 16X Teaching Team

### DO NOT MODIFY CODE IN THIS FILE ###

from gpiozero import SmoothedInputDevice

class LineFinder(SmoothedInputDevice):
    """
    Extends :class:`SmoothedInputDevice` and represents a single pin line
    sensor like the TCRT5000 infra-red proximity sensor found in the `CamJam #3
    EduKit`_.

    A typical line sensor has a small circuit board with three pins: VCC, GND,
    and OUT. VCC should be connected to a 3V3 pin, GND to one of the ground
    pins, and finally OUT to the GPIO specified as the value of the *pin*
    parameter in the constructor.

    The following code will print a line of text indicating when the sensor
    detects a line, or stops detecting a line::

        from gpiozero import LineSensor
        from signal import pause

        sensor = LineSensor(4)
        sensor.when_line = lambda: print('Line detected')
        sensor.when_no_line = lambda: print('No line detected')
        pause()

    :type pin: int or str
    :param pin:
        The GPIO pin which the sensor is connected to. See :ref:`pin-numbering`
        for valid pin numbers. If this is :data:`None` a :exc:`GPIODeviceError`
        will be raised.

    :type pull_up: bool or None
    :param pull_up:
        See description under :class:`InputDevice` for more information.

    :type active_state: bool or None
    :param active_state:
        See description under :class:`InputDevice` for more information.

    :param int queue_len:
        The length of the queue used to store values read from the sensor. This
        defaults to 5.

    :param float sample_rate:
        The number of values to read from the device (and append to the
        internal queue) per second. Defaults to 100.

    :param float threshold:
        Defaults to 0.5. When the average of all values in the internal queue
        rises above this value, the sensor will be considered "active" by the
        :attr:`~SmoothedInputDevice.is_active` property, and all appropriate
        events will be fired.

    :param bool partial:
        When :data:`False` (the default), the object will not return a value
        for :attr:`~SmoothedInputDevice.is_active` until the internal queue has
        filled with values.  Only set this to :data:`True` if you require
        values immediately after object construction.

    :type pin_factory: Factory or None
    :param pin_factory:
        See :doc:`api_pins` for more information (this is an advanced feature
        which most users can ignore).

    .. _CamJam #3 EduKit: http://camjam.me/?page_id=1035
    """
    def __init__(self, pin=None, *, pull_up=False, active_state=None,
                 queue_len=1, sample_rate=100, threshold=0.5, partial=False,
                 pin_factory=None):
        super().__init__(
            pin, pull_up=pull_up, active_state=active_state,
            threshold=threshold, queue_len=queue_len,
            sample_wait=1 / sample_rate, partial=partial,
            pin_factory=pin_factory)
        self._queue.start()


    # Gets the current reading whether there it detects black or white (0 or 1)
    @property
    def value(self):
        """
        Returns a value representing the average of the queued values. This
        is 0 for black under the sensor, and 1 for white under
        the sensor.
        """
        return super().value

    @property
    def line_detected(self):
        return not self.is_active

# LightSensor.py

# Created by Noah Grzegorek on behalf of the ENGR 16X Teaching Team

### DO NOT MODIFY CODE IN THIS FILE ###

# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
# Copyright (C) 2018  Seeed Technology Co.,Ltd.
'''
This is the code for
    - `Grove - Light Sensor <https://www.seeedstudio.com/Grove-Light-Sensor-v1.2-p-2727.html>`_

Examples:

    .. code-block:: python

        import time
        from grove.grove_light_sensor import GroveLightSensor

        # connect to alalog pin 2(slot A2)
        PIN = 2

        sensor = GroveLightSensor(pin)

        print('Detecting light...')
        while True:
            print('Light value: {0}'.format(sensor.light))
            time.sleep(1)
'''
import time, sys, math
from grove.adc import ADC

class LightSensor(object):
    '''
    Grove Light Sensor class

    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC(address = 0x08)

    # Gets the current light strength percentage (0% or 100%)
    @property
    def light(self):
        '''
        Get the light strength value, maximum value is 100.0%

        Returns:
            (int): ratio, 0(0.0%) - 1000(100.0%)
        '''
        value = self.adc.read(self.channel)
        return value

# IRSensor.py

# Created by Seth McConkey on behalf of the ENGR 16X Teaching Team

### DO NOT MODIFY CODE IN THIS FILE ###

'''
IR Sensor:
    Description:
        This sensor has two values that can be accessed: a value from 0 to 999 that is 
        proportional to the amount of infrared rays the left sensor is reading, and a value 
        from 0 to 999 that is proportional to the amount of infrared rays the left sensor is 
        reading. It is used to determine presence/distance of an infrared source, such as an 
        LED light or Infrared Beacon.

    Hardware:
        Connect this sensor to any analog port on the Grove BaseHAT: A0, A2, A4, or A6.
        Initialize the sensor using only the number of the port, DO NOT include the A.
        
        More info:
        https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi/
        https://wiki.seeedstudio.com/Grove-Infrared_Reflective_Sensor/


    Initialization:

        sensor_name = IRSensor(pin, pin + 1)

        If you plug your IR Sensor into A0 and want to name it 'IR', your initialization will
        look like this:

        IR = IRSensor(0, 1)
    
    IRSensor.value1:
        Read the value from the sensor labeled sensor1. If your sensor's name is 'IR', accessing the left
        value will look like this:

        value_from_sensor1 = IR.value1

    IRSensor.value2:
        Read the value from the sensor labeled sensor2. If your sensor's name is 'IR', accessing the right
        value will look like this:

        value_from_sensor2 = IR.value2
    
    IRSensor_Example.py: 
        Usage of this code is demonstrated in the example file for this sensor in the Examples
        folder on your Pi's desktop.
'''

### DO NOT MODIFY CODE BELOW THIS LINE ###

# original code for comparison:
# adapted from light sensor code:
# https://github.com/Seeed-Studio/grove.py/blob/master/grove/grove_light_sensor_v1_2.py

from grove.adc import ADC

class IRSensor(object):
    '''
    IR Sensor class

    Args:
        pin(int): number of the analog pin the sensor is connected to.
    '''
    def __init__(self, channel1, channel2):
        self.channel1 = channel1
        self.channel2 = channel2
        self.adc = ADC(address = 0x08)

    @property
    def value1(self):
        '''
        Get the infrared strength value, maximum value is 999

        Returns:
            (int): ratio, 0 - 999
        '''
        value = self.adc.read(self.channel1)
        return value

    @property
    def value2(self):
        '''
        Get the infrared strength value, maximum value is 999

        Returns:
            (int): ratio, 0 - 999
        '''
        value = self.adc.read(self.channel2)
        return value

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
        icm20600_cfg = ICM20600Cfg(ICM20600_RANGE_500_DPS,
                                ICM20600_GYRO_RATE_1K_BW_92,
                                ICM20600_GYRO_AVERAGE_1,
                                ICM20600_RANGE_8G,
                                ICM20600_ACC_RATE_1K_BW_218,
                                ICM20600_ACC_AVERAGE_4,
                                ICM20600_ICM_6AXIS_LOW_NOISE,
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

    # Function returns a three dimensional vector of the respective x, y, and z acceleration values (Mega-Goombas)
    def getAccel(self):
        return (tuple(x / 100 for x in self.icmChip.get_accel()))
    
    # Function returns a three dimensional vector of the respective x, y, and z gyroscope values (Degrees/Second)
    def getGyro(self):
        return self.icmChip.get_gyro()

    # Function returns a three dimensional vector of the respective x, y, and z magnetic values (Micro-Teslas)
    def getMag(self):
        return self.akChip.get_magnet()


# for Button, follow this code:
# https://github.com/Seeed-Studio/grove.py/blob/master/grove/grove_button.py

# For most of these, you will simply just need to rename the class to make the name simpler.
# You may change property namees/functions to be more consistent or easier to remember, but 
# that is not 100% necessary all the time.
# If you are confused on how the class works, consider changing it to be more intuitive
# so it is also easier for students

# Created by Aayush Iyengar on behalf on the ENGR 16X Teaching Team
from gpiozero import DigitalInputDevice
from gpiozero import HoldMixin

class Button(HoldMixin, DigitalInputDevice):
    """
    Extends :class:`DigitalInputDevice` and represents a simple push button
    or switch.

    Connect one side of the button to a ground pin, and the other to any GPIO
    pin. Alternatively, connect one side of the button to the 3V3 pin, and the
    other to any GPIO pin, then set *pull_up* to :data:`False` in the
    :class:`Button` constructor.

    The following example will print a line of text when the button is pushed::

        from gpiozero import Button

        button = Button(4)
        button.wait_for_press()
        print("The button was pressed!")

    :type pin: int or str
    :param pin:
        The GPIO pin which the button is connected to. See :ref:`pin-numbering`
        for valid pin numbers. If this is :data:`None` a :exc:`GPIODeviceError`
        will be raised.

    :type pull_up: bool or None
    :param pull_up:
        If :data:`True` (the default), the GPIO pin will be pulled high by
        default.  In this case, connect the other side of the button to ground.
        If :data:`False`, the GPIO pin will be pulled low by default. In this
        case, connect the other side of the button to 3V3. If :data:`None`, the
        pin will be floating, so it must be externally pulled up or down and
        the ``active_state`` parameter must be set accordingly.

    :type active_state: bool or None
    :param active_state:
        See description under :class:`InputDevice` for more information.

    :type bounce_time: float or None
    :param bounce_time:
        If :data:`None` (the default), no software bounce compensation will be
        performed. Otherwise, this is the length of time (in seconds) that the
        component will ignore changes in state after an initial change.

    :param float hold_time:
        The length of time (in seconds) to wait after the button is pushed,
        until executing the :attr:`when_held` handler. Defaults to ``1``.

    :param bool hold_repeat:
        If :data:`True`, the :attr:`when_held` handler will be repeatedly
        executed as long as the device remains active, every *hold_time*
        seconds. If :data:`False` (the default) the :attr:`when_held` handler
        will be only be executed once per hold.

    :type pin_factory: Factory or None
    :param pin_factory:
        See :doc:`api_pins` for more information (this is an advanced feature
        which most users can ignore).
    """
    def __init__(self, pin=None, *, pull_up=False, active_state=None,
                 bounce_time=None, hold_time=1, hold_repeat=False,
                 pin_factory=None):
        super().__init__(
            pin, pull_up=pull_up, active_state=active_state,
            bounce_time=bounce_time, pin_factory=pin_factory)
        self.hold_time = hold_time
        self.hold_repeat = hold_repeat

    @property
    def value(self):
        """
        Returns 1 if the button is currently pressed, and 0 if it is not.
        """
        return super().value



Button.is_pressed = Button.is_active
Button.pressed_time = Button.active_time
Button.when_pressed = Button.when_activated
Button.when_released = Button.when_deactivated
Button.wait_for_press = Button.wait_for_active
Button.wait_for_release = Button.wait_for_inactive

'''
def run_button_example():
    #Main function to run the button example
    pin = 5  #Assuming pin 5 for the Grove Button

    button = GroveButton(pin)  #Create a GroveButton instance

    def on_press(elapsed_time):
        #Callback function for button press event
        print('Button is pressed')

    def on_release(elapsed_time):
        #Callback function for button release event
        print("Button is released, pressed for {0} seconds".format(round(elapsed_time, 6)))

    #Assign the callback functions to the button instance
    button.set_on_press_callback(on_press)
    button.set_on_release_callback(on_release)

    #Main loop to continuously check button state
    while True:
        time.sleep(1)

#Run the example when this script is executed
if __name__ == '__main__':
    run_button_example()
'''

'''
Hall Sensor:
    Description:
        This sensor has only one value that can be accessed: a digital value of either 0 or 1 that is 
        dependent on the strength of magnetic field present at the sensor. The sensor outputs a 1 when 
        a strong magnetic field is detected

    Hardware:
        The hall sensor connects to digital pins on the Grove BaseHAT (any port starting with a D)
        Initialize the sensor using only the number of the port (do not include the D)
        
        More info:
        https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi/
        https://wiki.seeedstudio.com/Grove-Hall_Sensor/


    Initialization:

        sensor_name = HallSensor(pin)

        If you plug your Hall Sensor into D5 and want to name it 'Hall', your initialization will
        look like this:

        Hall = HallSensor(5)
    
    HallSensor.value:
        Read the value from the sensor. If your sensor's name is 'Hall', accessing the value will
        look like this:

        value_from_sensor = Hall.value
        
    
    HallSensor_Example.py: 
        Usage of this code is demonstrated in the example file for this sensor in the Examples
        folder on your Pi's desktop.
        
'''
### DO NOT MODIFY CODE BELOW THIS LINE ###

from gpiozero import DigitalInputDevice
from gpiozero import HoldMixin

class HallSensor(HoldMixin, DigitalInputDevice):
    """
    Simple Hall Sensor Class

    Args:
        pin(int): the digital pin to which the sensor is assigned
        pull_up(bool): whether the sensor is set to pull up or down. This impacts whether the 
            sensor returns a 0 or 1 when near a magnet and must be set to false for the wiring 
            setup of the base hat.
        bounce_time(float): The length of time (in seconds) after the button is presse during which 
            new inputs are ignored. This minimizeds 'bouncy' signals, where the output of the button
            changes rapidly as it is being pressed. The base time for this is 1 second.
   
    """
    def __init__(self, pin=None, *, pull_up=True, active_state=None,
                 bounce_time=None, pin_factory=None):
        super().__init__(
            pin, pull_up=pull_up, active_state=active_state,
            bounce_time=bounce_time, pin_factory=pin_factory)

    @property
    def value(self):
        """
        Returns 1 if the button is currently pressed, and 0 if it is not.
        """
        return super().value

