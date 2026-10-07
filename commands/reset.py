import asyncio
import discord
from utils.validators import est_autorise

# Salons Discord par défaut qu'on NE supprime PAS
SALONS_PROTEGES = {
    "general", "général", "general 1", "général 1",
    "text channels", "salons textuels",
    "voice channels", "salons vocaux",
    "règles", "rules", "bienvenue", "welcome",
}

# Rôles Discord par défaut qu'on NE supprime PAS
ROLES_PROTEGES = {
    "@everyone", "everyone",
}


async def _supprimer(obj, sem: asyncio.Semaphore, compteur: dict):
    async with sem:
        try:
            await obj.delete(reason="Reset")
            compteur["total"] += 1
        except (discord.NotFound, discord.HTTPException, discord.Forbidden):
            pass


def _salon_a_supprimer(channel, salon_courant_id: int) -> bool:
    if channel.id == salon_courant_id:
        return False
    if channel.name.lower().strip() in SALONS_PROTEGES:
        return False
    return True


def _role_a_supprimer(role: discord.Role) -> bool:
    if role.is_default():
        return False
    if role.managed:
        return False
    if role.name.lower() in ROLES_PROTEGES:
        return False
    return True


class ResetConfirm(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=60)
        self.author_id = author_id

    async def interaction_check(self, it: discord.Interaction) -> bool:
        return it.user.id == self.author_id

    @discord.ui.button(label="Confirmer", style=discord.ButtonStyle.danger)
    async def yes(self, it: discord.Interaction, _):
        await it.response.defer(ephemeral=True)

        guild = it.guild
        salon_courant = it.channel.id if it.channel else 0
        compteur = {"total": 0}

        # 1. Sélection des salons
        salons = [
            c for c in guild.channels
            if _salon_a_supprimer(c, salon_courant)
            and not isinstance(c, discord.CategoryChannel)
        ]
        cats = [
            c for c in guild.channels
            if _salon_a_supprimer(c, salon_courant)
            and isinstance(c, discord.CategoryChannel)
        ]

        # 2. Sélection des rôles
        me = guild.me
        roles = [
            r for r in guild.roles
            if _role_a_supprimer(r)
            and r < me.top_role
        ]

        # 3. Suppression parallèle
        sem = asyncio.Semaphore(5)

        await asyncio.gather(*[_supprimer(c, sem, compteur) for c in salons])
        await asyncio.gather(*[_supprimer(c, sem, compteur) for c in cats])
        await asyncio.gather(*[_supprimer(r, sem, compteur) for r in roles])

        # 4. Notification
        try:
            await it.followup.send(
                f"✅ Reset terminé. {compteur['total']} éléments supprimés.",
                ephemeral=True,
            )
        except (discord.HTTPException, discord.NotFound):
            try:
                await it.user.send(
                    f"✅ Reset terminé sur **{guild.name}**. "
                    f"{compteur['total']} éléments supprimés."
                )
            except discord.HTTPException:
                pass

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.secondary)
    async def no(self, it: discord.Interaction, _):
        await it.response.edit_message(content="Annulé.", view=None)


def setup(bot: discord.Client):
    @bot.tree.command(
        name="reset",
        description="Supprime TOUS les rôles et salons créés par le bot",
    )
    async def reset_cmd(interaction: discord.Interaction):
        # Vérification de l'autorisation (serveur protégé)
        if not est_autorise(interaction):
            await interaction.response.send_message(
                "❌ Tu n'as pas la permission d'utiliser `/reset` sur ce serveur.",
                ephemeral=True,
            )
            return

        # Vérification admin normale
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Réservé aux administrateurs.", ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "⚠️ Confirmer le reset ? **Tous** les rôles et salons créés par le bot "
            "seront supprimés, sauf les salons protégés (`general`, `règles`, etc.) "
            "et le salon courant.",
            view=ResetConfirm(interaction.user.id),
            ephemeral=True,
        )