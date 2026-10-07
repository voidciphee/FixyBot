import discord
from utils.permissions import (
    perms_for_rank, couleur_par_importance, detecter_groupe, is_chef
)
from utils.logger import get_logger

log = get_logger("role_generator")


async def create_roles_with_separators(
    guild: discord.Guild,
    specs: list[dict],
    couleur_base_hex: str = "#C8102E",
    emoji_sep: str = "━━━━━━━━━━",
) -> list[discord.Role]:
    crees: list[discord.Role] = []

    groupes: dict[str, list[dict]] = {
        "DIRECTION": [], "HAUTS GRADÉS": [], "MEMBRES": []
    }
    for spec in specs:
        g = detecter_groupe(spec["rank"])
        groupes[g].append(spec)

    ordre = ["DIRECTION", "HAUTS GRADÉS", "MEMBRES"]
    emoji_map = {
        "DIRECTION": "👑",
        "HAUTS GRADÉS": "⚔️",
        "MEMBRES": "🛡️",
    }

    for groupe in ordre:
        liste = groupes[groupe]
        if not liste:
            continue

        sep_name = f"{emoji_sep} {emoji_map[groupe]} {groupe} {emoji_sep}"
        sep = discord.utils.get(guild.roles, name=sep_name)
        if not sep:
            try:
                sep = await guild.create_role(
                    name=sep_name,
                    colour=discord.Color.darker_grey(),
                    permissions=discord.Permissions.none(),
                    mentionable=False,
                    hoist=False,
                    reason="Séparateur de groupe de grade",
                )
            except discord.HTTPException as e:
                log.error("Séparateur %s : %s", sep_name, e)
                sep = None
        if sep:
            crees.append(sep)

        for spec in liste:
            ex = discord.utils.get(guild.roles, name=spec["name"])
            if ex:
                crees.append(ex)
                continue

            if len(guild.roles) >= 245:
                log.warning("Limite Discord approchée, arrêt.")
                return crees

            # Couleur sûre (bornée à 0..255 par composante)
            couleur = couleur_par_importance(spec["rank"], couleur_base_hex)

            # Chef → Administrateur
            if is_chef(spec["rank"]):
                permissions = discord.Permissions(administrator=True)
            else:
                permissions = spec.get(
                    "permissions", perms_for_rank(spec["rank"])
                )

            try:
                role = await guild.create_role(
                    name=spec["name"],
                    colour=couleur,
                    permissions=permissions,
                    mentionable=False,
                    hoist=True,
                    reason="Générateur de gang",
                )
                crees.append(role)
            except discord.HTTPException as e:
                log.error("Rôle %s : %s", spec["name"], e)
                # ⭐ On continue au lieu de planter
                continue

    return crees


async def reorder_roles(guild: discord.Guild, ordered_roles: list[discord.Role]):
    positions = {r: len(ordered_roles) - i for i, r in enumerate(ordered_roles)}
    try:
        await guild.edit_role_positions(positions=positions)
    except discord.Forbidden:
        log.warning("Impossible de réordonner les rôles (permissions).")
    except discord.HTTPException as e:
        log.warning("Erreur réordonnancement : %s", e)