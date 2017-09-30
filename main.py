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


acc_to_speed = speed_calculator(
    97,
    117,
    125,
    0,
    20,
    50
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

    def __init__(self):
        self.pwm = board.L298N()
        self.wiimote = wiimote.WiimoteController()

    def run(self):
        self.wiimote.connect()
        self.pwm.setup()

        try:
            while True:
                if self.wiimote.is_btn_a_pressed():
                    acc_x, acc_y, acc_z = self.wiimote.read_acc()
                    forward = acc_to_speed(acc_y)
                    left_fact = acc_to_rotation_left(acc_x)
                    right_fact = acc_to_rotation_right(-acc_x)
                    left = int(left_fact * forward)
                    right = int(right_fact * forward)
                    self.pwm.set_duty_a(left)
                    self.pwm.set_duty_b(right)
                time.sleep(0.05)
        except Exception:
            self.pwm.cleanup()
            print "Interrupted. Good bye."


if __name__ == "__main__":
    controller = Controller()
    controller.run()
