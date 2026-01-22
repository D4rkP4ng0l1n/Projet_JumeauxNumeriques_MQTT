# 🃏 Projet Jumeaux Numériques MQTT

Un système complet de gestion de cartes Yu-Gi-Oh! en temps réel utilisant MQTT et une API REST, intégrant une base de données SQLite pour l'historique des actions.

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Endpoints de l'API](#-endpoints-de-lapi)
- [Topics MQTT](#-topics-mqtt)
- [Technologies](#-technologies)
- [Licence](#-licence)

---

## 🎯 Vue d'ensemble

Ce projet implémente une architecture de **jumeaux numériques** pour Yu-Gi-Oh! permettant de :

✨ **Synchroniser** les états des cartes entre une application Godot et un broker MQTT
🗄️ **Stocker** l'historique complet des actions effectuées sur les cartes
🔍 **Récupérer** les données des cartes via l'API officielle YGOProDeck
📡 **Communiquer** en temps réel via MQTT et REST

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐
│   Godot App     │         │   MQTT Broker    │
│   (Client)      │◄───────►│   (Mediateur)    │
└─────────────────┘         └──────────────────┘
        ▲                              ▲
        │                              │
        │        MQTT Topics           │
        │      (Pub/Subscribe)         │
        │                              │
        └──────────────┬───────────────┘
                       │
                ┌──────▼───────┐
                │   Listener   │
                │ (mqtt_listener)
                └──────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   ┌────────┐   ┌─────────┐   ┌──────────┐
   │ YGODeck│   │  FastAPI│   │ SQLite DB│
   │  API   │   │         │   │          │
   └────────┘   └─────────┘   └──────────┘
```

---

## 📦 Prérequis

- **Python** 3.8+
- **Mosquitto** ou tout broker MQTT compatible
- **pip** (gestionnaire de paquets Python)

---

## 🚀 Installation

### 1. Cloner le repository

\`\`\`bash
git clone https://github.com/D4rkP4ng0l1n/Projet_JumeauxNumeriques_MQTT.git
cd Projet_JumeauxNumeriques_MQTT
\`\`\`

### 2. Créer un environnement virtuel

\`\`\`bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
\`\`\`

### 3. Installer les dépendances

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Démarrer le broker MQTT

\`\`\`bash
mosquitto
\`\`\`

---

## ⚙️ Configuration

Les paramètres principaux se trouvent dans [mqtt_listener.py](mqtt_listener.py) :

\`\`\`python
# Configuration MQTT
BROKER = "localhost"      # Adresse du broker
PORT = 1883              # Port MQTT standard

# Configuration API
API_URL = "http://localhost:8000/card"

# Topics MQTT
TOPIC_CARD_IN = "yugioh/card/in"
TOPIC_CARD_OUT = "yugioh/card/out"
TOPIC_GODOT_IN = "yugioh/godot/in"
TOPIC_GODOT_OUT = "yugioh/godot/out"
\`\`\`

---

## 💻 Utilisation

### Démarrer l'API FastAPI

\`\`\`bash
cd api
uvicorn main:app --reload --port 8000
\`\`\`

L'API sera disponible à : **http://localhost:8000**

### Démarrer le listener MQTT

\`\`\`bash
python mqtt_listener.py
\`\`\`

Le listener va :
1. Se connecter au broker MQTT
2. S'abonner aux topics définis
3. Traiter les messages reçus
4. Loguer les actions dans la base de données

---

## 📁 Structure du projet

\`\`\`
.
├── mqtt_listener.py          # Listener MQTT principal
├── api/
│   ├── __init__.py
│   ├── main.py              # Application FastAPI
│   ├── database.py          # Gestion SQLite
│   └── yugioh.py            # API YGOProDeck
├── data/
│   └── history.db           # Base de données SQLite (créée automatiquement)
├── requirements.txt         # Dépendances Python
└── README.md               # Ce fichier
\`\`\`

---

## 🔌 Endpoints de l'API

### GET /card/{name}
Récupère les dernières données d'une carte par son nom

**Paramètres :**
- `name` : Nom de la carte

**Réponse :**
\`\`\`json
{
  "card_name": "Blue-Eyes White Dragon",
  "image_url": "url_de_l_image",
  "zone": "Monster1",
  "orientation": "Visible",
  "action": "PLACED",
  "timestamp": "2026-01-22T10:30:00"
}
\`\`\`

### POST /card
Enregistre une action sur une carte

**Paramètres (query) :**
- `card_name` : Nom de la carte (requis)
- `zone` : Zone du terrain
- `orientation` : Visible/Cachee
- `action` : Type d'action

### GET /actions
Récupère toutes les actions entre deux dates/heures

**Paramètres (query) :**
- `start` : Date/heure de début (format ISO 8601)
- `end` : Date/heure de fin (format ISO 8601)

**Format ISO 8601 :**
\`\`\`
2026-01-21T10:30:00
```

**Réponse :**
\`\`\`json
{
  "start": "2026-01-21T10:00:00",
  "end": "2026-01-21T20:00:00",
  "count": 15,
  "actions": [
    {
      "id": 1,
      "card_name": "Blue-Eyes White Dragon",
      "image_url": "...",
      "zone": "Monster Zone",
      "orientation": "face-up",
      "action": "SUMMON",
      "timestamp": "2026-01-21T15:30:45"
    },
    ...
  ]
}
\`\`\`

---

## 📡 Topics MQTT

| Topic | Direction | Description |
|-------|-----------|-------------|
| `yugioh/card/in` | Subscribe | Reçoit les données des cartes du téléphone |
| `yugioh/card/out` | Publish | Envoie les données des cartes au téléphone |
| `yugioh/godot/in` | Subscribe | Reçoit les données de Godot |
| `yugioh/godot/out` | Publish | Envoie les données à Godot |

---

## 🛠️ Technologies

| Technology | Utilisation |
|-----------|------------|
| **Python 3** | Langage principal |
| **FastAPI** | Framework API REST |
| **Uvicorn** | Serveur ASGI |
| **Paho MQTT** | Client MQTT |
| **SQLite** | Base de données |
| **Requests** | Appels HTTP |
| **YGOProDeck API** | Données des cartes |

---

## 🔄 Flux de fonctionnement

1. **Godot App** envoie une action via MQTT (`yugioh/godot/in`)
2. **MQTT Listener** reçoit le message
3. **Listener** récupère les données de la carte via l'API YGOProDeck
4. **Listener** enregistre l'action dans la base de données
5. **API REST** expose les données via les endpoints
6. **Godot App** peut consulter l'historique via l'API

---

## 📊 Base de données

La table `history` contient :
- `id` : Identifiant unique
- `card_name` : Nom de la carte
- `image_url` : URL de l'image
- `zone` : Zone du terrain
- `orientation` : Orientation de la carte (Visible/Cachee)
- `action` : Type d'action effectuée
- `timestamp` : Horodatage ISO 8601

---

## 🐛 Troubleshooting

**Erreur : "Échec de connexion au broker MQTT"**
- Vérifiez que Mosquitto est lancé
- Vérifiez l'adresse du broker et le port

**Erreur : "Carte non trouvée"**
- Vérifiez que le nom de la carte est correct
- L'API YGOProDeck doit être accessible

**Base de données vide**
- La base de données se crée automatiquement au démarrage
- Vérifiez les permissions d'accès au répertoire `data/`

---

## 👨‍💻 Auteur

Développé pour le projet de **Jumeaux Numériques** en 3IL - Ingésup

---