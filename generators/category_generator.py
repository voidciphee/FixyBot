import discord


async def create_category(guild: discord.Guild, name: str, overwrites=None):
    existing = discord.utils.get(guild.categories, name=name)
    if existing:
        return existing
    return await guild.create_category(
        name=name, overwrites=overwrites or {},
        reason="Générateur de serveur de gang",
    )