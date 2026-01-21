# -------------------- IMPORTS -------------------- #
from fastapi import FastAPI, HTTPException
from api.yugioh import get_card
from api.database import init_db, log_card, get_card_by_name, get_actions_between
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
def process_card(card_name: str, zone: str = "unknown", orientation: str = "unknown", action: str = "UNKNOWN") :
	card = get_card(card_name)

	name = card["name"]
	image = card["card_images"][0]["image_url"]
	log_card(name, image, zone, orientation, action)

	return card

@app.get("/actions")
def get_actions(start: str, end: str):
	"""
	Retourne toutes les actions entre 2 dates et heures.
	Format : ISO 8601 (ex: 2026-01-21T10:30:00)
	"""
	try:
		actions = get_actions_between(start, end)
		return {
			"start": start,
			"end": end,
			"count": len(actions),
			"actions": actions
		}
	except Exception as e:
		raise HTTPException(status_code=400, detail=f"Erreur lors de la récupération des actions : {str(e)}")
