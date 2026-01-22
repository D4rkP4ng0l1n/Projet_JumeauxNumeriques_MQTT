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
			image_url TEXT NOT NULL,
			zone TEXT NOT NULL,
			orientation TEXT NOT NULL,
			action TEXT NOT NULL,
			timestamp TEXT NOT NULL
		)
	""")
	conn.commit()
	conn.close()

def log_card(card_name, image_url, zone, orientation, action):
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	cursor.execute(
		"INSERT INTO history (card_name, image_url, zone, orientation, action, timestamp) VALUES (?,?,?,?,?,?)", (card_name, image_url, zone, orientation, action, datetime.now().isoformat())
	)
	conn.commit()
	card_id = cursor.lastrowid
	conn.close()
	return card_id

def get_card_by_name(card_name):
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()

	cursor.execute("""
		SELECT card_name, image_url, zone, orientation, action, timestamp
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
		"zone": row[2],
		"orientation": row[3],
		"action": row[4],
		"timestamp": row[5]
	}

def get_card_by_id(id):
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()

	cursor.execute("""
		SELECT card_name, image_url, zone, orientation, action, timestamp
		FROM history
		WHERE id = ?
	""", (id,))

	row = cursor.fetchone()
	conn.close()
	
	if row is None:
		return None

	return {
		"card_name": row[0],
		"image_url": row[1],
		"zone": row[2],
		"orientation": row[3],
		"action": row[4],
		"timestamp": row[5]
	}


def get_actions_between(start_datetime, end_datetime):
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()

	cursor.execute("""
		SELECT id, card_name, image_url, zone, orientation, action, timestamp
		FROM history
		WHERE timestamp BETWEEN ? AND ?
		ORDER BY timestamp ASC
	""", (start_datetime, end_datetime))

	rows = cursor.fetchall()
	conn.close()
	
	if not rows:
		return []

	return [
		{
			"id": row[0],
			"card_name": row[1],
			"image_url": row[2],
			"zone": row[3],
			"orientation": row[4],
			"action": row[5],
			"timestamp": row[6]
		}
		for row in rows
	]

def get_all_cards():
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()

	cursor.execute("""
		SELECT id, card_name, image_url, zone, orientation, action, timestamp
		FROM history
		ORDER BY timestamp DESC
	""")

	rows = cursor.fetchall()
	conn.close()
	
	if not rows:
		return []

	return [
		{
			"id": row[0],
			"card_name": row[1],
			"image_url": row[2],
			"zone": row[3],
			"orientation": row[4],
			"action": row[5],
			"timestamp": row[6]
		}
		for row in rows
	]
