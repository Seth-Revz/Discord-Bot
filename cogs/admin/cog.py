import logging
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

log = logging.getLogger(__name__)

class Admin(commands.Cog, name='Admin'):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='change_presence',
        description='Change the bots Presence'
    )
    @app_commands.describe(status='Online, Idle, Dnd, Offline', action='Playing, Listening, Watching', message='Playing ______.')
    async def change_presence(self, interaction: discord.Interaction, status: Literal['Online', 'Idle', 'Dnd', 'Offline'], action: Literal['Playing', 'Listening', 'Watching'], message: str):
        """ Change status message. """

        if action.lower() == 'listening':
            playing_type = 2
        elif action.lower() == 'watching':
            playing_type = 3
        else:
            playing_type = 0

        if status.lower() == 'online':
            status_type = discord.Status.online
        elif status.lower() == 'idle':
            status_type = discord.Status.idle
        elif status.lower() == 'dnd':
            status_type = discord.Status.dnd
        elif status.lower() == 'offline':
            status_type = discord.Status.offline
        else:
            status_type = discord.Status.online

        try:
            await self.bot.change_presence(
                status=status_type,
                activity=discord.Activity(type=playing_type, name=message)
            )
            
            await interaction.response.send_message(f"Successfully changed: \nStatus: **{status.capitalize()}**, Type: **{action.capitalize()}**, Game: **{message}**", ephemeral=True)
        except discord.InvalidArgument as err:
            await interaction.response.send_message(err, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(e, ephemeral=True)

    @app_commands.command(
        name='reload',
        description='Reload a cog'
    )
    @app_commands.describe(name='Group name')
    async def reload(self, interaction: discord.Interaction, name: str):
        """ Reloads an extension. """
        try:
            await self.bot.reload_extension(f"cogs.{name}.cog")
        except Exception as e:
            print('error', e)
            return
        await interaction.response.send_message(content=f"Reloaded extension **{name}**")

async def setup(bot):
    await bot.add_cog(Admin(bot), guild=discord.Object(bot.config.ADMIN_GUILD_ID))
