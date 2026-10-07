import discord
from discord import app_commands
from generators.reality_quest_generator import create_character_role as rq_role
from generators.tokyo_revengers_generator import create_character_role as tr_role
from generators.wind_breaker_generator import create_character_role as wb_role


def setup(bot: discord.Client):
    @bot.tree.command(
        name="character_role",
        description="[ADMIN] Crée un rôle de personnage selon l'univers",
    )
    @app_commands.describe(
        nom="Nom exact du personnage",
        univers="reality_quest | tokyo_revengers | wind_breaker",
    )
    @app_commands.choices(univers=[
        app_commands.Choice(name="Reality Quest", value="reality_quest"),
        app_commands.Choice(name="Tokyo Revengers", value="tokyo_revengers"),
        app_commands.Choice(name="Wind Breaker", value="wind_breaker"),
    ])
    async def character_role(interaction: discord.Interaction, nom: str,
                             univers: app_commands.Choice[str]):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Réservé aux administrateurs.", ephemeral=True
            )
            return
        if univers.value == "reality_quest":
            role = await rq_role(interaction.guild, nom)
        elif univers.value == "tokyo_revengers":
            role = await tr_role(interaction.guild, nom)
        else:
            role = await wb_role(interaction.guild, nom)
        await interaction.response.send_message(
            f"✅ Rôle de personnage créé : {role.mention}", ephemeral=True
        )