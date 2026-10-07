import discord
from views.fixy_confirm_view import FixyConfirmView


class SetupCommunityModal(discord.ui.Modal, title="🏠 Serveur communautaire"):
    nom = discord.ui.TextInput(
        label="Nom du serveur",
        placeholder="Ma super communauté",
        max_length=80,
    )
    description = discord.ui.TextInput(
        label="Description / thème",
        placeholder="Communauté gaming conviviale, discussion, événements...",
        style=discord.TextStyle.paragraph,
        max_length=500,
    )

    def __init__(self, state: dict):
        super().__init__()
        self.state = state

    async def on_submit(self, it: discord.Interaction):
        self.state["server_name"] = self.nom.value
        self.state["description"] = self.description.value

        embed = discord.Embed(
            title="🏠 Serveur communautaire",
            description=f"**{self.nom.value}**",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Description",
                        value=self.description.value[:200], inline=False)
        embed.add_field(name="Contenu prévu",
                        value=(
                            "• ~150 rôles utiles (direction, staff, membres, "
                            "gaming, centres d'intérêt, notifications)\n"
                            "• 6 catégories de salons + support + staff\n"
                            "• 7 salons vocaux\n"
                            "• Permissions adaptées par niveau\n"
                            "• Logs et sécurité"
                        ), inline=False)

        async def on_confirm(inter: discord.Interaction):
            from generators.community_generator import generate_community
            try:
                await generate_community(inter.guild, self.state)
                await inter.followup.send(
                    "✅ Serveur communautaire créé.", ephemeral=True,
                )
            except Exception as e:
                await inter.followup.send(f"❌ Erreur : {e}", ephemeral=True)

        await it.response.send_message(
            embed=embed,
            view=FixyConfirmView(it.user.id, on_confirm),
            ephemeral=True,
        )