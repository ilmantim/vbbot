from django.utils import timezone
from viberbot.api.messages import TextMessage
from environs import Env
from viberbotapp.bot_config import viber, MAIN_MENU
from viberbotapp.commands.keyboards import main_menu_keyboard


env = Env()
env.read_env()


def choose_section(chat_id, bills):
    send_message(
        chat_id,
        'Главное меню. Выберите раздел',
        main_menu_keyboard(bills)
    )
    return MAIN_MENU


def send_fallback(chat_id):
    send_message(
        chat_id,
        'Не понял команду. Давайте начнем сначала.'
    )
    return MAIN_MENU


def send_message(chat_id, *args):
    viber.send_messages(chat_id, [
        TextMessage(text=i) if type(i) is str else i for i in args
    ])


def check_reading_period():
    today = timezone.now()
    READING_PERIOD_START = env.int('START_DAY')
    READING_PERIOD_END = env.int('END_DAY')
    return READING_PERIOD_START <= today.day <= READING_PERIOD_END
