import time
import paho.mqtt.client as mqtt
import socket

MQTT_BROKER_HOST = "broker.emqx.io"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "gateway/ip"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        publish_ip_address(client)
    else:
        print(f"Connection failed with result code {rc}. Retrying in 5 seconds...")
        time.sleep(5)
        client.reconnect()

def publish_ip_address(client):
    ip_address = get_raspberry_pi_ip()
    client.publish(MQTT_TOPIC, ip_address)
    print(f"IP address published: {ip_address}")

def get_raspberry_pi_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's DNS server
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return "Unknown"

def main():
    client = mqtt.Client()
    client.on_connect = on_connect

    while True:
        try:
            client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
            client.loop_forever()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
