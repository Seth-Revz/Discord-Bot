import logging

import discord
from discord import Activity, Status
from discord.ext import commands

log = logging.getLogger(__name__)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction, command):        
        msg: str = ''
        group: str = f'{command.parent.name} ' if command.parent else ''
        command = command.name
        try:
            if 'options' in interaction.data:
                for option in interaction.data['options']:
                    if option['name'] not in msg:
                        if 'value' in option:
                            msg+=f" {option['name']}: {option['value']},"
            log.info(f"{interaction.guild.name} > {interaction.user} > /{group}{command}{msg.rstrip(',')}")
        except AttributeError:
            if 'options' in interaction.data:
                for option in interaction.data['options']:
                    if option['name'] not in msg:
                        if 'value' in option:
                            msg+=f" {option['name']}: {option['value']},"
            log.info(f"Private message > {interaction.user} > /{group}{command}{msg.rstrip(',')}")

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.config.STATUS == 'idle':
            status_type = Status.idle
        elif self.bot.config.STATUS == 'dnd':
            status_type = Status.dnd
        else:
            status_type = Status.online

        if self.bot.config.PLAYING_TYPE == 'listening':
            playing_type = 2
        elif self.bot.config.PLAYING_TYPE == 'watching':
            playing_type = 3
        else:
            playing_type = 0

        await self.bot.change_presence(
            activity=Activity(type=playing_type, name=self.bot.config.PLAYING),
            status=status_type
        )

async def setup(bot):
    await bot.add_cog(Events(bot))
