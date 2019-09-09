import minimalmodbus
import serial
from time import sleep

import ClockFace
from AxisMoveTask import AxisMoveTask

from pprint import pprint


port = '/dev/cu.usbserial-1410'

cf_broadcast = ClockFace.ClockFace(port, 0, True)
cf = ClockFace.ClockFace(port, 12, True)

cf_broadcast.instrument.serial.baudrate = 230400
cf_broadcast.instrument.serial.timeout = 0.025

# pprint(cf.get_calibration_info())

# cf.calibrate(True, False) # Hour
# cf.calibrate(False, True) # Minute
# cf.calibrate(True, True) # Both

# cf.move(AxisMoveTask(30, 20, True))
# cf.move(None, AxisMoveTask(30, 20, True))
# cf.move(None, AxisMoveTask(-30, 20, True))
# cf.move(AxisMoveTask(30, 10, True), AxisMoveTask(-30, 10, True))
# cf.move(AxisMoveTask(-30, 10, True), AxisMoveTask(-30, 15, True))
# cf.move(AxisMoveTask(135, 10, True), AxisMoveTask(135, 15, True))

# cf.move(AxisMoveTask(10, 20, True))
# cf.sleep(500)
# cf.sleep(1500, 500)
# cf.move(AxisMoveTask(-10, 30, True))
