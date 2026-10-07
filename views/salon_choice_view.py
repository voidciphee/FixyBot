import discord


class SalonChoiceView(discord.ui.View):
    """Demande à l'utilisateur : tous les salons de l'univers ou seulement le gang ?"""

    def __init__(self, state: dict):
        super().__init__(timeout=600)
        self.state = state

    @discord.ui.button(label="Oui, tous les salons de l'univers",
                       emoji="✅", style=discord.ButtonStyle.success)
    async def yes(self, it: discord.Interaction, _):
        self.state["all_salons"] = True
        await self._next(it)

    @discord.ui.button(label="Non, seulement ce gang",
                       emoji="❌", style=discord.ButtonStyle.danger)
    async def no(self, it: discord.Interaction, _):
        self.state["all_salons"] = False
        await self._next(it)

    async def _next(self, it: discord.Interaction):
        gang = self.state.get("gang", "—")
        mode = ("tous les salons de l'univers"
                if self.state["all_salons"]
                else f"uniquement les salons de **{gang}**")
        await it.response.edit_message(
            content=(
                f"✅ Choix enregistré : {mode}\n\n"
                "Choisis maintenant un thème visuel :"
            ),
            view=self._theme_view(),
        )

    def _theme_view(self):
        from views.theme_select_view import ThemeSelectView
        return ThemeSelectView(self.state)