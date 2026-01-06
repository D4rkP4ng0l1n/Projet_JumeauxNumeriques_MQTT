# -------------------- IMPORTS -------------------- #
import sqlite3
from datetime import datetime
from pathlib import Path
# -------------------- DB -------------------- #

DB_PATH = Path("data/history.db")

def init_db():
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS history (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			card_name TEXT NOT NULL,
			image_url TEXT,
			timestamp TEXT NOT NULL
		)
	""")
	conn.commit()
	conn.close()

def log_card(card_name, image_url):
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	cursor.execute(
		"INSERT INTO history (card_name, image_url, timestamp) VALUES (?,?,?)", (card_name, image_url, datetime.now().isoformat())
	)
	conn.commit()
	conn.close()

def get_card_by_name(card_name):
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()

	cursor.execute("""
		SELECT card_name, image_url, timestamp
		FROM history
		WHERE card_name = ?
		ORDER BY timestamp DESC
		LIMIT 1
	""", (card_name,))

	row = cursor.fetchone()
	conn.close()
	
	if row is None:
		return None

	return {
		"card_name": row[0],
		"image_url": row[1],
	}
