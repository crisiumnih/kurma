import paho.mqtt.client as mqtt

# MQTT Broker details
broker = "localhost"  # Broker is running on the same Raspberry Pi
port = 1883  # Default MQTT port
topic = "test/topic"  # Topic to subscribe to

# Callback when a message is received
def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

# Create MQTT client with the latest API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Assign callback
client.on_message = on_message

# Connect to broker
try:
    print(f"Connecting to MQTT Broker at {broker}:{port}...")
    client.connect(broker, port, 60)
    print("Connected to MQTT Broker!")
except Exception as e:
    print(f"Failed to connect to MQTT Broker: {e}")
    exit(1)

# Subscribe to topic
client.subscribe(topic)
print(f"Subscribed to topic: {topic}")

# Loop to process incoming messages
client.loop_forever()
