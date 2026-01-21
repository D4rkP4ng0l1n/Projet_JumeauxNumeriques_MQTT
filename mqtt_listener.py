# -------------------- IMPORTS -------------------- #
import paho.mqtt.client as mqtt
import requests
# -------------------- CONFIG -------------------- #
BROKER = "localhost"
PORT = 1883
API_URL = "http://localhost:8000/card"
# -------------------- TOPIC -------------------- #
TOPIC = "yugioh/card" # Topic entre carte et app
TOPIC_GODOT = "yugioh/godot_trigger" # Topic entre app et godot
# -------------------- CALLBACK -------------------- #

def on_connect(client, userdata, flags, rc) :
	if rc == 0:
		client.subscribe([
			(TOPIC, 0),
			(TOPIC_GODOT, 0)
		])
		print("Connecté au broker MQTT")
	else :
		print(f"Echec de connexion, code : {rc}")

def on_message(client, userdata, msg) :
	payload = msg.payload.decode()
	print(f"Message reçu sur {msg.topic} : {payload}")

	match msg.topic :
		case t if t == TOPIC :
			msgTopic(client, payload)
		case t if t == TOPIC_GODOT :
			msgTopicGodot(client, payload)
		case _ :
			pass
	

def msgTopic(client, card_name) :
	client.publish(TOPIC, card_name)
	print(f"Notification envoyée sur {TOPIC}")


def msgTopicGodot(client, card_name) :
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
