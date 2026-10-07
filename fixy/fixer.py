import asyncio
import discord
from utils.logger import get_logger

log = get_logger("fixy_fixer")


async def appliquer_corrections(guild: discord.Guild,
                                corrections: list[dict],
                                rapport: dict) -> dict:
    resultat = {"fait": 0, "echecs": 0, "details": []}
    sem = asyncio.Semaphore(5)

    for corr in corrections:
        t = corr.get("type")

        if t == "role_couleur":
            for role_id in corr.get("cibles", []):
                role = guild.get_role(role_id)
                if not role:
                    continue
                try:
                    r_val = (role.id >> 16) & 0xFF or 128
                    g_val = (role.id >> 8) & 0xFF or 128
                    b_val = role.id & 0xFF or 128
                    async with sem:
                        await role.edit(
                            colour=discord.Color.from_rgb(r_val, g_val, b_val),
                            reason="FixyBot correction",
                        )
                    resultat["fait"] += 1
                except discord.HTTPException as e:
                    log.warning("Erreur correction rôle %s : %s", role.name, e)
                    resultat["echecs"] += 1
                    resultat["details"].append(f"❌ {role.name} : {e}")

        elif t == "retirer_admin":
            role = guild.get_role(corr.get("role_id"))
            if not role:
                continue
            try:
                perms = role.permissions
                perms.administrator = False
                async with sem:
                    await role.edit(
                        permissions=perms,
                        reason="FixyBot correction",
                    )
                resultat["fait"] += 1
            except discord.HTTPException as e:
                log.warning("Erreur admin rôle %s : %s", role.name, e)
                resultat["echecs"] += 1
                resultat["details"].append(f"❌ {role.name} : {e}")

    return resultat