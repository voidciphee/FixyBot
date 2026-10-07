import discord


class FixyConfirmView(discord.ui.View):
    def __init__(self, auteur_id: int, on_confirm, on_cancel=None):
        super().__init__(timeout=300)
        self.auteur_id = auteur_id
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

    async def interaction_check(self, it: discord.Interaction) -> bool:
        return it.user.id == self.auteur_id

    @discord.ui.button(label="Confirmer", emoji="✅",
                       style=discord.ButtonStyle.success)
    async def confirmer(self, it: discord.Interaction, _):
        await it.response.defer(ephemeral=True)
        await self.on_confirm(it)

    @discord.ui.button(label="Annuler", emoji="❌",
                       style=discord.ButtonStyle.danger)
    async def annuler(self, it: discord.Interaction, _):
        if self.on_cancel:
            await self.on_cancel(it)
        else:
            try:
                await it.response.edit_message(
                    content="❌ Annulé.", view=None, embed=None,
                )
            except discord.HTTPException:
                pass