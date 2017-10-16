from collections import namedtuple
from math import copysign
import cwiid
import time

import board
import wiimote


def speed_calculator(x0, x1, x2, y0, y1, y2):
    """Function is a ramp between x0 and x1, then continuous plateau between x1 and x2.
    Ramp goes from y1 to y2, plateau at y2.
    Else is y0.
    """
    a = (y2 - y1) * 1. / (x1 - x0)
    b = y2 - a * x1

    def _angle_to_speed(x):
        if x1 <= x <= x2:
            return y2
        elif x0 < x < x1:
            return a * x + b
        else:
            return y0
    return _angle_to_speed


max_motor_voltage = 6  # [V]
max_battery_output = 8.5  # [V]
max_pwm = int(100 * max_motor_voltage / max_battery_output)

acc_to_speed = speed_calculator(
    97,
    117,
    125,
    0,
    20,
    max_pwm
)
acc_to_rotation_left = speed_calculator(
    100,
    120,
    160,
    0,
    -1,
    1
)
acc_to_rotation_right = speed_calculator(
    -151,
    -130,
    -100,
    0,
    -1,
    1
)


class Controller(object):

    def __init__(self, refresh_pwm=0.05, refresh_trigger=10):
        self.pwm = board.L298N()
        self.trigger = board.Button(True)
        self.wiimote = wiimote.WiimoteController()
        self.is_setup = False
        self.refresh_pwm = refresh_pwm
        self.refresh_trigger = refresh_trigger

    def setup(self):
        if self.is_setup:
            return
        if not self.wiimote.is_connected:
            if not self.wiimote.connect(exit_if_fail=False):
                return
        self.pwm.setup()
        self.is_setup = True

    def cleanup(self):
        if not self.is_setup:
            return
        self.pwm.cleanup(all_board=False)
        self.wiimote.cleanup()
        self.is_setup = False

    def control_for(self, nb_iterations):
        btn_a_pressed = False
        for _ in range(nb_iterations):
            if self.wiimote.is_btn_a_pressed():
                btn_a_pressed = True
                acc_x, acc_y, acc_z = self.wiimote.read_acc()
                forward = acc_to_speed(acc_y)
                left_fact = acc_to_rotation_left(acc_x)
                right_fact = acc_to_rotation_right(-acc_x)
                left = int(left_fact * forward)
                right = int(right_fact * forward)
                if self.wiimote.is_btn_b_pressed():
                    self.pwm.set_duty_a(-right)
                    self.pwm.set_duty_b(-left)
                else:
                    self.pwm.set_duty_a(left)
                    self.pwm.set_duty_b(right)
                print self.pwm.state
            elif btn_a_pressed:  # detect a release
                btn_a_pressed = False
                self.pwm.stop()
                print "STOP"
            time.sleep(self.refresh_pwm)

    def run(self):
        self.trigger.setup()
        try:
            while True:
                if self.trigger.triggered():
                    if not self.is_setup:
                        self.setup()
                    if not self.is_setup:
                        print "You had an error in controller setup"
                    else:
                        self.control_for(1000)
                else:
                    if self.is_setup:
                        self.cleanup()
                time.sleep(self.refresh_trigger)
        finally:
            self.cleanup()


if __name__ == "__main__":
    controller = Controller()
    controller.run()
