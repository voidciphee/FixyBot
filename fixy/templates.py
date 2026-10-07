import json
import os
import discord
from utils.logger import get_logger

log = get_logger("fixy_templates")

DIR = "data/fixy_templates"
os.makedirs(DIR, exist_ok=True)


def sauvegarder_template(guild: discord.Guild, nom: str) -> str:
    data = {
        "nom": nom,
        "roles": [
            {
                "name": r.name,
                "color": r.colour.value,
                "permissions": r.permissions.value,
                "hoist": r.hoist,
                "position": r.position,
            }
            for r in guild.roles
            if not r.is_default() and not r.managed
        ],
        "categories": [
            {
                "name": c.name,
                "channels": [ch.name for ch in c.channels],
            }
            for c in guild.categories
        ],
        "text_channels": [
            c.name for c in guild.text_channels if c.category is None
        ],
        "voice_channels": [
            c.name for c in guild.voice_channels if c.category is None
        ],
    }
    chemin = os.path.join(DIR, f"{nom}.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log.info("Template sauvegardé : %s", chemin)
    return chemin


def lister_templates() -> list[str]:
    return [f[:-5] for f in os.listdir(DIR) if f.endswith(".json")]


def charger_template(nom: str) -> dict:
    chemin = os.path.join(DIR, f"{nom}.json")
    if not os.path.exists(chemin):
        return {}
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


def supprimer_template(nom: str) -> bool:
    chemin = os.path.join(DIR, f"{nom}.json")
    if os.path.exists(chemin):
        os.remove(chemin)
        return True
    return False