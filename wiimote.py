import cwiid


class WiimoteController(object):

    def __init__(self):
        self.wm = None

    @property
    def is_connected(self):
        return self.wm is not None

    def connect(self, retries=5):
        print 'Press 1+2 on your Wiimote now...'
        i = 1
        while not self.wm:
            try:
                self.wm = cwiid.Wiimote()
            except RuntimeError:
                if i > retries:
                    print('cannot create connection')
                    quit()
                print 'Error opening wiimote connection'
                print 'attempt ' + str(i)
                i += 1

        # set wiimote to report button presses and accelerometer state
        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

        # turn on led to show connected
        self.wm.led = 1

        print 'connected',
        print 'battery at %s%%' % self.read_battery()

    def read_battery(self):
        return self.wm.state['battery']

    def is_btn_a_pressed(self):
        return self.wm.state['buttons'] & cwiid.BTN_A

    def is_btn_b_pressed(self):
        return self.wm.state['buttons'] & cwiid.BTN_B

    def read_acc(self):
        return self.wm.state['acc']