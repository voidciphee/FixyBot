import discord
from fixy.templates import (
    sauvegarder_template, lister_templates, supprimer_template,
    charger_template,
)


class FixyTemplatesView(discord.ui.View):
    def __init__(self, auteur_id: int):
        super().__init__(timeout=300)
        self.auteur_id = auteur_id

    async def interaction_check(self, it: discord.Interaction) -> bool:
        return it.user.id == self.auteur_id

    @discord.ui.button(label="Sauvegarder", emoji="💾",
                       style=discord.ButtonStyle.success, row=0)
    async def save(self, it: discord.Interaction, _):
        nom = f"template_{it.guild.id}"
        sauvegarder_template(it.guild, nom)
        await it.response.send_message(
            f"✅ Template sauvegardé sous `{nom}`.", ephemeral=True,
        )

    @discord.ui.button(label="Lister", emoji="📂",
                       style=discord.ButtonStyle.secondary, row=0)
    async def lister(self, it: discord.Interaction, _):
        noms = lister_templates()
        txt = "\n".join(f"• `{n}`" for n in noms) if noms else "Aucun template."
        await it.response.send_message(
            f"📂 **Templates disponibles :**\n{txt}", ephemeral=True,
        )

    @discord.ui.button(label="Charger (aperçu)", emoji="📥",
                       style=discord.ButtonStyle.primary, row=1)
    async def charger(self, it: discord.Interaction, _):
        nom = f"template_{it.guild.id}"
        data = charger_template(nom)
        if not data:
            await it.response.send_message(
                f"❌ Aucun template `{nom}` trouvé.", ephemeral=True,
            )
            return
        roles = data.get("roles", [])
        cats = data.get("categories", [])
        await it.response.send_message(
            f"📥 Template `{nom}` :\n"
            f"• {len(roles)} rôles\n"
            f"• {len(cats)} catégories\n\n"
            f"Utilise `/setup` → 🧩 Template pour l'appliquer.",
            ephemeral=True,
        )

    @discord.ui.button(label="Supprimer", emoji="🗑️",
                       style=discord.ButtonStyle.danger, row=1)
    async def supprimer(self, it: discord.Interaction, _):
        nom = f"template_{it.guild.id}"
        ok = supprimer_template(nom)
        await it.response.send_message(
            f"✅ Template `{nom}` supprimé." if ok
            else f"❌ Aucun template `{nom}` trouvé.",
            ephemeral=True,
        )