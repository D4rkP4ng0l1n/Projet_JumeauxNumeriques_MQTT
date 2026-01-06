# -------------------- IMPORTS -------------------- #
from fastapi import FastAPI, HTTPException
from api.yugioh import get_card
from api.database import init_db, log_card, get_card_by_name
# -------------------- MAIN -------------------- #

app = FastAPI()

@app.on_event("startup")
def startup():
	init_db()

@app.get("/card/{name}")
def read_card(name):
	card = get_card_by_name(name)
	
	if card is None:
		raise HTTPException(status_code=404, detail="Carte non trouvée")

	return card

@app.post("/card")
def process_card(card_name) :
	card = get_card(card_name)

	name = card["name"]
	image = card["card_images"][0]["image_url"]
	log_card(name, image)

	return card
