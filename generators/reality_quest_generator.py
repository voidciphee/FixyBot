import json
import os
import discord
from config import DATA_DIR
from utils.permissions import perms_for_rank, detecter_groupe, is_chef
from utils.logger import get_logger
from generators.role_generator import create_roles_with_separators
from generators.rp_structure import creer_structure_rp

log = get_logger("reality_quest")
RQ_FILE = os.path.join(DATA_DIR, "reality_quest.json")


def load_rq() -> dict:
    if not os.path.exists(RQ_FILE):
        return {}
    with open(RQ_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _couleur(hex_str: str) -> discord.Color:
    try:
        return discord.Color(int(hex_str.lstrip("#"), 16))
    except Exception:
        return discord.Color.dark_red()


def build_rq_role_specs(gang: str = None) -> list[dict]:
    data = load_rq()
    specs = []
    seen = set()

    def ajouter(emoji, role, canon, couleur):
        nom = f"{emoji} {role}".strip()
        if nom in seen:
            return
        seen.add(nom)
        specs.append({
            "name": nom, "emoji": emoji, "rank": role, "canon": canon,
            "color": couleur, "permissions": perms_for_rank(role),
        })

    orgs = data.get("organisations", {})

    if gang:
        if gang in orgs:
            orgs = {gang: orgs[gang]}
        else:
            gl = gang.lower()
            orgs = {k: v for k, v in orgs.items() if k.lower() == gl}
            if not orgs:
                log.warning("Aucune organisation trouvée pour %s", gang)
                return []

    for org_nom, org_data in orgs.items():
        c = _couleur(org_data.get("couleur", "#C8102E"))
        for h in org_data.get("hierarchie", []):
            ajouter(h["emoji"], h["role"], h.get("canon", False), c)

    return specs


async def generate_reality_quest(
    guild: discord.Guild,
    gang: str = None,
    all_salons: bool = False,
):
    specs = build_rq_role_specs(gang=gang)
    if not specs:
        log.warning("Aucun rôle pour Reality Quest (gang=%s)", gang)
        return True

    total_actuel = len(guild.roles)
    max_nouveaux = max(0, 240 - total_actuel)
    if len(specs) > max_nouveaux:
        specs = specs[:max_nouveaux]

    roles_crees = await create_roles_with_separators(
        guild, specs, couleur_base_hex="#C8102E",
    )

    # Classer les rôles créés par niveau
    role_membres = [r for r in roles_crees if not is_chef(r.name) and
                    detecter_groupe(r.name) == "MEMBRES"]
    role_haut = [r for r in roles_crees if
                 detecter_groupe(r.name) == "HAUTS GRADÉS"]
    role_dir = [r for r in roles_crees if is_chef(r.name) or
                detecter_groupe(r.name) == "DIRECTION"]

    # Structure RP complète
    if gang:
        await creer_structure_rp(
            guild, role_membres, role_haut, role_dir,
        )

    log.info("Reality Quest terminé pour %s (gang=%s)", guild.name, gang)
    return True


async def create_character_role(guild: discord.Guild, nom_personnage: str):
    if len(guild.roles) >= 249:
        raise RuntimeError("Limite de rôles atteinte (250).")
    return await guild.create_role(
        name=f"👤 {nom_personnage}",
        colour=discord.Color.from_rgb(255, 215, 0),
        permissions=discord.Permissions.none(),
        mentionable=False,
        reason="Rôle de personnage Reality Quest (admin)",
    )