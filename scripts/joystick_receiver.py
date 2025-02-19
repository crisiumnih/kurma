import paho.mqtt.client as mqtt
import threading
import time
from turtle_movements import move_forward, move_backward, rotate_clockwise, rotate_counterclockwise, stop_movement

# MQTT Broker details
broker = "192.168.0.124"
port = 1883

# Global state variable to track current movement
current_movement = None
movement_lock = threading.Lock()

def execute_movement():
    """Continuously executes the current movement command"""
    global current_movement
    
    while True:
        with movement_lock:
            movement = current_movement
            
        if movement:
            if movement == "forward":
                move_forward()
            elif movement == "backward":
                move_backward()
            elif movement == "clockwise":
                rotate_clockwise()
            elif movement == "anticlockwise":
                rotate_counterclockwise()
            elif movement == "stop":
                stop_movement()
                
        time.sleep(0.1)  # Small delay to prevent CPU overuse

def on_message(client, userdata, msg):
    """Callback when a message is received"""
    global current_movement
    
    topic = msg.topic
    payload = msg.payload.decode()
    
    with movement_lock:
        if topic == "joystick/x":
            if payload in ["forward", "backward", "stop"]:
                current_movement = payload
                print(f"X command received: {payload}")
                
        elif topic == "joystick/y":
            if payload in ["clockwise", "anticlockwise", "stop"]:
                current_movement = payload
                print(f"Y command received: {payload}")
                
        elif topic == "joystick/switch":
            if payload == "1":
                current_movement = "stop"
                print("Reset command received")

def main():
    # Create and start movement thread
    movement_thread = threading.Thread(target=execute_movement, daemon=True)
    movement_thread.start()
    
    # Create MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    
    # Connect to MQTT broker
    try:
        client.connect(broker, port)
        print(f"Connected to MQTT broker at {broker}:{port}")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return
    
    # Subscribe to joystick topics
    client.subscribe([
        ("joystick/x", 0),
        ("joystick/y", 0),
        ("joystick/switch", 0)
    ])
    
    print("Listening for joystick commands...")
    
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        stop_movement()
        client.disconnect()

if __name__ == "__main__":
    main()
