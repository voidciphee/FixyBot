import discord
from utils.permissions import detecter_groupe


# Structure RP commune à tous les gangs
RP_STRUCTURE = {
    "📌 INFORMATIONS": {
        "salons": [
            "📜・règlement", "📢・annonces", "📖・présentation-du-gang",
            "📜・histoire-du-gang", "📋・grades-et-hiérarchie",
            "📅・événements", "📢・actualités",
        ],
        "niveau": "public",
    },
    "💬 COMMUNAUTÉ": {
        "salons": [
            "💬・général", "💬・discussion-rp", "🎭・hors-rp",
            "📸・photos", "🎵・musiques", "😂・memes",
        ],
        "niveau": "public",
    },
    "🏴 QUARTIER DU GANG": {
        "salons": [
            "🏙️・quartier-général", "🏠・base-du-gang", "🚪・entrée",
            "🛋️・salle-commune", "📦・stockage", "🗺️・territoire",
            "📍・points-de-rendez-vous",
        ],
        "niveau": "membre",
    },
    "⚔️ ACTIVITÉS RP": {
        "salons": [
            "⚔️・missions", "🥊・combats", "🚨・interventions",
            "🏍️・sorties", "🎯・objectifs", "🗺️・opérations",
            "📋・rapports-de-mission",
        ],
        "niveau": "membre",
    },
    "👑 DIRECTION": {
        "salons": [
            "👑・conseil-du-chef", "📋・réunions", "📜・décisions",
            "🗂️・gestion-du-gang", "📊・rapports", "🔐・archives",
        ],
        "niveau": "direction",
    },
    "🕵️ TRAHISONS / SÉCURITÉ": {
        "salons": [
            "🚨・signalements", "🕵️・surveillance", "⚠️・suspects",
            "🔒・dossiers-confidentiels", "📂・dossiers-des-traitres",
            "⚖️・jugements", "📋・rapports-de-trahison", "🔎・enquêtes",
        ],
        "niveau": "direction",
    },
    "🤝 ALLIANCES / CONFLITS": {
        "salons": [
            "🤝・alliances", "🕊️・diplomatie", "⚔️・guerres",
            "🚨・conflits", "📜・traités", "📋・accords",
            "🗺️・territoires",
        ],
        "niveau": "haut",
    },
    "🎫 RECRUTEMENT": {
        "salons": [
            "🎫・recrutement", "📝・candidatures",
            "🔎・candidatures-en-cours", "✅・candidatures-acceptées",
            "❌・candidatures-refusées", "📋・tests",
            "🎖️・nouveaux-membres",
        ],
        "niveau": "membre",
    },
}

# Salons vocaux RP
RP_VOCAUX = [
    "🔊・Quartier général",
    "🔊・Salle de réunion",
    "🔊・Conseil",
    "🔊・Patrouille",
    "🔊・Mission",
    "🔊・Combat",
    "🔊・Discussion",
    "🔊・Détente",
]


def _overwrites_public(guild: discord.Guild):
    return {
        guild.default_role: discord.PermissionOverwrite(
            view_channel=True, send_messages=True, read_message_history=True,
            connect=True, speak=True,
        ),
    }


def _overwrites_membre(guild: discord.Guild, roles_membres: list[discord.Role]):
    ow = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
    }
    for r in roles_membres:
        ow[r] = discord.PermissionOverwrite(
            view_channel=True, send_messages=True, read_message_history=True,
            connect=True, speak=True,
        )
    return ow


def _overwrites_haut(guild: discord.Guild, roles_haut: list[discord.Role],
                     roles_membres: list[discord.Role]):
    ow = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
    }
    for r in roles_membres + roles_haut:
        ow[r] = discord.PermissionOverwrite(
            view_channel=True, send_messages=True, read_message_history=True,
            connect=True, speak=True,
        )
    return ow


def _overwrites_direction(guild: discord.Guild, roles_dir: list[discord.Role]):
    ow = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
    }
    for r in roles_dir:
        ow[r] = discord.PermissionOverwrite(
            view_channel=True, send_messages=True, read_message_history=True,
            connect=True, speak=True,
        )
    return ow


async def creer_structure_rp(
    guild: discord.Guild,
    role_membres: list[discord.Role],
    role_haut: list[discord.Role],
    role_dir: list[discord.Role],
):
    """Crée la structure RP complète (catégories + salons + vocaux)."""

    for nom_cat, data in RP_STRUCTURE.items():
        niveau = data["niveau"]

        if niveau == "public":
            ow = _overwrites_public(guild)
        elif niveau == "membre":
            ow = _overwrites_membre(guild, role_membres)
        elif niveau == "haut":
            ow = _overwrites_haut(guild, role_haut, role_membres)
        else:  # direction
            ow = _overwrites_direction(guild, role_dir)

        # Crée la catégorie
        cat = discord.utils.get(guild.categories, name=nom_cat)
        if not cat:
            try:
                cat = await guild.create_category(
                    name=nom_cat, overwrites=ow,
                    reason="Générateur RP",
                )
            except discord.HTTPException:
                continue

        # Crée les salons textuels
        for salon_nom in data["salons"]:
            if discord.utils.get(guild.text_channels, name=salon_nom):
                continue
            try:
                await guild.create_text_channel(
                    name=salon_nom, category=cat, overwrites=ow,
                    reason="Générateur RP",
                )
            except discord.HTTPException:
                break

    # Crée les salons vocaux
    cat_vocal = discord.utils.get(guild.categories, name="🔊 VOCAUX RP")
    if not cat_vocal:
        try:
            cat_vocal = await guild.create_category(
                name="🔊 VOCAUX RP", reason="Générateur RP",
            )
        except discord.HTTPException:
            cat_vocal = None

    if cat_vocal:
        ow_vocal = _overwrites_membre(guild, role_membres)
        for nom_vocal in RP_VOCAUX:
            if discord.utils.get(guild.voice_channels, name=nom_vocal):
                continue
            try:
                await guild.create_voice_channel(
                    name=nom_vocal, category=cat_vocal, overwrites=ow_vocal,
                    reason="Générateur RP",
                )
            except discord.HTTPException:
                break