from viberbotapp.bot_config import MAIN_MENU
from viberbotapp.commands.helper import send_message


def submit_readings(message, chat_id):
    # сюда переносим логику из бота тг
    send_message(
        chat_id,
        "Этот раздел находится в разбработке. Возвращаю в главное меню"
    )
    return MAIN_MENU
