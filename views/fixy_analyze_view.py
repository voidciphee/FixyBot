import discord
from fixy.analyzer import analyser_serveur
from fixy.fixer import appliquer_corrections
from views.fixy_confirm_view import FixyConfirmView
from utils.logger import get_logger

log = get_logger("fixy_analyze_view")


class FixyAnalyzeView(discord.ui.View):
    def __init__(self, auteur_id: int):
        super().__init__(timeout=300)
        self.auteur_id = auteur_id
        self.rapport = None

    async def interaction_check(self, it: discord.Interaction) -> bool:
        return it.user.id == self.auteur_id

    async def run(self, it: discord.Interaction):
        await it.response.defer(ephemeral=True)
        try:
            rapport = await analyser_serveur(it.guild)
        except Exception as e:
            log.exception("Erreur analyse")
            await it.followup.send(f"❌ Erreur d'analyse : {e}",
                                    ephemeral=True)
            return

        self.rapport = rapport

        embed = discord.Embed(
            title="🔍 Analyse de ton serveur",
            description=f"**{it.guild.name}**",
            color=discord.Color.orange(),
        )
        embed.add_field(name="🏗️ Organisation",
                        value=rapport["score_organisation"], inline=True)
        embed.add_field(name="👑 Rôles",
                        value=rapport["score_roles"], inline=True)
        embed.add_field(name="💬 Salons",
                        value=rapport["score_salons"], inline=True)
        embed.add_field(name="🔐 Permissions",
                        value=rapport["score_permissions"], inline=True)
        embed.add_field(name="🛡️ Sécurité",
                        value=rapport["score_securite"], inline=True)

        if rapport["problemes"]:
            embed.add_field(
                name="⚠️ Problèmes détectés",
                value="\n".join(rapport["problemes"][:10]),
                inline=False,
            )
        else:
            embed.add_field(
                name="✅ Aucun problème détecté",
                value="Ton serveur est bien organisé.",
                inline=False,
            )

        if rapport["suggestions"]:
            embed.add_field(
                name="💡 Suggestions",
                value="\n".join(rapport["suggestions"][:5]),
                inline=False,
            )

        # Réinitialise les boutons
        self.clear_items()

        if rapport["corrections"]:
            self.add_item(_BtnCorriger(rapport))
        else:
            btn = discord.ui.Button(
                label="Rien à corriger", emoji="✅",
                style=discord.ButtonStyle.success, disabled=True,
            )
            self.add_item(btn)

        self.add_item(_BtnDetails(rapport))

        await it.followup.send(embed=embed, view=self, ephemeral=True)


class _BtnCorriger(discord.ui.Button):
    def __init__(self, rapport):
        super().__init__(
            label="🔧 Corriger automatiquement",
            style=discord.ButtonStyle.success,
        )
        self.rapport = rapport

    async def callback(self, it: discord.Interaction):
        corrections = self.rapport["corrections"]
        if not corrections:
            await it.response.send_message(
                "Aucune correction proposée.", ephemeral=True,
            )
            return

        liste = []
        for c in corrections:
            t = c.get("type")
            if t == "role_couleur":
                liste.append(
                    f"• Ajouter une couleur à {len(c['cibles'])} rôle(s)"
                )
            elif t == "retirer_admin":
                role = it.guild.get_role(c.get("role_id"))
                liste.append(
                    f"• Retirer Administrateur du rôle "
                    f"**{role.name if role else '?'}**"
                )
            else:
                liste.append(f"• {t}")

        embed = discord.Embed(
            title="⚠️ Corrections proposées",
            description="\n".join(liste),
            color=discord.Color.yellow(),
        )

        async def on_confirm(inter: discord.Interaction):
            res = await appliquer_corrections(
                inter.guild, corrections, self.rapport,
            )
            try:
                await inter.followup.send(
                    f"✅ {res['fait']} corrections appliquées.\n"
                    f"❌ {res['echecs']} échecs.",
                    ephemeral=True,
                )
            except discord.HTTPException:
                pass

        async def on_cancel(inter: discord.Interaction):
            await inter.response.edit_message(
                content="❌ Corrections annulées.", embed=None, view=None,
            )

        await it.response.send_message(
            embed=embed,
            view=FixyConfirmView(it.user.id, on_confirm, on_cancel),
            ephemeral=True,
        )


class _BtnDetails(discord.ui.Button):
    def __init__(self, rapport):
        super().__init__(
            label="📋 Voir les détails",
            style=discord.ButtonStyle.secondary,
        )
        self.rapport = rapport

    async def callback(self, it: discord.Interaction):
        r = self.rapport
        details = []

        details.append("**Rôles :**")
        details.append("\n".join(r["problemes"][:5]) or "OK")

        details.append("\n**Corrections possibles :**")
        if r["corrections"]:
            for c in r["corrections"]:
                details.append(f"• {c['type']}")
        else:
            details.append("Aucune.")

        texte = "\n".join(details)
        await it.response.send_message(
            f"```{texte[:1900]}```", ephemeral=True,
        )