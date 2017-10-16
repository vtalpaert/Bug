import time
import RPi.GPIO as GPIO

# Headers for GPIO.BCM configuration
GPIO.setmode(GPIO.BCM)
# motor 1
ENA = 18
IN1 = 17
IN2 = 27
# motor 2
IN3 = 23
IN4 = 22
ENB = 24
# battery voltage reading pin
#BAT = 0
# trigger switch/button
TSW = 0
TBT = 25


# PWM frequency
FREQ = 40

DEBUG = False


class L298N(object):
    def __init__(self):
        self.pwm_a, self.pwm_b = None, None
        self.state = {'a': 0, 'b': 0}

    @property
    def is_setup(self):
        return self.pwm_a is not None and self.pwm_b is not None

    def setup(self):
        for output_pin in [ENA, IN1, IN2, IN3, IN4, ENB]:
            GPIO.setup(output_pin, GPIO.OUT)
        self.pwm_a = GPIO.PWM(ENA, FREQ)
        self.pwm_a.start(0)
        self.forward_a()
        self.pwm_b = GPIO.PWM(ENB, FREQ)
        self.pwm_b.start(0)
        self.forward_b()

    def cleanup(self, all_board=True):
        if DEBUG:
            print "cleanup"
        self.pwm_a.stop()
        self.pwm_b.stop()
        if all_board:
            GPIO.cleanup()

    def forward_a(self):
        if DEBUG:
            print "forward A"
        GPIO.output((IN1, IN2), (GPIO.LOW, GPIO.HIGH))

    def forward_b(self):
        if DEBUG:
            print "forward B"
        GPIO.output((IN3, IN4), (GPIO.LOW, GPIO.HIGH))

    def backward_a(self):
        if DEBUG:
            print "backward A"
        GPIO.output((IN1, IN2), (GPIO.HIGH, GPIO.LOW))

    def backward_b(self):
        if DEBUG:
            print "backward B"
        GPIO.output((IN3, IN4), (GPIO.HIGH, GPIO.LOW))

    def set_duty_a(self, duty):
        if duty != self.state['a']:
            if duty * self.state['a'] <= 0:
                if duty < 0:
                    self.backward_a()
                elif duty > 0:
                    self.forward_a()
            self.pwm_a.ChangeDutyCycle(abs(duty))
            self.state['a'] = duty

    def set_duty_b(self, duty):
        if duty != self.state['b']:
            if duty * self.state['b'] <= 0:
                if duty < 0:
                    self.backward_b()
                elif duty > 0:
                    self.forward_b()
            self.pwm_b.ChangeDutyCycle(abs(duty))
            self.state['b'] = duty

    def stop(self):
        self.set_duty_a(0)
        self.set_duty_b(0)

    def fast_stop(self):
        GPIO.output((IN1, IN2, IN3, IN4), (GPIO.LOW,)*4)
        self.stop()


class Button(object):
    def __init__(self, is_connected_to_high):
        self.is_connected_to_high = is_connected_to_high

    def setup(self):
        if self.is_connected_to_high:
            GPIO.setup(TBT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(TBT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def triggered(self):
        if self.is_connected_to_high:
            return GPIO.input(TBT)
        else:
            return not GPIO.input(TBT)


class Switch(object):
    @staticmethod
    def setup():
        GPIO.setup(TSW, GPIO.IN)

    @staticmethod
    def state():
        return GPIO.input(TSW)


class BoardManager(object):
    """Triggers on high"""
    def __init__(self):
        self.pwm = L298N()

    def __enter__(self):
        self.pwm.setup()
        return self, self.pwm

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pwm.cleanup(all_board=False)
        GPIO.cleanup()
