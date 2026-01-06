# -------------------- IMPORTS -------------------- #
from fastapi import FastAPI
from api.yugioh import get_card
# -------------------- MAIN -------------------- #

app = FastAPI()

@app.post("/card")
def process_card(card_name) :
	card = get_card(card_name)
	return card
