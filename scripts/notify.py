#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyobjc-framework-CoreBluetooth>=10"]
# ///
"""bclock host notifier — broadcast a single-byte command via BLE advertisement."""

from __future__ import annotations

import argparse
import random
import sys
import time

import objc
from Foundation import NSObject, NSRunLoop, NSDate
from CoreBluetooth import (
    CBPeripheralManager,
    CBAdvertisementDataLocalNameKey,
    CBManagerStatePoweredOn,
)


COMMANDS = {"off": 0x00, "done": 0x01, "error": 0x02, "plan": 0x03, "attention": 0x04}
ADVERTISE_WINDOW_S = 0.5
POWERON_TIMEOUT_S = 2.0
RUNLOOP_SLICE_S = 0.05


class Broadcaster(NSObject):
    def init(self):
        self = objc.super(Broadcaster, self).init()
        if self is None:
            return None
        self.ready = False
        self.mgr = CBPeripheralManager.alloc().initWithDelegate_queue_(self, None)
        return self

    def peripheralManagerDidUpdateState_(self, mgr):
        self.ready = mgr.state() == CBManagerStatePoweredOn


def _pump(loop, seconds):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        loop.runMode_beforeDate_(
            "NSDefaultRunLoopMode",
            NSDate.dateWithTimeIntervalSinceNow_(RUNLOOP_SLICE_S),
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="bclock broadcaster")
    parser.add_argument("state", choices=list(COMMANDS))
    args = parser.parse_args()

    cmd = COMMANDS[args.state]
    nonce = random.randint(0, 0xFFFFFFFF)
    name = f"bclock:{cmd:02x}:{nonce:08x}"

    broadcaster = Broadcaster.alloc().init()
    loop = NSRunLoop.currentRunLoop()
    deadline = time.monotonic() + POWERON_TIMEOUT_S
    while not broadcaster.ready and time.monotonic() < deadline:
        loop.runMode_beforeDate_(
            "NSDefaultRunLoopMode",
            NSDate.dateWithTimeIntervalSinceNow_(RUNLOOP_SLICE_S),
        )

    if not broadcaster.ready:
        return 0

    broadcaster.mgr.startAdvertising_({CBAdvertisementDataLocalNameKey: name})
    _pump(loop, ADVERTISE_WINDOW_S)
    broadcaster.mgr.stopAdvertising()
    return 0


if __name__ == "__main__":
    sys.exit(main())
