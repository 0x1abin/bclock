#!/usr/bin/env bash
set -euo pipefail

PORT="${BCLOCK_PORT:-/dev/cu.usbserial-10}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FW="$ROOT/firmware"

echo "flashing $FW -> $PORT"

for f in config.py led.py servo.py servo_anim.py ble_server.py main.py; do
  echo "  cp $f"
  mpremote connect "$PORT" cp "$FW/$f" ":$f"
done

echo "  reset"
mpremote connect "$PORT" reset
echo "done"
