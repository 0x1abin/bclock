import asyncio

import led
import servo_anim
import ble_server


class Notifier:
    def __init__(self):
        self._led = led.AnimationRunner()
        self._servo = servo_anim.ServoRunner()

    def set_cmd(self, code):
        self._led.set_cmd(code)
        self._servo.set_cmd(code)


asyncio.run(ble_server.scan_loop(Notifier()))
