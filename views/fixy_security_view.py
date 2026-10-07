import discord


class FixySecurityView(discord.ui.View):
    def __init__(self, auteur_id: int):
        super().__init__(timeout=300)
        self.auteur_id = auteur_id

    async def interaction_check(self, it: discord.Interaction) -> bool:
        return it.user.id == self.auteur_id

    @discord.ui.button(label="Niveau de vérification", emoji="🔒",
                       style=discord.ButtonStyle.primary, row=0)
    async def verif(self, it: discord.Interaction, _):
        try:
            await it.guild.edit(
                verification_level=discord.VerificationLevel.medium,
                reason="FixyBot sécurité",
            )
            await it.response.send_message(
                "✅ Niveau de vérification → **Moyen**.", ephemeral=True,
            )
        except discord.HTTPException as e:
            await it.response.send_message(f"❌ {e}", ephemeral=True)

    @discord.ui.button(label="Activer 2FA modérateurs", emoji="🔑",
                       style=discord.ButtonStyle.primary, row=0)
    async def twofa(self, it: discord.Interaction, _):
        try:
            await it.guild.edit(
                mfa_level=discord.MFALevel.require_2fa,
                reason="FixyBot sécurité",
            )
            await it.response.send_message(
                "✅ 2FA requis pour les modérateurs.", ephemeral=True,
            )
        except discord.HTTPException as e:
            await it.response.send_message(f"❌ {e}", ephemeral=True)

    @discord.ui.button(label="Créer salon logs", emoji="📜",
                       style=discord.ButtonStyle.success, row=1)
    async def logs(self, it: discord.Interaction, _):
        try:
            cat = discord.utils.get(it.guild.categories,
                                    name="📁 INFORMATIONS")
            if not cat:
                cat = await it.guild.create_category("📁 INFORMATIONS")
            if not discord.utils.get(it.guild.text_channels, name="📜・logs"):
                await it.guild.create_text_channel(
                    "📜・logs", category=cat,
                    reason="FixyBot sécurité",
                )
            await it.response.send_message(
                "✅ Salon `#logs` créé.", ephemeral=True,
            )
        except discord.HTTPException as e:
            await it.response.send_message(f"❌ {e}", ephemeral=True)

    @discord.ui.button(label="Analyser la sécurité", emoji="🔍",
                       style=discord.ButtonStyle.secondary, row=1)
    async def analyser(self, it: discord.Interaction, _):
        from views.fixy_analyze_view import FixyAnalyzeView
        v = FixyAnalyzeView(it.user.id)
        await v.run(it)