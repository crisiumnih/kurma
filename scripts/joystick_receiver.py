import paho.mqtt.client as mqtt
from turtle_movements import move_forward, move_backward, rotate_clockwise, rotate_counterclockwise, stop_movement

# MQTT Broker details
broker = "192.168.29.5"
port = 1883

# Callback when a message is received
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    if topic == "joystick/x":
        if payload == "forward":
            move_forward()  # Call move_forward function
        elif payload == "backward":
            move_backward()  # Call move_backward function
        elif payload == "stop":
            stop_movement()  # Call stop_movement function

    elif topic == "joystick/y":
        if payload == "clockwise":
            rotate_clockwise()  # Call rotate_clockwise function
        elif payload == "anticlockwise":
            rotate_counterclockwise()  # Call rotate_counterclockwise function
        elif payload == "stop":
            stop_movement()  # Call stop_movement function

    elif topic == "joystick/switch":
        if payload == "1":
            stop_movement()  # Call stop_movement function for reset
            print("reset")  # Print "reset" to terminal

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker, port)

# Subscribe to joystick topics
client.subscribe("joystick/x")
client.subscribe("joystick/y")
client.subscribe("joystick/switch")

print("Listening for joystick commands...")
client.loop_forever()
