# -------------------- IMPORTS -------------------- #
import paho.mqtt.client as mqtt
import requests
# -------------------- CONFIG -------------------- #
BROKER = "localhost"
PORT = 1883
TOPIC = "yugioh/card"

# -------------------- CALLBACK -------------------- #

def on_connect(client, userdata, flags, rc) :
	if rc == 0 :
		print("Connecté au broker MQTT !")
		client.subscribe(TOPIC)
		print(f"Abonné au topic : {TOPIC}")
	else :
		print(f"Echec de connexion, code : {rc}")

def on_message(client, userdata, msg) :
	card_name = msg.payload.decode()
	print(f"Message reçu : {card_name}")

# -------------------- CLIENT MQTT -------------------- #

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Connexion au broker MQTT...")
client.connect(BROKER, PORT, 60)

client.loop_forever()
