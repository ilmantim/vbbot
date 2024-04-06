from viberbotapp.bot_config import MAIN_MENU, METER_INFO
from viberbotapp.commands.find_bill import find_bill
from viberbotapp.commands.helper import send_fallback, send_message
from viberbotapp.commands.show_bill import show_bill
from viberbotapp.models import Person


def meter_info(message, chat_id):
    user_message = message.text.lower()
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    if user.prev_step == METER_INFO and user_message in ['да', 'нет']:
        state = show_bill(user_message, chat_id)
    elif user_message.isdigit():
        state, bill_value = find_bill(message, chat_id)
        return state, bill_value
    elif 'узнать' in user_message or 'счет' in user_message:
        send_message(
            chat_id,
            "Лицевой счёт указан в верхней части квитанции (извещение) "
            "рядом с Вашей фамилией",
            "Введите лицевой счет:"
        )
        state = METER_INFO
    elif 'меню' in user_message:
        state = MAIN_MENU
    elif 'ввести' in user_message or 'другой' in user_message:
        send_message(chat_id, 'Введите лицевой счёт')
        state = METER_INFO
    else:
        state = send_fallback(chat_id)

    return state, None



