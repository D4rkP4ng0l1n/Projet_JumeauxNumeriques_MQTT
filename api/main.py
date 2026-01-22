# -------------------- IMPORTS -------------------- #
from fastapi import FastAPI, HTTPException
from api.yugioh import get_card
from api.database import init_db, log_card, get_card_by_name, get_card_by_id, get_actions_between, get_all_cards
# -------------------- MAIN -------------------- #

app = FastAPI()

@app.on_event("startup")
def startup():
	init_db()

# Obtenir la dernière carte touchée avec son nom
@app.get("/card/{name}")
def read_card(name):
	card = get_card_by_name(name)
	
	if card is None:
		raise HTTPException(status_code=404, detail="Carte non trouvée")

	return card

# Obtenir les informations d'une carte avec son id
@app.get("/card/id/{card_id}")
def read_card_by_id(card_id):
	card = get_card_by_id(card_id)
	if card is None:
		raise HTTPException(status_code=404, detail="Carte non trouvée")

	return card

# Obtenir toutes les cartes de la BDD
@app.get("/cards")
def get_all():
	cards = get_all_cards()
	return {
		"count": len(cards),
		"cards": cards
	}

# Enregistrer une carte lorsqu'elle est jouée
@app.post("/card")
def process_card(card_name: str, zone: str = "unknown", orientation: str = "unknown", action: str = "unknown") :
	card = get_card(card_name)
	if card is None :
		raise HTTPException(status_code=404, detail="Carte non trouvée") 

	name = card["name"]
	image = card["card_images"][0]["image_url"]
	card_id = log_card(name, image, zone, orientation, action)

	return {
		"id": card_id
	}

# Obtenir le déroulé d'une partie
@app.get("/actions")
def get_actions(start, end):
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
