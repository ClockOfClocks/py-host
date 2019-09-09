import minimalmodbus
import AxisMoveTask
from typing import Optional


class ClockFace:
    MOVE_HOUR = 1
    MOVE_MINUTE = 2
    MOVE_HOUR_RELATIVE = 4
    MOVE_MINUTE_RELATIVE = 8

    CALIBRATE_HOUR = 1
    CALIBRATE_MINUTE = 2

    SLEEP_HOUR = 4
    SLEEP_MINUTE = 8

    def __init__(
            self,
            port,
            slave_address,
            debug=False
    ):
        self.instrument = minimalmodbus.Instrument(port, slave_address)
        self.instrument.debug = debug
        self.debug = debug

    def get_calibration_info(self):
        info = self.instrument.read_register(1)

        return info & 0xFF > 0, info & 0xFF00 > 0

    def calibrate(self, hour_hand: bool, minute_hand: bool):

        if self.debug:
            print('calibrate', ' hour' if hour_hand else '', ' minute' if minute_hand else '', )

        if hour_hand is False and minute_hand is False:
            raise TypeError('One of the hands must be marked to calibrate')

        register_address = 0

        if hour_hand:
            register_address |= self.CALIBRATE_HOUR

        if minute_hand:
            register_address |= self.CALIBRATE_MINUTE

        self.instrument.write_register(register_address, 1, 0, 6)

    def sleep(self, hour_hand_sleep: Optional[int] = None, minute_hand_sleep: Optional[int] = None):

        # if self.debug:
        #     print('Sleep ', ' hour ' if hour_hand_sleep else '', ' minute' if minute_hand_sleep else '', )

        if hour_hand_sleep is None and minute_hand_sleep is None:
            raise TypeError('One of the hands must be marked to sleep')

        register_address = 0
        values = []

        if hour_hand_sleep is not None:
            register_address |= self.SLEEP_HOUR
            values.append(hour_hand_sleep)

        if minute_hand_sleep is not None:
            register_address |= self.SLEEP_MINUTE
            values.append(minute_hand_sleep)

        if len(values) == 1:
            self.instrument.write_register(register_address, values[0])

        self.instrument.write_registers(register_address, values)

    def move(self, hour_hand_task: AxisMoveTask = None, minute_hand_task: AxisMoveTask = None) -> None:

        if hour_hand_task is None and minute_hand_task is None:
            raise TypeError('One of the tasks must be defined')

        register_address = 0
        values = []

        if hour_hand_task is not None:
            register_address |= self.MOVE_HOUR

            values.append(self._convert_float_to_int_for_payload(hour_hand_task.degree))
            values.append(self._convert_float_to_int_for_payload(hour_hand_task.speed))

            if hour_hand_task.relative:
                register_address |= self.MOVE_HOUR_RELATIVE

        if minute_hand_task is not None:
            register_address |= self.MOVE_MINUTE

            values.append(self._convert_float_to_int_for_payload(minute_hand_task.degree))
            values.append(self._convert_float_to_int_for_payload(minute_hand_task.speed))

            if minute_hand_task.relative:
                register_address |= self.MOVE_MINUTE_RELATIVE

        self.instrument.write_registers(register_address, values)

    @staticmethod
    def _convert_float_to_int_for_payload(value: float) -> int:
        return minimalmodbus._twos_complement(int(round(value * 10)))
