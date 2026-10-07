import discord


class FixyMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)

    # ─── 🧩 Templates ───
    @discord.ui.button(label="Templates", emoji="🧩",
                       style=discord.ButtonStyle.secondary, row=0)
    async def templates(self, it: discord.Interaction, _):
        from views.fixy_templates_view import FixyTemplatesView
        await it.response.send_message(
            "🧩 Gestion des templates :",
            view=FixyTemplatesView(it.user.id),
            ephemeral=True,
        )

    # ─── 🛡️ Sécurité ───
    @discord.ui.button(label="Sécurité", emoji="🛡️",
                       style=discord.ButtonStyle.secondary, row=0)
    async def securite(self, it: discord.Interaction, _):
        from views.fixy_security_view import FixySecurityView
        await it.response.send_message(
            "🛡️ Configuration de la sécurité :",
            view=FixySecurityView(it.user.id),
            ephemeral=True,
        )

    # ─── 🔍 Vérifier mon serveur ───
    @discord.ui.button(label="Vérifier mon serveur", emoji="🔍",
                       style=discord.ButtonStyle.secondary, row=1)
    async def analyser(self, it: discord.Interaction, _):
        from views.fixy_analyze_view import FixyAnalyzeView
        view = FixyAnalyzeView(it.user.id)
        await view.run(it)

    # ─── ⚙️ Configuration ───
    @discord.ui.button(label="Configuration", emoji="⚙️",
                       style=discord.ButtonStyle.secondary, row=1)
    async def config(self, it: discord.Interaction, _):
        embed = discord.Embed(
            title="⚙️ Configuration FixyBot",
            description=(
                "**Commandes disponibles :**\n"
                "• `/setup` — Créer un serveur (communautaire / univers / template)\n"
                "• `/reset` — Supprimer les rôles/salons du bot\n"
                "• `/character_role` — Créer un rôle de personnage\n"
                "• `/fixy` — Ce menu (gestion)\n"
            ),
            color=discord.Color.blurple(),
        )
        await it.response.send_message(embed=embed, ephemeral=True)