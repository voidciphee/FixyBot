import discord


async def create_text(guild, name, category=None, overwrites=None, topic=None):
    existing = discord.utils.get(guild.text_channels, name=name)
    if existing:
        return existing
    return await guild.create_text_channel(
        name=name,
        category=category,
        overwrites=overwrites or {},
        topic=topic,
        reason="Générateur de serveur de gang",
    )


async def create_voice(guild, name, category=None, overwrites=None):
    existing = discord.utils.get(guild.voice_channels, name=name)
    if existing:
        return existing
    return await guild.create_voice_channel(
        name=name,
        category=category,
        overwrites=overwrites or {},
        reason="Générateur de serveur de gang",
    )