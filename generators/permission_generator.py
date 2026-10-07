import discord


def gang_overwrites(guild: discord.Guild, gang_role: discord.Role,
                    everyone: discord.Role):
    return {
        everyone: discord.PermissionOverwrite(view_channel=False),
        gang_role: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            connect=True,
            speak=True,
        ),
    }


def private_overwrites(guild: discord.Guild,
                       allowed_roles: list[discord.Role]):
    ow = {guild.default_role: discord.PermissionOverwrite(view_channel=False)}
    for r in allowed_roles:
        ow[r] = discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
        )
    return ow