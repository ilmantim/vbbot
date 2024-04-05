from viberbot.api.messages import TextMessage

from viberbotapp.bot_config import viber, MAIN_MENU
from viberbotapp.commands.keyboards import main_menu_keyboard


def choose_section(chat_id, bills):
    viber.send_messages(chat_id, [
        TextMessage(text='Главное меню. Выберите раздел'),
        main_menu_keyboard(bills)
    ])


def send_fallback(chat_id):
    viber.send_messages(chat_id, [
        TextMessage(text='Не понял команду. Давайте начнем сначала.')
    ])
    return MAIN_MENU


def handle_find_bill_info(chat_id):
    viber.send_messages(chat_id, [
        TextMessage(
            text=
            "Лицевой счёт указан в верхней части квитанции (извещение) "
            "рядом с Вашей фамилией \nВведите лицевой счет:"
        )
    ])
    return MAIN_MENU


def send_message(chat_id, *args):
    viber.send_messages(chat_id, [
        TextMessage(text=i) if type(i) is str else i for i in args
    ])
