from environs import Env
from viberbot import BotConfiguration, Api

env = Env()
env.read_env()

vb_token = env.str('VB_TOKEN')

bot_configuration = BotConfiguration(
    name="ch-sk bot",
    avatar=None,
    auth_token=vb_token,
)
viber = Api(bot_configuration)
