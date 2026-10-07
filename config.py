import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SUPPORT_SERVER_INVITE = os.getenv("SUPPORT_SERVER_INVITE", "https://discord.gg/")
DATA_DIR = "data"