import RPi.GPIO as GPIO

# Headers for GPIO.BOARD configuration, comments are for BCM config
# motor 1
ENA = 29  # 5
IN1 = 33  # 13
IN2 = 7  # 4
# motor 2
IN3 = 13  # 27
IN4 = 16  # 23
ENB = 31  # 6

# PWM frequency
FREQ = 40

DEBUG = True


class L298N(object):
    def __init__(self):
        self.pwm_a, self.pwm_b = None, None
        self.state = {'a': 0, 'b': 0}

    @property
    def is_setup(self):
        return self.pwm_a is not None and self.pwm_b is not None

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        for output_pin in [ENA, IN1, IN2, IN3, IN4, ENB]:
            GPIO.setup(output_pin, GPIO.OUT)
        self.pwm_a = GPIO.PWM(ENA, FREQ)
        self.pwm_a.start(0)
        self.forward_a()
        self.pwm_b = GPIO.PWM(ENB, FREQ)
        self.pwm_b.start(0)
        self.forward_b()

    def cleanup(self):
        if DEBUG:
            print "cleanup"
        self.pwm_a.stop()
        self.pwm_b.stop()
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
                else:
                    self.forward_a()
            self.pwm_a.ChangeDutyCycle(abs(duty))
            self.state['a'] = duty

    def set_duty_b(self, duty):
        if duty != self.state['b']:
            if duty * self.state['b'] <= 0:
                if duty < 0:
                    self.backward_b()
                else:
                    self.forward_b()
            self.pwm_b.ChangeDutyCycle(abs(duty))
            self.state['b'] = duty

    def stop(self):
        self.set_duty_a(0)
        self.set_duty_b(0)
