import os
import pathlib
from dotenv.main import load_dotenv

load_dotenv()

BOT_NAME = 'DiscordBot'
BOT_TOKEN = os.getenv('DISCORD_TOKEN', '')

OWNER_ID = int(os.getenv('BOT_OWNER_ID', ''))
ADMIN_GUILD_ID = int(os.getenv('ADMIN_GUILD_ID', ''))
PLAYING = 'GameName'
PLAYING_TYPE = 'playing'
STATUS = 'online'
INVITE_URL = os.getenv('INVITE_URL', '')

CONFIG_DIR = 'configs'
LOG_DIR = 'logs'
DB_DIR = 'data'

LOGGING_CONFIG_FILE = 'logging_config.json'
LOG_FILE = 'bot.log'
DB_FILE = 'database.db'

LOGGING_CONFIG_PATH = pathlib.Path(CONFIG_DIR, LOGGING_CONFIG_FILE)
LOG_PATH = pathlib.Path(LOG_DIR, LOG_FILE)
DB_PATH = pathlib.Path(DB_DIR, DB_FILE)

# EMOTES = {
#     'Shiny': '<a:shiny:824860421386534922>',
# }
