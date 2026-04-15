import asyncio
from machine import Pin
import neopixel

import config


def _scale(rgb, factor):
    return (
        int(rgb[0] * factor),
        int(rgb[1] * factor),
        int(rgb[2] * factor),
    )


class AnimationRunner:
    def __init__(self, pin=config.LED_PIN, n=config.LED_COUNT, brightness=config.BRIGHTNESS):
        self._np = neopixel.NeoPixel(Pin(pin, Pin.OUT), n)
        self._n = n
        self._brightness = brightness / 255.0
        self._task = None
        self._clear()

    def _clear(self):
        for i in range(self._n):
            self._np[i] = (0, 0, 0)
        self._np.write()

    def _fill(self, rgb):
        scaled = _scale(rgb, self._brightness)
        for i in range(self._n):
            self._np[i] = scaled
        self._np.write()

    def set_cmd(self, code):
        if self._task is not None:
            self._task.cancel()
        self._task = asyncio.create_task(self._dispatch(code))

    async def _dispatch(self, code):
        try:
            if code == config.CMD_DONE:
                await self._done()
            elif code == config.CMD_ERROR:
                await self._error()
            elif code == config.CMD_PLAN:
                await self._plan()
            elif code == config.CMD_ATTENTION:
                await self._attention()
            else:
                self._clear()
        except asyncio.CancelledError:
            pass

    async def _breathe_cycle(self, base, step=4, sleep_ms=20, pause_ms=150):
        for s in range(0, 101, step):
            self._fill(_scale(base, s / 100.0))
            await asyncio.sleep_ms(sleep_ms)
        for s in range(100, -1, -step):
            self._fill(_scale(base, s / 100.0))
            await asyncio.sleep_ms(sleep_ms)
        if pause_ms:
            await asyncio.sleep_ms(pause_ms)

    async def _done(self):
        for _ in range(3):
            await self._breathe_cycle((0, 255, 0), step=5, sleep_ms=15, pause_ms=80)
        self._clear()

    async def _error(self):
        base = (255, 0, 0)
        for _ in range(3):
            self._fill(base)
            await asyncio.sleep_ms(140)
            self._clear()
            await asyncio.sleep_ms(140)

    async def _plan(self):
        while True:
            await self._breathe_cycle((140, 220, 255))

    async def _attention(self):
        while True:
            await self._breathe_cycle((30, 60, 255))


if __name__ == "__main__":
    async def _demo():
        anim = AnimationRunner()
        for name, code, hold in (
            ("done", config.CMD_DONE, 4000),
            ("error", config.CMD_ERROR, 2000),
            ("plan 2s", config.CMD_PLAN, 2000),
            ("attention 2s", config.CMD_ATTENTION, 2000),
            ("off", config.CMD_OFF, 500),
        ):
            print("demo:", name)
            anim.set_cmd(code)
            await asyncio.sleep_ms(hold)
        print("RESULT:ok")

    asyncio.run(_demo())
