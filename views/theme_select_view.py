
import discord
from themes.registry import theme_choices


class ThemeSelectView(discord.ui.View):
    def __init__(self, state: dict):
        super().__init__(timeout=600)
        self.state = state

        options = [
            discord.SelectOption(label=label, value=key)
            for key, label in theme_choices()
        ]
        select = discord.ui.Select(placeholder="Choisis un thème",
                                   options=options)
        select.callback = self.pick
        self.add_item(select)

    async def pick(self, it: discord.Interaction):
        value = it.data["values"][0]
        self.state["theme"] = value
        from views.gang_view import GangView
        await it.response.edit_message(
            content=(
                "🏴 Clique sur **Configurer les gangs** pour définir les noms, "
                "puis **Confirmer** pour la prévisualisation."
            ),
            view=GangView(self.state),
        )