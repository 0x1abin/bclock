import time
from servo import Servo

s = Servo(3)
try:
    s.angle(90)
    time.sleep(1)
    for a in range(0, 181, 5):
        s.angle(a)
        time.sleep_ms(30)
    for a in range(180, -1, -5):
        s.angle(a)
        time.sleep_ms(30)
    s.angle(90)
    time.sleep_ms(500)
finally:
    s.deinit()
    print("done")
