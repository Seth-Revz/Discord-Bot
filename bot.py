import atexit
import json
import logging.config
import pathlib
from typing import Optional, Literal

import asyncio
import discord
from discord.ext import commands

import configs.config as config
from utils.db import Database

logger = logging.getLogger("DiscordBotName")

class DiscordBot(commands.AutoShardedBot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix=commands.when_mentioned, 
            intents=intents
        )

        self.config = config
        self.db: Database = Database(config.DB_PATH)

    async def on_ready(self):
        logger.info(f"Ready: {self.user} | Servers: {len(self.guilds)}")

bot = DiscordBot()

@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context, mod: Optional[Literal["~"]] = None) -> None:
    if mod == "~":
        synced = await ctx.bot.tree.sync()
    else:
        synced = await ctx.bot.tree.sync()
        synced += await ctx.bot.tree.sync(guild=discord.Object(config.ADMIN_GUILD_ID))

    return await ctx.send(f"Synced {len(synced)} commands {'globally' if mod is None else 'to the current guild.'}")

def setup_logging() -> None:
    log_config = json.loads(pathlib.Path(config.LOGGING_CONFIG_PATH).read_text())
    logging.config.dictConfig(log_config)
    
    queue_handler = logging.getHandlerByName('queue_handler')
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

def setup_dirs() -> None:
    pathlib.Path.mkdir(pathlib.Path(config.LOG_DIR), parents=True, exist_ok=True)
    pathlib.Path.mkdir(pathlib.Path(config.DB_DIR), parents=True, exist_ok=True)

async def load_extensions():
    for folder in pathlib.Path('cogs').iterdir():
        if pathlib.Path.exists(pathlib.Path(folder, 'cog.py')):
            await bot.load_extension(f'cogs.{folder.name}.cog')

async def main():
    setup_dirs()
    setup_logging()

    await bot.db.create_tables()
    await load_extensions()
    await bot.start(config.BOT_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
