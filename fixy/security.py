import json
import os
from utils.logger import get_logger

log = get_logger("fixy_security")
FICHIER = "data/fixy_security.json"


def charger_config(guild_id: int) -> dict:
    if not os.path.exists(FICHIER):
        return {}
    with open(FICHIER, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(guild_id), {})


def sauvegarder_config(guild_id: int, config: dict):
    data = {}
    if os.path.exists(FICHIER):
        with open(FICHIER, "r", encoding="utf-8") as f:
            data = json.load(f)
    data[str(guild_id)] = config
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)