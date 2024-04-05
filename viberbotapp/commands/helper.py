from viberbot.api.messages import TextMessage

from viberbotapp.bot_config import viber, MAIN_MENU
from viberbotapp.commands.keyboards import main_menu_keyboard


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
