import discord
from views.fixy_menu_view import FixyMenuView
from utils.logger import get_logger

log = get_logger("commands.fixy")


def setup(bot: discord.Client):
    log.info("Enregistrement de la commande /fixy...")

    @bot.tree.command(
        name="fixy",
        description="🧠 FixyBot — Gestion avancée du serveur",
    )
    async def fixy_cmd(interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 FixyBot — Gestion du serveur",
            description=(
                "Gère ton serveur : templates, sécurité, analyse, configuration.\n\n"
                "Pour créer un serveur, utilise **`/setup`**."
            ),
            color=discord.Color.blurple(),
        )
        embed.add_field(name="🧩 Templates", value="Sauvegarder / charger",
                        inline=True)
        embed.add_field(name="🛡️ Sécurité", value="Protections",
                        inline=True)
        embed.add_field(name="🔍 Vérifier", value="Analyse serveur",
                        inline=True)
        embed.add_field(name="⚙️ Configuration", value="Paramètres",
                        inline=True)
        await interaction.response.send_message(
            embed=embed,
            view=FixyMenuView(),
            ephemeral=True,
        )

    log.info("Commande /fixy enregistrée.")