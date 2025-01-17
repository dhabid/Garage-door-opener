---
description: Here you can do some tests to check if everything is ok.
---

# Codes to test

## Test relay with LED

To test the relay with an LED copy the following code and paste it into Thonny editor.

{% code fullWidth="false" %}
```python
from machine import Pin
import time

relay = Pin(16, Pin.OUT) # The pin that is connected to the Input Circuit of the Relay

while True:  # Loop forever
    relay.value(0)  # Turn the relay ON
    time.sleep(1)
    relay.value(1)  # Turn the relay OFF
    time.sleep(1)
```
{% endcode %}

Now do the following:

{% stepper %}
{% step %}
Add the LED to the breadboard, connecting its Negative Leg to one of the Ground Pins of the Pico
{% endstep %}

{% step %}
Connect one side of the Resistor to the Positive Leg of the LED
{% endstep %}

{% step %}
Connect the other side of the Resistor to the Common terminal of the Relay
{% endstep %}

{% step %}
Connect the Normally Open terminal of the Relay to the VBUS pin of the Pico
{% endstep %}
{% endstepper %}

***

## Test relay and sensors with LED

To test the relay and sensors with an LED copy the following code and paste it in thonny editor. Then the LED should turn ON when the sensor is closed.

```python
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
```

***

## See your IP address

To see your IP address just copy the following code andd paste it into thonny editor.

```python
import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wi-FI name","Password")

wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print("waiting for connection...")
    time.sleep(1)
    
    
if wlan.status() != 3:
    raise RuntimeError("wifi connection failed")
else:
    print("connected")
    print("IP: ",wlan.ifconfig()[0])
```

\
You just need to change the WI-FI Name and Password to yours, so the pico can connect to your WI-FI. Then run the code.\
That IP address is the IP of your Raspberry Pi Pico w, take note of the IP address you will need it down below.
