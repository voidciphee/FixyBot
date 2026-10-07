import discord
from views.setup_view import SetupView
from utils.validators import est_autorise


def setup(bot: discord.Client):
    @bot.tree.command(
        name="setup",
        description="🏯 Gang Server Builder — choisis un anime et génère ton serveur",
    )
    async def setup_cmd(interaction: discord.Interaction):
        # Vérification de l'autorisation (serveur protégé)
        if not est_autorise(interaction):
            await interaction.response.send_message(
                "❌ Tu n'as pas la permission d'utiliser `/setup` sur ce serveur.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title="🏯 GANG SERVER BUILDER",
            description=(
                "Choisis un anime et génère automatiquement ton serveur Discord "
                "avec une structure complète.\n\n"
                "🎌 **Choisir un anime** — parcourir les catégories\n"
                "🔍 **Rechercher un anime** — recherche rapide par nom\n"
                "💡 **Suggestion** — proposer une idée\n"
                "ℹ️ **Informations** — détails du bot"
            ),
            color=discord.Color.dark_red(),
        )
        await interaction.response.send_message(
            embed=embed,
            view=SetupView(),
            ephemeral=True,
        )