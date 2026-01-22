# -------------------- IMPORTS -------------------- #
import requests
from fastapi import HTTPException
# -------------------- API -------------------- #
def get_card(name) :
	try:
		API = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
		r = requests.get(API, params={"name": name})
		data = r.json()["data"][0]
		return data
	except Exception as e :
		raise HTTPException(status_code=404, detail="Carte innexistante dans l'api ygoprodeck")