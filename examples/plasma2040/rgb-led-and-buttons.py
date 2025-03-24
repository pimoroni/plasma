import time

# Import helpers for RGB LEDs and Buttons
from pimoroni import RGBLED, Button

user_sw = Button("USER_SW", repeat_time=0)
button_a = Button("BUTTON_A", repeat_time=0)
button_b = Button("BUTTON_B", repeat_time=0)
led = RGBLED("LED_R", "LED_G", "LED_B")
led.set_rgb(0, 0, 0)

while True:
    if user_sw.read():
        print("Pressed User SW - {}".format(time.ticks_ms()))
        led.set_rgb(255, 0, 0)
    if button_a.read():
        print("Pressed A - {}".format(time.ticks_ms()))
        led.set_rgb(0, 255, 0)
    if button_b.read():
        print("Pressed B - {}".format(time.ticks_ms()))
        led.set_rgb(0, 0, 255)
