import discord
from fixy.ai_parser import build_plan
from views.fixy_confirm_view import FixyConfirmView
from utils.logger import get_logger

log = get_logger("fixy_ai_view")


class FixyAIModal(discord.ui.Modal, title="🧠 Configuration libre"):
    requete = discord.ui.TextInput(
        label="Décris ce que tu veux",
        placeholder=(
            "Ex: serveur RP Tokyo Revengers avec Tokyo Manji Gang, "
            "salons missions, traîtres, alliances, 8 vocaux"
        ),
        style=discord.TextStyle.paragraph,
        max_length=1000,
    )

    def __init__(self, state: dict):
        super().__init__()
        self.state = state

    async def on_submit(self, it: discord.Interaction):
        plan = build_plan(self.requete.value)
        self.state["plan"] = plan

        embed = discord.Embed(
            title="🧠 Analyse de ta demande",
            color=discord.Color.blurple(),
        )
        embed.add_field(
            name="Univers",
            value=(plan["univers"] or "❓ non détecté").replace("_", " ").title(),
            inline=True,
        )
        embed.add_field(name="Gang", value=plan["gang"] or "—", inline=True)
        embed.add_field(name="Type", value=plan["type"].title(), inline=True)
        embed.add_field(
            name="Éléments",
            value=", ".join(plan["elements"]) or "—", inline=False,
        )

        async def on_confirm(inter: discord.Interaction):
            if not plan["univers"]:
                await inter.followup.send(
                    "❌ Aucun univers détecté.", ephemeral=True,
                )
                return
            cfg = {
                "server_name": inter.guild.name,
                "gangs": [plan["gang"]] if plan["gang"] else [],
                "gang": plan["gang"],
                "universe": plan["univers"],
                "theme": "urban",
                "all_salons": False,
                "theme_obj": {},
            }
            try:
                from generators.server_generator import generate
                await generate(inter.guild, cfg)
                await inter.followup.send(
                    "✅ Serveur généré.", ephemeral=True,
                )
            except Exception as e:
                log.exception("Erreur IA")
                await inter.followup.send(f"❌ Erreur : {e}", ephemeral=True)

        await it.response.send_message(
            embed=embed,
            view=FixyConfirmView(it.user.id, on_confirm),
            ephemeral=True,
        )