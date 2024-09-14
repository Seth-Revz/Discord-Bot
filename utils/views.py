import configs.config as config

def custom_id(view: str, id: int) -> str:
    """create a custom id from the bot name : the view : the identifier"""
    return f'{config.BOT_NAME}:{view}:{id}'