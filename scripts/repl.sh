#!/usr/bin/env bash
PORT="${BCLOCK_PORT:-/dev/cu.usbserial-10}"
exec mpremote connect "$PORT"
