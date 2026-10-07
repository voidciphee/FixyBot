import asyncio
import hashlib
import discord


def perms_for_rank(rank: str) -> discord.Permissions:
    r = rank.lower()
    if any(k in r for k in (
        "leader", "king", "boss", "commander", "chef",
        "chef du district", "chef de l'alliance", "chef de l'organisation",
        "chef du quartier général", "fondateur", "teppen",
        "président", "dirigeant", "oyabun", "wakagashira",
        "général", "commandant", "chef de l'iljinhoe", "chef du joppok",
        "chef du baekho", "chef du heukryong", "chef du cheongryong",
        "chef du jujak", "chef du hyeonmu", "chef du heukho",
        "chef du bongcheon", "roi", "famille royale",
    )):
        return discord.Permissions(administrator=True)
    if any(k in r for k in (
        "vice", "officier supérieur", "dirigeant", "conseil",
        "représentant", "responsable", "executive", "officer", "lieutenant",
        "roi", "second", "bras droit", "colonel", "shatei-gashira",
        "sergent d'armes", "trésorier", "garde royale", "garde du roi",
    )):
        return discord.Permissions(
            manage_messages=True, kick_members=True, mute_members=True,
            move_members=True, manage_nicknames=True,
            read_message_history=True, send_messages=True, view_channel=True,
        )
    if any(k in r for k in (
        "capitaine", "captain", "chef d'équipe", "chef de division",
        "chef d'unité", "cadre", "responsable de secteur",
        "caporal-chef", "road captain", "chef de section",
    )):
        return discord.Permissions(
            manage_messages=True, mute_members=True, move_members=True,
            read_message_history=True, send_messages=True, view_channel=True,
        )
    if any(k in r for k in ("recrue", "recruit", "novice", "temporaire",
                            "nouveau membre", "nomade", "prospect",
                            "civil", "habitant")):
        return discord.Permissions(
            view_channel=True, send_messages=True, read_message_history=True,
        )
    return discord.Permissions(
        view_channel=True, send_messages=True, read_message_history=True,
        attach_files=True, embed_links=True, add_reactions=True,
    )


def _hash_int(s: str) -> int:
    return int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16)


def _safe_color(r: int, g: int, b: int) -> discord.Color:
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return discord.Color.from_rgb(r, g, b)


def couleur_par_importance(rank: str, couleur_base_hex: str) -> discord.Color:
    r_str = rank.lower()
    importance = "membre"
    if any(k in r_str for k in (
        "roi", "famille royale", "gouvernement", "conseil royal",
        "noblesse", "garde royale", "garde du roi",
        "légende", "maître suprême", "seigneur", "empereur",
        "reine", "gardien", "idole suprême", "commandant suprême",
        "chef", "président", "général", "directeur",
    )):
        importance = "direction"
    elif any(k in r_str for k in (
        "vice", "officier", "commandant", "capitaine", "lieutenant",
        "brigadier", "colonel", "sergent", "consul", "maître",
        "représentant", "responsable", "second", "bras droit",
    )):
        importance = "haut"

    try:
        base_rgb = int(couleur_base_hex.lstrip("#"), 16)
    except Exception:
        base_rgb = 0xC8102E

    base_r = (base_rgb >> 16) & 0xFF
    base_g = (base_rgb >> 8) & 0xFF
    base_b = base_rgb & 0xFF

    h = _hash_int(rank + couleur_base_hex)

    if importance == "direction":
        r = base_r + 40 + ((h >> 16) & 0x1F)
        g = base_g + 40 + ((h >> 8) & 0x1F)
        b = base_b + 40 + (h & 0x1F)
    elif importance == "haut":
        r = base_r + 10 + ((h >> 16) & 0x1F)
        g = base_g + 10 + ((h >> 8) & 0x1F)
        b = base_b + 10 + (h & 0x1F)
    else:
        r = base_r - 20 + ((h >> 16) & 0x1F)
        g = base_g - 20 + ((h >> 8) & 0x1F)
        b = base_b - 20 + (h & 0x1F)

    return _safe_color(r, g, b)


def couleur_unique(nom_role: str, base_hex: str = "#C8102E") -> discord.Color:
    try:
        base_rgb = int(base_hex.lstrip("#"), 16)
    except Exception:
        base_rgb = 0xC8102E
    h = _hash_int(nom_role)
    base_r = (base_rgb >> 16) & 0xFF
    base_g = (base_rgb >> 8) & 0xFF
    base_b = base_rgb & 0xFF
    r = base_r + ((h >> 16) & 0x3F) - 30
    g = base_g + ((h >> 8) & 0x3F) - 30
    b = base_b + (h & 0x3F) - 30
    return _safe_color(r, g, b)


def detecter_groupe(rank: str) -> str:
    r = rank.lower()
    if any(k in r for k in (
        "leader", "king", "boss", "chef", "teppen", "président",
        "oyabun", "wakagashira", "général", "commandant", "fondateur",
        "représentant principal", "chef du district", "roi",
        "famille royale",
    )):
        return "DIRECTION"
    if any(k in r for k in (
        "vice", "roi", "second", "bras droit", "colonel", "lieutenant",
        "capitaine", "officier", "dirigeant", "représentant", "cadre",
        "responsable", "conseiller", "trésorier", "sergent",
    )):
        return "HAUTS GRADÉS"
    return "MEMBRES"


def is_chef(rank: str) -> bool:
    r = rank.lower()
    return r.strip() in ("roi", "président", "leader", "teppen", "chef",
                         "famille royale", "fondateur")


# ══════════════════════════════════════════════════════
# ⭐ FONCTION UTILITAIRE POUR CRÉER LES RÔLES SANS BLOCAGE
# ══════════════════════════════════════════════════════

async def creer_role_avec_timeout(guild, **kwargs):
    """Crée un rôle avec un timeout de 15 secondes.
    Si Discord ne répond pas, on log et on continue."""
    try:
        return await asyncio.wait_for(
            guild.create_role(**kwargs),
            timeout=15.0,
        )
    except asyncio.TimeoutError:
        import logging
        logging.getLogger("permissions").error(
            "⏱ TIMEOUT création rôle '%s'", kwargs.get("name", "?")
        )
        return None
    except discord.HTTPException as e:
        import logging
        logging.getLogger("permissions").error(
            "❌ HTTP %s création rôle '%s' : %s",
            e.status, kwargs.get("name", "?"), e,
        )
        return None
    except Exception as e:
        import logging
        logging.getLogger("permissions").exception(
            "❌ Exception création rôle '%s' : %s",
            kwargs.get("name", "?"), e,
        )
        return None


async def creer_categorie_avec_timeout(guild, **kwargs):
    try:
        return await asyncio.wait_for(
            guild.create_category(**kwargs), timeout=15.0
        )
    except asyncio.TimeoutError:
        import logging
        logging.getLogger("permissions").error(
            "⏱ TIMEOUT création catégorie '%s'", kwargs.get("name", "?")
        )
        return None
    except Exception as e:
        import logging
        logging.getLogger("permissions").exception(
            "❌ Catégorie '%s' : %s", kwargs.get("name", "?"), e
        )
        return None


async def creer_salon_avec_timeout(parent, **kwargs):
    try:
        return await asyncio.wait_for(
            parent.create_text_channel(**kwargs), timeout=15.0
        )
    except asyncio.TimeoutError:
        import logging
        logging.getLogger("permissions").error(
            "⏱ TIMEOUT création salon '%s'", kwargs.get("name", "?")
        )
        return None
    except Exception as e:
        import logging
        logging.getLogger("permissions").exception(
            "❌ Salon '%s' : %s", kwargs.get("name", "?"), e
        )
        return None


async def creer_vocal_avec_timeout(parent, **kwargs):
    try:
        return await asyncio.wait_for(
            parent.create_voice_channel(**kwargs), timeout=15.0
        )
    except asyncio.TimeoutError:
        import logging
        logging.getLogger("permissions").error(
            "⏱ TIMEOUT création vocal '%s'", kwargs.get("name", "?")
        )
        return None
    except Exception as e:
        import logging
        logging.getLogger("permissions").exception(
            "❌ Vocal '%s' : %s", kwargs.get("name", "?"), e
        )
        return None