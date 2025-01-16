---
icon: warehouse
description: >-
  This project was made because i wanted to remotely control my garage door
  using a Raspberry Pi and Home Assistant.
---

# Garage Door Opener

### Summary

This project is a step-by-step guide of what I did to remotely control my garage door using a Raspberry Pi and Home Assistant.

#### Table of Contents

[Introduction](../../#introduction)

[Prerequisites](../../#prerequisites)

[Raspberri pi pico w](../../#raspberri-pi-pico-w)

* [Installations](../../#installations)
* [Soldering](../../#soldering)
* [Choose pins](../../#choose-pins)

[Codes to test](../../#codes-to-test)

[Code on Raspberry pi pico w](../../#code-on-raspberry-pi-pico-w)

[Home Assistant](../../#home-assistant)

* [Install Home Assistant](../../#install-home-assistant)
* [Install Homebridge](../../#install-homebridge)
  * [Step 1: Add the repository](../../#step-1-add-the-repository)
  * [Step 2: Installing the Portainer add-on](../../#step-2-installing-the-portainer-add-on)
  * [Step 3: Setting up Portainer](../../#step-3-setting-up-portainer)
  * [Step 4: Deploying HomeBridge](../../#step-4-deploying-homebridge)

[Homebridge](../../#homebridge)

* [Install plugin](../../#install-plugin)
* [Edit the JSON config file](../../#edit-the-json-config-file)

[Connect to your Garage](../../#connect-to-your-garage)

[Remote Access](../../#remote-access)

* [Step 1: DuckDNS domain name setup](../../#step-1-duckdns-domain-name-setup)
* [Step 2: Port Forwarding](../../#step-2-port-forwarding)
* [Step 3: DuckDNS Home Assistant install and setup](../../#step-3-duckdns-home-assistant-install-and-setup)
* [Step 4: Port Forward validation](../../#step-4-port-forward-validation)
* [Step 5: Internal/External URL configuration change](../../#step-5-internalexternal-url-configuration-change)
* [Step 6: Security checks](../../#step-6-security-checks)

[Extra](../../#extra)

### Introduction



This project was made because i wanted to control my garage doors with my phone.\
Because I have an iPhone and other people who live with me don't, i will be using Home Assistant and Homebridge, that can do the bridge to Apple Homekit.

### Prerequisites



For this project you will need:\


* raspberry pi pico W or raspberry pi pico WH [8€](https://www.raspberrypi.com/products/raspberry-pi-pico/)\

* relay [1,40€](https://mauser.pt/catalog/product_info.php?products_id=096-7804)\

* reed switch [11€](https://www.amazon.es/-/pt/dp/B0BNBBZK7C/ref=sr_1_6?keywords=interruptores%2Bmagn%C3%A9ticos\&s=tools\&sr=1-6\&th=1)\

* jumper cables
* soldering
* Raspberry pi 3 or Raspberry pi 4 (recommended)

## Raspberri pi pico w



### Installations



To do all these things first you will need to install some things on your Raspberry Pi.\
You can do this tutorial and by the end, you should be good to go to the next step:\
[raspberry pi pico w installations](https://projects.raspberrypi.org/en/projects/introduction-to-the-pico/0)\


### Soldering



If you didn't buy the Raspberry Pi Pico WH you need to sold the pins.\
It should stay like this:\


[![](https://github.com/dhabid/Garage-door-opener/raw/main/Images/soldered_pins.jpg)](../../Images/soldered_pins.jpg)

### Choose pins



Next, you will need to choose what pins you will use.\


#### Interior Garage



I've used the **`pin GP6 for the reed switch that tells if the garage door is open`** and the **`pin GP12 to confirm if the garage door is closed`**.\
Note that you need to connect the other cable of the reed switch to GND, it doesn't matter which cable.\


On the relay i've connected the **`IN1 of the relay to pin GP16`**, the **`GND of the relay to pin 38`**, and the **`VCC of the relay to pin 36`**.\
The relay will be used in NO(Normally open) mode.\


Tip

Normally open (NO) contacts connect the circuit when the relay is activated; the circuit is disconnected when the relay is inactive.\
Normally closed (NC) contacts disconnect the circuit when the relay is activated; the circuit is connected when the relay is inactive.\


#### Exterior Garage



I've used the **`pin GP0 to confirm if the garage door is closed`**. Because the relay has 2 channels i've connected the **`IN2 of the relay to pin GP20`**.

You can see the pinout of the raspberry pi pico w below:

[![](https://github.com/dhabid/Garage-door-opener/raw/main/Images/PicoW-A4-Pinout.png)](../../Images/PicoW-A4-Pinout.png)

Tip

### Codes to test



Here you can do some tests to check if everything is ok.

#### Test relay with LED



To test the relay with an LED copy the code in `test_relay_with_LED.py` and paste it into thonny editor.\
Add the LED to the breadboard, connecting its Negative Leg to one of the Ground Pins of the Pico.\
Connect one side of the Resistor to the Positive Leg of the LED.\
Connect the other side of the Resistor to the Common terminal of the Relay.\
Connect the Normally Open terminal of the Relay to the VBUS pin of the Pico.\


#### Test relay and sensors with LED



To test the relay and sensors with an LED copy the code in `test_relay_reedswitch_with_LED.py` and paste it in thonny editor. Then the LED should turn ON when the sensor is closed.

#### See your IP address



To see your IP address just copy the code in `connect_pi_to_network_and_show_IP.py` and paste it into thonny editor.\
You just need to change the WIFI settings to yours, sot the pico can connect to your WIFI. Then run the code.\
That IP address is the IP of your rasberry pi pico w, take note of the IP address you will need it down below.\


### Code on Raspberry pi pico w



#### Code to control the garage door



To control your garage door just copy the code in `main.py` and paste it into thonny editor.\


Important

**You need to keep the name of the file main.py so the code is always running**

Note

Remember to change the WIFI settings and the pins you connected the reed switches and the relay.\


## Home Assistant



### Install Home Assistant



Now you need to install Home Assistant operating system on your raspberry pi 4.\
To do this just go to [this site](https://www.home-assistant.io/installation/raspberrypi/) and follow the steps.\


Within a few minutes after connecting the Raspberry Pi, you will be able to reach your new Home Assistant.

In the browser of your desktop system, enter [homeassistant.local:8123](http://homeassistant.local:8123/).

If you are running an older Windows version or have a stricter network configuration, you might need to access Home Assistant at homeassistant:8123 or `http://X.X.X.X:8123` (replace X.X.X.X with your Raspberry Pi’s IP address).

### Install Homebridge



Once you've completed installing and now have access to your Home Assistant you need to install Homebridge.\
To do that you can see [this video](https://www.youtube.com/watch?v=xPj5vrK6-3k) or follow the following steps.

#### Step 1: Add the repository



* Go to `Configuration` -> `Add-ons` -> `Add-on Store`
* `Click on the three dots` -> `Repositories` -> `Paste this address (https://github.com/MikeJMcGuire/HASSAddons) and click 'Add'`.\
  Now you should see a section like this: [![Mike JMcGuire Section](https://github.com/dhabid/Garage-door-opener/raw/main/Images/section_Mike.png)](../../Images/section_Mike.png)

#### Step 2: Installing the Portainer add-on



* Now on that section `click on Portainer and install it`.
* Once installed `disable Protection Mode` and `enable Watchdog` and click on Start.
* After a moment `click on Open Web UI` and `login to Portainer`.

#### Step 3: Setting up Portainer



* The default credentials are `admin for username` and `portainer for the password`.
* `Change the password once you've logged in`.

#### Step 4: Deploying HomeBridge



* Now on Home click on `Primary` -> `Stacks` -> `Add Stacks`
* Put `homebridge` as a name and then `paste the following lines into the web editor`:

```
version: '2'
services:
  homebridge:
    image: oznu/homebridge:ubuntu
    restart: always
    network_mode: host
    environment:
      - PGID=1000
      - PUID=1000
      - HOMEBRIDGE_CONFIG_UI=1
      - HOMEBRIDGE_CONFIG_UI_PORT=8581
      - TZ=Europe/Lisbon
    volumes:
      - /mnt/data/supervisor/homeassistant/homebridge:/homebridge
```

* Note to `replace Europe/Lisbon to your timezone`.
* `Click deploy the stack` and give it some time.

### Homebridge



The Homebridge UI web interface will allow you to install, remove and update plugins, and modify the Homebridge config.json and manage other aspects of your Homebridge service.\


Login to the web interface by going to [homeassistant.local:8581](http://homeassistant.local:8581/).\
If you are running an older Windows version or have a stricter network configuration, you might need to access Home Assistant at homeassistant:8581 or `http://X.X.X.X:8581` (replace X.X.X.X with your Raspberry Pi’s IP address).

#### Install plugin



In the Homebridge UI go to plugins and then search for this plugin and install it: [![http-advanced-accessory-plugin](https://github.com/dhabid/Garage-door-opener/raw/main/Images/http-advanced-accessory-plugin.png)](../../Images/http-advanced-accessory-plugin.png)

#### Edit the JSON config file



On Plugins, go to HTTP Advanced Accessory plugin click on the 3 dots, and go to JSON config.\
[![go to JSON config file](https://github.com/dhabid/Garage-door-opener/raw/main/Images/JSON_config.png)](../../Images/JSON_config.png)

To add the Exterior garage door copy and paste the code from `Exterior.json`.\
Now i need to add the Interior garage door, for that i just click on the plus button and then copy and paste the code from `Interior.json`.\


Note

Be aware to change the `YOUR_HOMEBRIDGE_USERNAME`, `YOUR_HOMEBRIDGE_PASSWORD` and `YOUR_RASPBERRY_PI_PICOW_IP_ADDRESS` variables to the ones you have.

Remember that when you're done you need to `restart Homebridge` so that the changes have an effect.\


After that on the main page, a QR code like this should appear:\


[![](https://github.com/dhabid/Garage-door-opener/raw/main/Images/pair_Homekit.png)](../../Images/pair_Homekit.png)

Important

`Keep that 7-digit code`. You will need it in the next step.

#### Add the Homebridge Accessories to Home Assistant



To add the Homebridge accessories to Home Assistant you just need to go to the `main page in Home Assistant` -> `Settings` -> `Devices and Services` and something like this should appear in discovered:\
[![Homekit Device](https://github.com/dhabid/Garage-door-opener/raw/main/Images/Homekit_device.png)](../../Images/Homekit_device.png)

`Click on it and then paste the 7-digit code` obtained in the step before.

## Connect to your Garage



The final step is to connect to your garage.\


* Go to the motor in your garage and see what pins open the garage.\
  To do that just take a multimeter or a pliers and connect two screws like the picture below shows (one of them should be ground) and test all of them until your garage open:\


[![](https://github.com/dhabid/Garage-door-opener/raw/main/Images/Pins_garagedoor.jpg)](../../Images/Pins_garagedoor.jpg)

Note

One end must always be connected to the motor ground.

Warning

**For your safety on the step below disconnect the electricity from the motor.**

* Once you've found what pins open your garage door, just reconnect the COM of the relay to the ground pin you just discovered on your motor and the NO to the other pin that opens and closes the garage door.

Once that is completed you can turn on the electricity on the motor, go to your phone and open the garage door on Home Assistant app!!!

## Remote Access



Now you can control your garage door with your network.\
To control the garage door from anywhere you can watch [this video](https://www.youtube.com/watch?v=AK5E2T5tWyM) or follow the steps below.

### Step 1: DuckDNS domain name setup



* Go to [DuckDNS webstite](https://www.duckdns.org/) and log in
* Once you log in you can `create a subdomain`. It can be anything you want as long as it is not already in use.\


Note

This will be the URL that you will be using to connect to your HomeAssistant.

* Change the current IP to 8.8.8.8 and save it.

Important

Copy your token from the top because we will need it in the next step.

### Step 2: Port Forwarding



Tip

Port forwarding is a way of allowing people from the internet to connect to you. A port forward puts a device outside of your router as if it was directly connected to the internet.\


Next, you need to go to your router webpage and configure Port Forward.\
If you don't know your router webpage you can check your router. But usually is something like [http://192.168.1.1/](http://192.168.1.1/).\
If you don't know how to Port Forward check [this website](https://portforward.com/) and search for your router.\
In my case (Vodafone Gigabox router) these were the steps:

* Go to `Internet`->`Port Mapping`->`Click the Plus Button` Something like this should appear:\


[![](https://github.com/dhabid/Garage-door-opener/raw/main/Images/Portmapping.png)](../../Images/Portmapping.png)

* On `Name put HomeAssistant`
* Choose `TCP as the service`
* Choose `Home Assistant as the Device`
* The `LAN IP should be the same as your Home Assistant IP`
* On `Public Port put 8123`
* On `LAN Port put 8123`
* Click `save` Now add another Port Mapping.\

* `Repeat all as the above` but on `Public Port put 443` Add another Port Mapping.
* On `Name put Homebridge`
* Choose `TCP as the service`
* Choose `Home Assistant as the Device`
* The `LAN IP should be the same as your Home Assistant IP`
* On `Public Port put 8581`
* On `LAN Port put 8581`\


Tip

Port 8183 will be used for mobile apps and your desktop. Port 443 is useful for services like Alexa and Google Home. Port 8581 is for access to your Homebridge.

### Step 3: DuckDNS Home Assistant install and setup



Now you need to install DuckDNS add-on.\


* To do that `in Home Assistant go to Add-on store`, `search for DuckDNS add-on and install it`.\

* `Enable Watchdog` and `Auto update`.\

* Go to the `Configuration page` and `paste the token` that you copy into the DuckDNS webpage.
* Put `true in accept_terms`.
* Put `your domain name in the domains box` and `save it`.
* `Go to the Log page and keep refreshing` until you see something like this:\


[![](https://github.com/dhabid/Garage-door-opener/raw/main/Images/Logpage.png)](../../Images/Logpage.png)

* Once that's done `go to the DuckDNS webpage and replace 8.8.8.8 with your public IP address` (the one blurred above 31.48.x.x)
* Go to your `Home Assistant Configuration.yaml and add this code`:

```
# Loads default set of integrations. Do not remove.
default_config:

http:
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem
```

* Next go to `Developer tools` -> `Check Configuration` and if you get a successful message `Restart Home Assistant`.

### Step 4: Port Forward validation



* Go to `[https://canyouseeme.org/](https://canyouseeme.org/)`
* In `Your IP put the blurred one` (in this case 31.48.x.x) and in `Port to check put 8123` and click Check Port
* It should appear a successful message, if it doesn't go back and check if you haven't entered any wrong information
* `Repeat these steps for ports 443 and 8581`.

### Step 5: Internal/External URL configuration change



* Go to `Settings` -> `System` -> `Network`
* In Home Assistant URL set Internet and Local Network to the DuckDNS domain name and save it

### Step 6: Security checks



* Make sure you have some decent passwords
* Once everything is tested and working enable the IP ban in the Home Assistant Configuration.yaml

```
# Loads default set of integrations. Do not remove.
default_config:

http:
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem
  ip_ban_enabled: true
  login_attempts_threshold: 5

```

Note

This will only allow 5 login attempts from a certain IP address. Once those login attempts have been reached it will automatically blacklist that IP address.

* Next go to `Configurations`, `check your configuration`, and `restart the Home Assistant`.

## Extra



If you want to add your accessories to the Apple Homekit app you can [watch this video](https://www.youtube.com/watch?v=9G2f_c3fnyc\&t=117s) or follow these steps:

* Go to `Configuration.yaml` file and `add this code`:

```
homekit:
  - name: HA Bridge
    port: 51828
    filter:
      include_entities:
        - cover.interior
        - cover.exterior
```

Note

In include\_entities you can put all the accessories you want.

* Next go to `Configurations`, `check your configuration`, and `restart the Home Assistant`.
* Once is restarted, in Notifications, you should see a Homekit Pairing QR code.
* Open the Home app on your iPhone, scan it and add the Bridge.

Note

These accessories will not work remotely on the Apple Homekit app.\
You can control them remotely only on your Home Assistant app.
