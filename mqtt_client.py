from paho.mqtt.client import Client

# Callback when a client connects to the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("test/topic")  # Subscribe to a topic

# Callback when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}'")

# Create an MQTT server instance
def run_mqtt_server():
    client = Client()  # Create an MQTT client instance
    client.on_connect = on_connect  # Assign on_connect callback
    client.on_message = on_message  # Assign on_message callback

    # Connect to the broker (localhost for local testing)
    client.connect("localhost", 1883, 60)

    # Start the loop to process network traffic and dispatch callbacks
    client.loop_forever()

# Run the server
if __name__ == "__main__":
    run_mqtt_server()