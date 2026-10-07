import json
import os
from config import DATA_DIR
from utils.logger import get_logger

log = get_logger("database")


def list_universes() -> list[str]:
    if not os.path.isdir(DATA_DIR):
        return []
    return sorted(f[:-5] for f in os.listdir(DATA_DIR) if f.endswith(".json"))


def load_universe(name: str) -> dict:
    path = os.path.join(DATA_DIR, f"{name}.json")
    if not os.path.exists(path):
        log.warning("Univers introuvable : %s", name)
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)