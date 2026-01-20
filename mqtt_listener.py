# -------------------- IMPORTS -------------------- #
import paho.mqtt.client as mqtt
import requests
# -------------------- CONFIG -------------------- #
BROKER = "localhost"
PORT = 1883
TOPIC = "yugioh/card"
TOPIC_GODOT = "yugioh/godot_trigger"
API_URL = "http://localhost:8000/card"
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

	try :
		response = requests.post(API_URL, params={"card_name": card_name})
		if response.status_code == 200 :
			data = response.json()
			print(f"{data}")
			client.publish(TOPIC_GODOT, card_name)
			print(f"Notification envoyée à Godot sur {TOPIC_GODOT}")

		else :
			print(f"Erreur API : {response.status_code}")
	except Exception as e :
		print(f"Erreur requête API : {e}")

# -------------------- CLIENT MQTT -------------------- #

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Connexion au broker MQTT...")
client.connect(BROKER, PORT, 60)

client.loop_forever()
