import discord
from discord.ext import commands

from config import TOKEN
from commands import setup as setup_cmd
from commands import reset as reset_cmd
from commands import character_role as character_role_cmd
from commands import fixy as fixy_cmd
from utils.logger import get_logger

log = get_logger("main")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        log.info("Connecté en tant que %s | %d commandes synchronisées",
                 bot.user, len(synced))
    except Exception as e:
        log.exception("Erreur de synchronisation : %s", e)


setup_cmd.setup(bot)
reset_cmd.setup(bot)
character_role_cmd.setup(bot)
fixy_cmd.setup(bot)

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("❌ DISCORD_TOKEN manquant dans .env")
    bot.run(TOKEN)