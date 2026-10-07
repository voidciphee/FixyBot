import discord
from config import SUPPORT_SERVER_INVITE


class SuggestionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label="Rejoindre le serveur",
            emoji="💜",
            style=discord.ButtonStyle.link,
            url=SUPPORT_SERVER_INVITE,
        ))