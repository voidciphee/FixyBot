import discord
from utils.permissions import perms_for_rank
from utils.logger import get_logger
from generators.role_generator import create_roles_with_separators

log = get_logger("custom_generator")

HIERARCHIES = {
    "gang_urbain": [
        ("👑", "Chef"), ("👑", "Co-chef"), ("⚔️", "Vice-chef"),
        ("🏛️", "Dirigeant"), ("📋", "Représentant"),
        ("⚔️", "Capitaine"), ("⚔️", "Vice-capitaine"),
        ("🛡️", "Officier supérieur"), ("🛡️", "Officier"),
        ("🔥", "Chef de division"), ("🔥", "Chef d'équipe"),
        ("👊", "Membre d'élite"), ("👊", "Membre confirmé"),
        ("👊", "Membre"), ("🔰", "Recrue"),
    ],
    "gang_yakuza": [
        ("👑", "Oyabun"), ("👑", "Wakagashira"),
        ("⚔️", "Shatei-gashira"), ("🏛️", "Wakashu"),
        ("📋", "Conseiller"), ("⚔️", "Capitaine"),
        ("🛡️", "Lieutenant"), ("🔥", "Chef d'équipe"),
        ("👊", "Membre d'élite"), ("👊", "Membre"),
        ("🔰", "Recrue"),
    ],
    "gang_militaire": [
        ("👑", "Général"), ("👑", "Commandant"),
        ("⚔️", "Colonel"), ("🏛️", "Capitaine"),
        ("📋", "Lieutenant"), ("🛡️", "Sergent"),
        ("🔥", "Caporal-chef"), ("👊", "Caporal"),
        ("👊", "Soldat d'élite"), ("👊", "Soldat"),
        ("🔰", "Recrue"),
    ],
    "gang_biker": [
        ("👑", "Président"), ("⚔️", "Vice-président"),
        ("🏛️", "Sergent d'armes"), ("📋", "Trésorier"),
        ("⚔️", "Road Captain"), ("🛡️", "Membre patché"),
        ("🔥", "Responsable"), ("👊", "Membre prospect"),
        ("🔰", "Nomade"),
    ],
    "gang_ecole": [
        ("👑", "Président du conseil"), ("👑", "Vice-président"),
        ("⚔️", "Capitaine d'équipe"), ("🏛️", "Délégué principal"),
        ("📋", "Délégué"), ("🛡️", "Responsable"),
        ("🔥", "Chef de section"), ("👊", "Membre d'élite"),
        ("👊", "Membre"), ("🔰", "Élève"),
    ],
    "gang_mineur": [
        ("👑", "Chef"), ("⚔️", "Bras droit"),
        ("🏛️", "Cadre"), ("📋", "Responsable"),
        ("⚔️", "Capitaine"), ("🛡️", "Officier"),
        ("🔥", "Chef d'équipe"), ("👊", "Membre d'élite"),
        ("👊", "Membre"), ("🔰", "Recrue"),
    ],
}

MOTS_CLES = {
    "gang_urbain": ["rue", "quartier", "urbain", "cité", "banlieue",
                    "territoire", "turf"],
    "gang_yakuza": ["yakuza", "mafia", "syndicat", "clan", "famille",
                    "oyabun", "kumicho"],
    "gang_militaire": ["militaire", "armée", "soldat", "général",
                       "régiment", "bataillon", "escadron"],
    "gang_biker": ["moto", "biker", "route", "club", "chapitre", "patché"],
    "gang_ecole": ["école", "lycée", "collège", "élève", "conseil",
                   "étudiant", "classe"],
}


def _detecter_style(description: str, nom: str) -> str:
    texte = f"{nom} {description}".lower()
    scores = {style: 0 for style in MOTS_CLES}
    for style, kws in MOTS_CLES.items():
        for kw in kws:
            if kw in texte:
                scores[style] += 1
    meilleur = max(scores, key=scores.get)
    if scores[meilleur] == 0:
        return "gang_urbain"
    return meilleur


def _couleur_depuis_nom(nom: str) -> discord.Color:
    h = hash(nom.lower()) & 0xFFFFFF
    r = (h >> 16) & 0xFF
    g = (h >> 8) & 0xFF
    b = h & 0xFF
    r = max(r, 60)
    g = max(g, 60)
    b = max(b, 60)
    return discord.Color.from_rgb(r, g, b)


def build_custom_role_specs(
    gang_name: str,
    description: str = "",
    prefixer: bool = True,
) -> list[dict]:
    """
    Construit les specs de rôles.
    Si `prefixer` est False, le nom du gang n'apparaît pas dans le nom du rôle.
    """
    style = _detecter_style(description, gang_name)
    hierarchy = HIERARCHIES.get(style, HIERARCHIES["gang_urbain"])
    color = _couleur_depuis_nom(gang_name)
    specs = []
    for emoji, rank in hierarchy:
        if prefixer:
            nom = f"{emoji} {gang_name} {rank}"
        else:
            nom = f"{emoji} {rank}"
        specs.append({
            "name": nom,
            "emoji": emoji,
            "rank": rank,
            "style": style,
            "color": color,
            "permissions": perms_for_rank(rank),
        })
    log.info("Style détecté pour %s : %s (%d rôles)",
             gang_name, style, len(specs))
    return specs


async def generate_custom_gangs(guild: discord.Guild, config: dict):
    from generators.category_generator import create_category
    from generators.channel_generator import create_text, create_voice
    from generators.permission_generator import (
        gang_overwrites, private_overwrites,
    )

    gangs = config.get("gangs") or ["Crimson"]
    description = config.get("description", "")
    theme = config.get("theme_obj", {})

    all_roles = {}

    # Plusieurs gangs : on préfixe pour distinguer
    # Un seul gang : pas de préfixe (plus propre)
    prefixer = len(gangs) > 1

    for gang in gangs:
        specs = build_custom_role_specs(gang, description, prefixer=prefixer)
        if specs:
            c = specs[0]["color"]
            couleur_hex = "#{:06X}".format(c.value)
        else:
            couleur_hex = "#C8102E"

        roles = await create_roles_with_separators(
            guild, specs,
            couleur_base_hex=couleur_hex,
        )
        all_roles[gang] = roles

    info_cat = await create_category(
        guild, theme.get("info_cat", "📁 INFORMATIONS")
    )
    community_cat = await create_category(
        guild, theme.get("community_cat", "📁 COMMUNAUTÉ")
    )
    territories_cat = await create_category(
        guild, theme.get("territories_cat", "📁 TERRITOIRES")
    )
    voice_cat = await create_category(
        guild, theme.get("voice_cat", "🔊 VOCAL")
    )

    await create_text(guild, theme.get("rules_channel", "📜・règlement"), info_cat)
    await create_text(guild, theme.get("announce_channel", "📢・annonces"), info_cat)
    await create_text(guild, theme.get("welcome_channel", "👋・bienvenue"), info_cat)
    await create_text(guild, theme.get("chat_channel", "💬・discussion"), community_cat)
    await create_text(guild, theme.get("media_channel", "📸・médias"), community_cat)
    await create_text(guild, theme.get("bot_channel", "🤖・commandes"), community_cat)

    for t in theme.get("territories", []):
        await create_text(guild, t, territories_cat)

    await create_voice(guild, "🔊・Lobby", voice_cat)

    for gang in gangs:
        gang_roles = all_roles.get(gang, [])
        if not gang_roles:
            continue
        top_role = gang_roles[0]
        ow = gang_overwrites(guild, top_role, guild.default_role)
        cat = await create_category(guild, f"📁 {gang.upper()}", overwrites=ow)
        await create_text(guild, f"💬・{gang.lower()}-chat", cat, ow)
        await create_text(guild, f"📢・{gang.lower()}-annonces", cat, ow)
        await create_text(guild, f"🔒・{gang.lower()}-hq", cat,
                          private_overwrites(guild, gang_roles))
        await create_voice(guild, f"🔊・{gang.lower()}-vocal", cat, ow)

    log.info("Génération custom terminée pour %s (%d gangs, prefixer=%s)",
             guild.name, len(gangs), prefixer)
    return True