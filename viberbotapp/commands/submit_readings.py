from viberbot.api.messages import TextMessage

from viberbotapp.bot_config import viber, MAIN_MENU


def submit_readings(message, chat_id):
    # сюда переносим логику из бота тг
    viber.send_messages(chat_id, [
        TextMessage(
            text=
            "Этот раздел находится в разбработке. Возвращаю в главное меню"
        )
    ])
    return MAIN_MENU
