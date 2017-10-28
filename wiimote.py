import cwiid


class WiimoteController(object):

    def __init__(self):
        self.wm = None

    @property
    def is_connected(self):
        return self.wm is not None

    def connect(self, retries=5, exit_if_fail=True):
        print 'Press 1+2 on your Wiimote now...'
        i = 1
        while not self.wm:
            try:
                self.wm = cwiid.Wiimote()
            except RuntimeError:
                if i > retries:
                    print('cannot create connection')
                    if exit_if_fail:
                        quit()
                    else:
                        return False
                print 'Error opening wiimote connection'
                print 'attempt ' + str(i)
                i += 1

        # turn on led to show connected
        self.wm.led = 1

        print 'connected',
        print 'battery at %s%%' % self.read_battery()
        return True

    def set_mode(self, btn, acc, nunchuk):
        if btn and acc and nunchuk:
            self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK
        elif btn and acc:
            self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        elif btn and nunchuk:
            self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_NUNCHUK
        else:
            print 'Not Implemented...'

    def read_battery(self):
        return self.wm.state['battery']

    def is_btn_a_pressed(self):
        return self.wm.state['buttons'] & cwiid.BTN_A

    def is_btn_b_pressed(self):
        return self.wm.state['buttons'] & cwiid.BTN_B

    def read_acc(self):
        return self.wm.state['acc']

    def cleanup(self):
        if self.wm:
            self.wm.close()

    def read_stick(self):
        if 'nunchuk' in self.wm.state:
            return self.wm.state['nunchuk']['stick']

    def read_nunchuk_btn(self):
        if 'nunchuk' in self.wm.state:
            return self.wm.state['nunchuk']['buttons']

    def is_btn_c_pressed(self):
        try:
            return self.read_nunchuk_btn() & cwiid.NUNCHUK_BTN_C
        except TypeError:
            return False

    def is_btn_z_pressed(self):
        try:
            return self.read_nunchuk_btn() & cwiid.NUNCHUK_BTN_Z
        except TypeError:
            return False


def simplify_sitck(values):
    if values is None:
        return 0, 0
    clean1 = 2 * (values[0] - 131.5) / (232 - 31)
    clean2 = 2 * (values[1] - 128.) / (225 - 31)
    return clean1, clean2

import math

def get_speed_angle(values):
    x, y = simplify_sitck(values)
    if abs(x) < 0.07 and abs(y) < 0.07:
        return 0, 0
    length = math.sqrt(x ** 2 + y ** 2)
    angle = math.asin(x / length)
    return make_pwm(length, angle)


def make_pwm(length, angle):
    length = length * 100 * 6. / 8.5
    if length == 0:
        return 0, 0
    left = length
    right = length
    if angle < 0:
        left = max(0, 1./0.7 * angle + 1) * length
    if angle > 0:
        right = max(0, -1./0.7 * angle +1) * length
    return int(left), int(right)


if __name__ == '__main__':
    example = {'led': 1, 'rpt_mode': 18, 'ext_type': 1, 'buttons': 0, 'rumble': 0, 'error': 0,
        'nunchuk': {'acc': (178, 122, 139), 'buttons': 0, 'stick': (135, 131)}, 'battery': 59}
    """
    middle 135 130
    up 133 225
    down 135 31
    total left 31 127
    total right 232 127
    left up 59 203
    right up 208 203
    left btm 60 55
    right btm 207.5 57
    """
    from time import sleep
    wiimote = WiimoteController()
    wiimote.connect()
    wiimote.set_mode(True, False, True)
    try:
        while True:
            stick = wiimote.read_stick()
            if stick:
                print get_speed_angle(stick)
            sleep(0.1)
    except KeyboardInterrupt:
        wiimote.cleanup()
