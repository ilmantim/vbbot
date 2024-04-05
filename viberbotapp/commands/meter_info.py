from viberbotapp.bot_config import MAIN_MENU, METER_INFO
from viberbotapp.commands.find_bill import find_bill
from viberbotapp.commands.helper import send_fallback, handle_find_bill_info, \
    send_message
from viberbotapp.commands.show_bill import show_bill
from viberbotapp.models import Person


def meter_info(message, chat_id):
    user_message = message.text.lower()
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    if user.prev_step == METER_INFO and user_message in ['да', 'нет']:
        state = show_bill(chat_id)
    elif user_message.isdigit():
        user.prev_step = METER_INFO
        user.save()
        state, bill_value = find_bill(message, chat_id)
        return state, bill_value
    elif 'узнать' in user_message or 'счет' in user_message:
        state = handle_find_bill_info(chat_id)
    elif 'меню' in user_message:
        state = MAIN_MENU
    elif 'ввести' in user_message or 'другой' in user_message:
        send_message(chat_id, 'Введите лицевой счёт')
        state = METER_INFO
    else:
        state = send_fallback(chat_id)

    return state, None



