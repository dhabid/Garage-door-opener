from machine import Pin
import time

relay = Pin(16, Pin.OUT) # The pin that is connected to the Input Circuit of the Relay

while True:  # Loop forever
    relay.value(0)  # Turn the relay ON
    time.sleep(1)
    relay.value(1)  # Turn the relay OFF
    time.sleep(1)
