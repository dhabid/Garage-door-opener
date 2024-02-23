import network
import socket
import time
from uselect import select
from machine import Pin

# Turn the Raspberry Pi LED on to see that it's running
led = Pin('LED', Pin.OUT)
led.on()

# WiFi Settings. Change these before uploading to the Pi Pico
WIFI_SSID = 'Vodafone-ACFE67'
WIFI_PASSWORD = '4MFAJFFD6X9X6JMA'

# Set up pins for the first garage door
OPEN_PIN = 6
CLOSED_PIN = 12
RELAY_PIN = 16

# Set up pins for the second garage door
CLOSED_PIN_EXTERIOR = 0
RELAY_PIN_EXTERIOR = 20

# Pulse length in ms
PULSE_LENGTH = 500

# Homekit target and current states for the first garage door
TARGET_DOOR_STATE_OPEN = 0
TARGET_DOOR_STATE_CLOSED = 1
CURRENT_DOOR_STATE_OPEN = 0
CURRENT_DOOR_STATE_CLOSED = 1
CURRENT_DOOR_STATE_OPENING = 2
CURRENT_DOOR_STATE_CLOSING = 3
CURRENT_DOOR_STATE_STOPPED = 4

# Homekit target and current states for the second garage door
TARGET_DOOR_STATE_OPEN_EXTERIOR = 0
TARGET_DOOR_STATE_CLOSED_EXTERIOR = 1
CURRENT_DOOR_STATE_OPEN_EXTERIOR = 0
CURRENT_DOOR_STATE_CLOSED_EXTERIOR = 1
CURRENT_DOOR_STATE_OPENING_EXTERIOR = 2
CURRENT_DOOR_STATE_CLOSING_EXTERIOR = 3
CURRENT_DOOR_STATE_STOPPED_EXTERIOR = 4

IGNORE_SENSORS_AFTER_ACTION_FOR_SECONDS = 5


#Setup pins for relay and sensors for interior door
relay = Pin(RELAY_PIN, Pin.OUT)
openSensor=Pin(OPEN_PIN, Pin.IN, Pin.PULL_UP)
closedSensor=Pin(CLOSED_PIN, Pin.IN, Pin.PULL_UP)
#Setup pins for relay and sensors for exterior door
relayExterior = Pin(RELAY_PIN_EXTERIOR, Pin.OUT)
closedSensorExterior = Pin(CLOSED_PIN_EXTERIOR, Pin.IN, Pin.PULL_UP)

# Set initial target and current states for the first garage door
targetState = TARGET_DOOR_STATE_CLOSED
currentState = CURRENT_DOOR_STATE_STOPPED

# Set initial target and current states for the second garage door
targetStateExterior = TARGET_DOOR_STATE_CLOSED_EXTERIOR
currentStateExterior = CURRENT_DOOR_STATE_STOPPED_EXTERIOR

lastDoorAction = time.time()

# Setup WiFi connection
wifi = network.WLAN(network.STA_IF)


def connectWifi():
    global wifi

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(WIFI_SSID, WIFI_PASSWORD)

    max_wait = 10
    while wifi.status() != 3:
        print('waiting for connection. Status: ' + str(wifi.status()))
        time.sleep(1)

    print('connected')
    status = wifi.ifconfig()
    ipAddress = status[0]
    print('ip = ' + ipAddress)


connectWifi()

# Set up socket and start listening on port 80
addr = socket.getaddrinfo(wifi.ifconfig()[0], 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('listening on', addr)


def startDoor(newTargetState):
    global targetState
    global currentState
    global lastDoorAction

    targetState = newTargetState
    lastDoorAction = time.time()

    relay.value(0)
    time.sleep_ms(PULSE_LENGTH)
    relay.value(1)

    setCurrentState()

    print('startDoor', targetState, currentState)

    return getDoorStatus()


def startDoorExterior(newTargetStateExterior):
    global targetStateExterior
    global currentStateExterior
    global lastDoorAction
    
    targetStateExterior = newTargetStateExterior
    lastDoorAction = time.time()

    relayExterior.value(0)
    time.sleep_ms(PULSE_LENGTH)
    relayExterior.value(1)

    setCurrentStateExterior()

    print('startDoorExterior', targetStateExterior, currentStateExterior)

    return getDoorStatusExterior()


def setCurrentState():
    global targetState
    global currentState
    global openSensor
    global closedSensor

    # Ignore sensors after having started the door for a few seconds to give the door enough time to move away from the sensor
    actionThresholdReached = time.time() > lastDoorAction + IGNORE_SENSORS_AFTER_ACTION_FOR_SECONDS

    # If threshold is reached and door is fully open
    if actionThresholdReached and openSensor.value() == 0:
        currentState = CURRENT_DOOR_STATE_OPEN
        targetState = TARGET_DOOR_STATE_OPEN

    # If threshold is reached and door is fully closed
    elif actionThresholdReached and closedSensor.value() == 0:
        currentState = CURRENT_DOOR_STATE_CLOSED
        targetState = TARGET_DOOR_STATE_CLOSED

    # Threshold has not been reached or door is neither fully open or closed
    else:

        # Set current state based on intention (target state)
        if targetState == TARGET_DOOR_STATE_OPEN:
            currentState = CURRENT_DOOR_STATE_OPENING
        elif targetState == TARGET_DOOR_STATE_CLOSED:
            currentState = CURRENT_DOOR_STATE_CLOSING


def setCurrentStateExterior():
    global targetStateExterior
    global currentStateExterior
    global openSensorExterior
    global closedSensorExterior

    # Ignore sensors after having started the door for a few seconds to give the door enough time to move away from the sensor
    actionThresholdReached = time.time() > lastDoorAction + IGNORE_SENSORS_AFTER_ACTION_FOR_SECONDS

    # If threshold is reached and door is fully open
    if actionThresholdReached and closedSensorExterior.value() == 0:
        currentStateExterior = CURRENT_DOOR_STATE_OPEN_EXTERIOR
        targetStateExterior = TARGET_DOOR_STATE_OPEN_EXTERIOR

    # If threshold is reached and door is fully closed
    elif actionThresholdReached and closedSensorExterior.value() == 1:
        currentStateExterior = CURRENT_DOOR_STATE_CLOSED_EXTERIOR
        targetStateExterior = TARGET_DOOR_STATE_CLOSED_EXTERIOR


def getDoorStatus():
    global targetState
    global currentState

    # Ensure current state is up to date
    setCurrentState()

    return '{"success": true, "currentState": ' + str(currentState) + ', "targetState": ' + str(targetState) + '}'


def getDoorStatusExterior():
    global targetStateExterior
    global currentStateExterior

    # Ensure current state is up to date
    setCurrentStateExterior()

    return '{"success": true, "currentState": ' + str(currentStateExterior) + ', "targetState": ' + str(targetStateExterior) + '}'


def returnError(errcode):
    return '{"success": false, "error": "' + errcode + '"}'


# Handle an incoming request
def handleRequest(conn, address):
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)

    print(request)

    if '/?open' in request:
        response = startDoor(TARGET_DOOR_STATE_OPEN)
    elif '/?close' in request:
        response = startDoor(TARGET_DOOR_STATE_CLOSED)
    elif '/?getstatus' in request:
        response = getDoorStatus()
    elif '/?oExterior' in request:
        response = startDoorExterior(TARGET_DOOR_STATE_OPEN_EXTERIOR)
    elif '/?cExterior' in request:
        response = startDoorExterior(TARGET_DOOR_STATE_CLOSED_EXTERIOR)
    elif '/?gsExterior' in request:
        response = getDoorStatusExterior()
    else:
        response = returnError('UNKNOWN_COMMAND')

    conn.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
    conn.send(response)
    conn.close()


# Main Loop
while True:
    # Check if WiFi is connected, if not, reconnect
    if wifi.isconnected() == False:
        print('Connecting wifi...')
        connectWifi()

    # Handle incoming HTTP requests in a non-blocking way
    r, w, err = select((s,), (), (), 1)

    # Is there an incoming request? If so, handle the request
    if r:
        for readable in r:
            conn, addr = s.accept()
            try:
                handleRequest(conn, addr)
            except OSError as e:
                pass



