import discord
from generators.server_generator import generate
from utils.logger import get_logger

log = get_logger("preview_view")


class PreviewView(discord.ui.View):
    def __init__(self, config: dict, author_id: int):
        super().__init__(timeout=600)
        self.config = config
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ Cette prévisualisation ne t'appartient pas.", ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="CRÉER LE SERVEUR", emoji="🚀",
                       style=discord.ButtonStyle.success)
    async def create(self, interaction: discord.Interaction, _):
        await interaction.response.defer(ephemeral=True)
        try:
            await generate(interaction.guild, self.config)
            await interaction.followup.send(
                "✅ Serveur généré avec succès.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Permission refusée. Vérifie Manage Roles / Manage Channels.",
                ephemeral=True,
            )
        except Exception as e:
            log.exception("Erreur génération")
            try:
                await interaction.followup.send(f"❌ Erreur : {e}", ephemeral=True)
            except discord.HTTPException:
                pass

    @discord.ui.button(label="ANNULER", emoji="❌",
                       style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, _):
        await interaction.response.edit_message(
            content="❌ Annulé.", view=None, embed=None
        )