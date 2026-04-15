import asyncio

import aioble

import config


PREFIX = "bclock:"


async def scan_loop(anim):
    last_nonce = None
    while True:
        try:
            print("scan: starting")
            async with aioble.scan(
                duration_ms=0,
                interval_us=config.SCAN_INTERVAL_US,
                window_us=config.SCAN_WINDOW_US,
                active=False,
            ) as scanner:
                async for r in scanner:
                    name = r.name()
                    if not name or not name.startswith(PREFIX):
                        continue
                    try:
                        _, cc, nn = name.split(":")
                        cmd = int(cc, 16)
                        nonce = int(nn, 16)
                    except (ValueError, IndexError):
                        continue
                    if nonce == last_nonce:
                        continue
                    last_nonce = nonce
                    print("scan: cmd", hex(cmd), "nonce", hex(nonce))
                    anim.set_cmd(cmd)
        except Exception as e:
            print("scan err:", e)
            await asyncio.sleep_ms(500)
