# Choose pins

Next, you will need to choose what pins you will use. I have two garage doors that I want to control, one has access to the interior of the house and the other has access to the exterior.

## Interior Garage

I've used the **`pin GP6 for the reed switch that tells if the garage door is open`** and the **`pin GP12 to confirm if the garage door is closed`**.\
Note that you need to connect the other cable of the reed switch to GND, it doesn't matter which cable.\


On the relay, I've connected the **`IN1 of the relay to pin GP16`**, the **`GND of the relay to pin 38`**, and the **`VCC of the relay to pin 36`**.\
The relay will be used in NO(Normally open) mode.\


{% hint style="info" %}
**Normally open (NO)** contacts **connect** the circuit when the relay is activated; the circuit is disconnected when the relay is inactive.\
**Normally closed (NC)** contacts **disconnect** the circuit when the relay is activated; the circuit is connected when the relay is inactive.
{% endhint %}

## Exterior Garage

I've used the **`pin GP0 to confirm if the garage door is closed`**. Because the relay has 2 channels I've connected the **`IN2 of the relay to pin GP20`**.

You can see the pinout of the Raspberry Pi Pico w below:

![](https://github.com/dhabid/Garage-door-opener/raw/main/Images/PicoW-A4-Pinout.png)
