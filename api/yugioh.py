# -------------------- IMPORTS -------------------- #
import requests
# -------------------- API -------------------- #
def get_card(name) :
	PI = "https://db.ygoprAodeck.com/api/v7/cardinfo.php"
	r = requests.get(API, params={"name": name})
	data = r.json()["data"][0]
	return data

