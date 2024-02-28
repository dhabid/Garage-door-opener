from machine import Pin
import time


switch = Pin(13, Pin.IN, Pin.PULL_UP)
relay = Pin(16, Pin.OUT) # The pin that is connected to the Input Circuit of the Relay


while True:  # Loop forever
    if switch.value() == 1:
        relay.value(0)  # Turn the relay ON
        time.sleep(1)
    else:
        relay.value(1)  # Turn the relay OFF
        time.sleep(1)

