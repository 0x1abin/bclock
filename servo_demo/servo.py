from machine import Pin, PWM


class Servo:
    MIN_US = 500
    MAX_US = 2500
    PERIOD_US = 20000

    def __init__(self, pin, freq=50, min_us=MIN_US, max_us=MAX_US):
        self.pwm = PWM(Pin(pin), freq=freq)
        self.min_us = min_us
        self.max_us = max_us

    def write_us(self, us):
        if us < self.min_us:
            us = self.min_us
        elif us > self.max_us:
            us = self.max_us
        duty = int(us * 65535 / self.PERIOD_US)
        self.pwm.duty_u16(duty)

    def angle(self, deg):
        if deg < 0:
            deg = 0
        elif deg > 180:
            deg = 180
        us = self.min_us + (self.max_us - self.min_us) * deg / 180
        self.write_us(int(us))

    def deinit(self):
        self.pwm.deinit()
