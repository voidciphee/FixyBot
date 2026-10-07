import discord
from views.preview_view import PreviewView
from themes.registry import get_theme


class GangView(discord.ui.View):
    def __init__(self, state: dict):
        super().__init__(timeout=600)
        self.state = state

        # Si on est en mode univers existant, on n'affiche PAS
        # le bouton "Configurer les gangs".
        universe = state.get("universe")
        if not universe:
            self.add_item(self.configure)
        self.add_item(self.retour)
        self.add_item(self.confirm)

    # ── Bouton "Configurer les gangs" (mode custom uniquement) ──
    @discord.ui.button(
        label="Configurer les gangs", emoji="🏴",
        style=discord.ButtonStyle.primary,
    )
    async def configure(self, it: discord.Interaction, _):
        await it.response.send_modal(GangModal(self.state))

    # ── Bouton "Retour" ──
    @discord.ui.button(
        label="Retour", emoji="⬅️",
        style=discord.ButtonStyle.secondary,
    )
    async def retour(self, it: discord.Interaction, _):
        from views.setup_view import MainMenuView
        await it.response.edit_message(
            content="🏯 Menu principal :",
            embed=None,
            view=MainMenuView(self.state),
        )

    # ── Bouton "Confirmer" ──
    @discord.ui.button(
        label="Confirmer", emoji="✅",
        style=discord.ButtonStyle.success,
    )
    async def confirm(self, it: discord.Interaction, _):
        universe = self.state.get("universe")
        gang = self.state.get("gang")

        if universe and gang:
            gangs = [gang]
        else:
            gangs = self.state.get("gangs") or ["Crimson"]

        self.state["gangs"] = gangs

        theme_key = self.state.get("theme", "urban")
        theme = get_theme(theme_key)

        cfg = {
            "server_name": self.state.get("server_name", it.guild.name),
            "gangs": gangs,
            "gang": gang,
            "description": self.state.get("description", ""),
            "theme": theme_key,
            "color": theme["color"],
            "universe": universe,
            "theme_obj": theme,
            "all_salons": self.state.get("all_salons", False),
        }

        embed = discord.Embed(title="🏯 SERVER GENERATOR", color=theme["color"])
        embed.add_field(name="Serveur", value=cfg["server_name"], inline=False)
        embed.add_field(name="Mode", value=self.state.get("mode", "Custom Gang"), inline=True)
        embed.add_field(name="Univers", value=universe or "—", inline=True)
        embed.add_field(name="Gang", value=gang or "—", inline=True)
        embed.add_field(name="Thème", value=theme["label"], inline=True)
        embed.add_field(name="Gangs à générer", value=str(len(gangs)), inline=True)

        await it.response.edit_message(
            embed=embed, content=None,
            view=PreviewView(cfg, it.user.id),
        )


class GangModal(discord.ui.Modal, title="Configuration des gangs"):
    def __init__(self, state: dict):
        super().__init__()
        self.state = state
        self.gangs_input = discord.ui.TextInput(
            label="Noms des gangs (séparés par des virgules)",
            placeholder="Crimson, Vipers, Ravens",
            default=", ".join(state.get("gangs", ["Crimson"])),
            max_length=200,
        )
        self.desc_input = discord.ui.TextInput(
            label="Description / contexte",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=500,
            default=state.get("description", ""),
        )
        self.add_item(self.gangs_input)
        self.add_item(self.desc_input)

    async def on_submit(self, interaction: discord.Interaction):
        raw = self.gangs_input.value or "Crimson"
        gangs = [g.strip() for g in raw.split(",") if g.strip()]
        self.state["gangs"] = gangs or ["Crimson"]
        self.state["description"] = self.desc_input.value or ""
        await interaction.response.send_message(
            f"✅ Gangs enregistrés : {', '.join(self.state['gangs'])}",
            ephemeral=True,
        )