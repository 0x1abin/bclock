import asyncio

import led
import ble_server

asyncio.run(ble_server.scan_loop(led.AnimationRunner()))
