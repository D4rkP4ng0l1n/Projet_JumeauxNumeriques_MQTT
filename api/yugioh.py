# -------------------- IMPORTS -------------------- #
import requests
# -------------------- API -------------------- #
def get_card(name) :
	API = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
	r = requests.get(API, params={"name": name})
	data = r.json()["data"][0]
	return data

