import asyncio

import config
import servo


class ServoRunner:
    NEUTRAL = 90
    LEFT = 60
    RIGHT = 120
    STEP_MS = 150
    CYCLES = 3

    def __init__(self, pin=config.SERVO_PIN):
        self._servo = servo.Servo(pin)
        self._servo.angle(self.NEUTRAL)
        self._task = None

    def set_cmd(self, code):
        if self._task is not None:
            self._task.cancel()
        self._task = asyncio.create_task(self._dispatch(code))

    async def _dispatch(self, code):
        try:
            if code in (config.CMD_DONE, config.CMD_ERROR, config.CMD_ATTENTION):
                await self._wave()
            else:
                self._servo.angle(self.NEUTRAL)
        except asyncio.CancelledError:
            pass
        finally:
            try:
                self._servo.angle(self.NEUTRAL)
            except Exception:
                pass

    async def _wave(self):
        self._servo.angle(self.NEUTRAL)
        await asyncio.sleep_ms(self.STEP_MS)
        for _ in range(self.CYCLES):
            self._servo.angle(self.LEFT)
            await asyncio.sleep_ms(self.STEP_MS)
            self._servo.angle(self.RIGHT)
            await asyncio.sleep_ms(self.STEP_MS)
        self._servo.angle(self.NEUTRAL)
        await asyncio.sleep_ms(self.STEP_MS)


if __name__ == "__main__":
    async def _demo():
        runner = ServoRunner()
        for name, code, hold in (
            ("done", config.CMD_DONE, 2500),
            ("error", config.CMD_ERROR, 2500),
            ("attention", config.CMD_ATTENTION, 2500),
            ("plan (no wave)", config.CMD_PLAN, 800),
            ("off", config.CMD_OFF, 500),
        ):
            print("demo:", name)
            runner.set_cmd(code)
            await asyncio.sleep_ms(hold)
        print("RESULT:ok")

    asyncio.run(_demo())
