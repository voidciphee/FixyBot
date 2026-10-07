import re
from utils.logger import get_logger

log = get_logger("fixy_ai")


UNIVERS = {
    "tokyo_revengers": [
        "tokyo revengers", "toman", "tokyo manji", "bonten",
        "tenjiku", "valhalla", "moebius", "black dragons",
        "kanto manji", "brahman", "rokuhara", "thousand winters",
    ],
    "wind_breaker": [
        "wind breaker", "bofurin", "bōfūrin", "shishitoren",
        "keel", "gravel", "roppo ichiza", "furin",
    ],
    "reality_quest": [
        "reality quest", "gwanak", "boramae", "sillim", "iljinhoe",
        "joppok", "baekho", "heukryong", "cheongryong", "jujak",
        "hyeonmu", "heukho", "quartier gwanak",
    ],
    "jujika_no_rokunin": ["jujika no rokunin", "jujika"],
    "my_dress_up_darling": ["my dress-up darling", "dress-up darling"],
    "darling_in_the_franxx": ["darling in the franxx", "franxx"],
}

TYPES = {
    "rp": ["rp", "roleplay", "jeu de rôle"],
    "communauté": ["communauté", "community", "discussion"],
    "gaming": ["gaming", "esport", "team"],
    "business": ["business", "projet", "entreprise"],
}

ELEMENTS = {
    "missions": ["mission", "objectif", "opération"],
    "trahisons": ["trahison", "traître", "enquête", "surveillance",
                  "jugement"],
    "alliances": ["alliance", "diplomatie", "traité", "conflit",
                  "guerre", "territoire"],
    "recrutement": ["recrutement", "candidature", "test", "recrue"],
    "vocal": ["vocal", "vox", "voice"],
    "moderation": ["modération", "anti-spam", "anti raid", "sécurité"],
    "economie": ["économie", "monnaie", "boutique"],
    "logs": ["logs", "audit"],
}


def _normalize(text: str) -> str:
    return text.lower().strip()


def detect_univers(texte: str) -> str | None:
    t = _normalize(texte)
    for univ, mots in UNIVERS.items():
        if any(mot in t for mot in mots):
            return univ
    return None


def detect_gang(texte: str, univers: str | None) -> str | None:
    if not univers:
        return None
    t = _normalize(texte)
    for mot in UNIVERS.get(univers, []):
        if mot in t:
            return mot
    return None


def detect_type(texte: str) -> str:
    t = _normalize(texte)
    for kind, mots in TYPES.items():
        if any(mot in t for mot in mots):
            return kind
    return "communauté"


def detect_elements(texte: str) -> list[str]:
    t = _normalize(texte)
    return [cle for cle, mots in ELEMENTS.items()
            if any(mot in t for mot in mots)]


def detect_nombre_salons(texte: str) -> int | None:
    m = re.search(r"(\d+)\s*salons?", _normalize(texte))
    return int(m.group(1)) if m else None


def detect_nombre_vocaux(texte: str) -> int | None:
    m = re.search(r"(\d+)\s*(salons?\s*)?voca", _normalize(texte))
    return int(m.group(1)) if m else None


def build_plan(texte: str) -> dict:
    univers = detect_univers(texte)
    gang = detect_gang(texte, univers)
    kind = detect_type(texte)
    elements = detect_elements(texte)
    n_salons = detect_nombre_salons(texte)
    n_vocaux = detect_nombre_vocaux(texte)

    roles = {
        "tokyo_revengers": 10, "wind_breaker": 9, "reality_quest": 12,
    }.get(univers, 6)

    plan = {
        "univers": univers,
        "gang": gang,
        "type": kind,
        "elements": elements,
        "n_salons": n_salons,
        "n_vocaux": n_vocaux,
        "roles_estimes": roles,
        "categories_estimees": 4 + len(elements),
        "salons_estimes": n_salons or (20 + 4 * len(elements)),
        "vocaux_estimes": n_vocaux or 8,
    }
    log.info("Plan IA : %s", plan)
    return plan