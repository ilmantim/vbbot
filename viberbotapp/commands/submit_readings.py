from viberbotapp.bot_config import MAIN_MENU, SUBMIT_READINGS
from viberbotapp.commands.find_bill import find_bill
from viberbotapp.commands.helper import send_message, send_fallback
from viberbotapp.commands.keyboards import return_to_main_menu_keyboard, \
    submit_readings_and_get_meter_keyboard
from viberbotapp.commands.show_bill import show_bill
from viberbotapp.models import Person


def submit_readings(message, chat_id):
    user_message = message.text.lower()
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    if user.prev_step == SUBMIT_READINGS and user_message in ['да', 'нет']:
        state, context = show_bill(user_message, chat_id)
        return state, context
    elif user_message.isdigit():
        state, context = find_bill(message, chat_id)
        return state, context
    elif 'узнать' in user_message or 'счет' in user_message:
        send_message(
            chat_id,
            "Лицевой счёт указан в верхней части квитанции (извещение) "
            "рядом с Вашей фамилией",
            "Введите лицевой счет:",
            return_to_main_menu_keyboard()
        )
        state = SUBMIT_READINGS
    elif 'меню' in user_message:
        state = MAIN_MENU
    elif 'ввести' in user_message or 'другой' in user_message:
        send_message(
            chat_id,
            'Введите лицевой счёт',
            submit_readings_and_get_meter_keyboard()
            )
        state = SUBMIT_READINGS
    else:
        state = send_fallback(chat_id)

    return state, None
