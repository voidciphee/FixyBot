import discord
from utils.logger import get_logger

log = get_logger("fixy_analyzer")


async def analyser_serveur(guild: discord.Guild) -> dict:
    rapport = {
        "roles": [],
        "salons": [],
        "permissions": [],
        "securite": [],
        "organisation": [],
        "score_roles": "🟢",
        "score_salons": "🟢",
        "score_permissions": "🟢",
        "score_securite": "🟢",
        "score_organisation": "🟢",
        "problemes": [],
        "suggestions": [],
        "corrections": [],
    }

    await _analyser_roles(guild, rapport)
    await _analyser_salons(guild, rapport)
    await _analyser_permissions(guild, rapport)
    await _analyser_securite(guild, rapport)
    await _analyser_organisation(guild, rapport)

    return rapport


async def _analyser_roles(guild, r):
    sans_couleur = [
        role for role in guild.roles
        if role.colour.value == 0 and not role.is_default() and not role.managed
    ]
    if sans_couleur:
        r["problemes"].append(
            f"🟡 {len(sans_couleur)} rôle(s) sans couleur : "
            + ", ".join(role.name for role in sans_couleur[:5])
        )
        r["suggestions"].append(
            "Ajouter une couleur distincte aux rôles sans couleur."
        )
        r["corrections"].append({
            "type": "role_couleur",
            "cibles": [role.id for role in sans_couleur[:10]],
        })
        r["score_roles"] = "🟡"

    noms = {}
    for role in guild.roles:
        key = role.name.lower().strip()
        noms.setdefault(key, []).append(role)
    doublons = {k: v for k, v in noms.items() if len(v) > 1}
    if doublons:
        r["problemes"].append(
            f"🟡 {len(doublons)} nom(s) de rôle en doublon."
        )
        r["score_roles"] = "🟡"


async def _analyser_salons(guild, r):
    sans_cat = [
        c for c in guild.channels
        if c.category is None and not isinstance(c, discord.CategoryChannel)
    ]
    if sans_cat:
        r["problemes"].append(
            f"🟡 {len(sans_cat)} salon(s) sans catégorie."
        )
        r["suggestions"].append(
            "Classer les salons sans catégorie dans des catégories logiques."
        )
        r["score_salons"] = "🟡"

    cats_vides = [c for c in guild.categories if not c.channels]
    if cats_vides:
        r["problemes"].append(f"🟡 {len(cats_vides)} catégorie(s) vide(s).")
        r["score_salons"] = "🟡"


async def _analyser_permissions(guild, r):
    admins = [role for role in guild.roles if role.permissions.administrator]
    if len(admins) > 3:
        r["problemes"].append(
            f"🔴 {len(admins)} rôles ont la permission Administrateur "
            f"(recommandé : 2-3 max)."
        )
        r["score_permissions"] = "🔴"

    for role in admins:
        if role.is_default() or role.managed:
            continue
        if role.name.lower() in ("membre", "member", "invité", "guest"):
            r["problemes"].append(
                f"🔴 Le rôle **{role.name}** a la permission Administrateur "
                f"alors qu'il ne devrait pas."
            )
            r["corrections"].append({
                "type": "retirer_admin",
                "role_id": role.id,
            })


async def _analyser_securite(guild, r):
    a_logs = any("log" in c.name.lower() for c in guild.text_channels)
    if not a_logs:
        r["problemes"].append("🟡 Aucun salon de logs détecté.")
        r["suggestions"].append(
            "Ajouter un salon de logs et activer l'audit."
        )
        r["score_securite"] = "🟡"

    a_auto_mod = guild.verification_level != discord.VerificationLevel.none
    if not a_auto_mod:
        r["problemes"].append("🟡 Niveau de vérification du serveur trop bas.")
        r["score_securite"] = "🟡"


async def _analyser_organisation(guild, r):
    if len(guild.categories) < 3:
        r["problemes"].append(
            "🟡 Peu de catégories : serveur peu organisé."
        )
        r["score_organisation"] = "🟡"

    total_salons = len(guild.text_channels) + len(guild.voice_channels)
    if total_salons > 100 and len(guild.categories) < 5:
        r["problemes"].append(
            f"🟡 {total_salons} salons pour {len(guild.categories)} catégories : "
            "répartition déséquilibrée."
        )
        r["score_organisation"] = "🟡"