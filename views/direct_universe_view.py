import discord


class DirectUniverseView(discord.ui.View):
    """Pour Action / Romance : génération directe de l'anime."""

    def __init__(self, state: dict, universe_key: str, univers_nom: str):
        super().__init__(timeout=600)
        self.state = state
        self.universe_key = universe_key
        self.univers_nom = univers_nom
        self.state["universe"] = universe_key
        # Pas de gang pour Action / Romance
        self.state.pop("gang", None)
        self.state["all_salons"] = False

    @discord.ui.button(label="Créer ce serveur", emoji="🚀",
                       style=discord.ButtonStyle.success)
    async def creer(self, it: discord.Interaction, _):
        from views.preview_view import PreviewView
        from themes.registry import get_theme

        theme_key = self.state.get("theme", "urban")
        theme = get_theme(theme_key)

        cfg = {
            "server_name": self.state.get("server_name", it.guild.name),
            "gangs": [],
            "gang": None,
            "universe": self.universe_key,
            "theme": theme_key,
            "color": theme["color"],
            "all_salons": False,
            "theme_obj": theme,
        }

        embed = discord.Embed(
            title="🏯 SERVER GENERATOR",
            color=theme["color"],
        )
        embed.add_field(name="Serveur", value=cfg["server_name"], inline=False)
        embed.add_field(name="Univers", value=self.univers_nom, inline=True)
        embed.add_field(name="Type", value="Direct (sans gang)", inline=True)

        await it.response.edit_message(
            embed=embed, content=None,
            view=PreviewView(cfg, it.user.id),
        )

    @discord.ui.button(label="Changer de thème", emoji="🎨",
                       style=discord.ButtonStyle.secondary)
    async def theme(self, it: discord.Interaction, _):
        from views.theme_select_view import ThemeSelectView
        await it.response.edit_message(
            content="Choisis un thème visuel :",
            view=ThemeSelectView(self.state),
        )

    @discord.ui.button(label="Retour", emoji="⬅️",
                       style=discord.ButtonStyle.secondary)
    async def retour(self, it: discord.Interaction, _):
        from views.setup_univers_view import SetupUniversView
        await it.response.edit_message(
            content="Choisis une catégorie d'univers :",
            view=SetupUniversView(self.state),
        )