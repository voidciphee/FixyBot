import discord
from utils.database import load_universe


class GangPickerView(discord.ui.View):
    """Vue qui affiche les gangs d'un univers et laisse l'utilisateur en choisir un."""

    def __init__(self, state: dict, universe_key: str):
        super().__init__(timeout=600)
        self.state = state
        self.universe_key = universe_key

        data = load_universe(universe_key)
        gangs = list(data.get("organisations", {}).keys())

        if not gangs:
            gangs = ["Aucun gang disponible"]

        options = [
            discord.SelectOption(label=g[:100], value=g)
            for g in gangs[:25]
        ]
        select = discord.ui.Select(
            placeholder="Choisis un gang / groupe",
            options=options,
        )
        select.callback = self.pick
        self.add_item(select)

        back = discord.ui.Button(
            label="Retour", emoji="⬅️",
            style=discord.ButtonStyle.secondary,
        )
        back.callback = self.back
        self.add_item(back)

    async def pick(self, interaction: discord.Interaction):
        gang = interaction.data["values"][0]
        self.state["gang"] = gang
        self.state["universe"] = self.universe_key

        from views.salon_choice_view import SalonChoiceView
        await interaction.response.edit_message(
            content=(
                f"🌍 Univers : **{self.universe_key}**\n"
                f"🏴 Gang : **{gang}**\n\n"
                "❓ Veux-tu créer **tous les salons de cet univers** ?\n"
                "(Si non, seuls les salons du gang sélectionné seront créés.)"
            ),
            view=SalonChoiceView(self.state),
        )

    async def back(self, interaction: discord.Interaction):
        from views.setup_view import UniverseSelectView
        await interaction.response.edit_message(
            content="Choisis un univers :",
            view=UniverseSelectView(self.state),
        )