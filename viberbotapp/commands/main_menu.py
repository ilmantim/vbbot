from django.utils import timezone

from viberbotapp.bot_config import SUBMIT_READINGS, METER_INFO, \
    FAVORITES, CONTACT_INFO, MAIN_MENU
from viberbotapp.commands.helper import send_fallback, send_message
from viberbotapp.commands.keyboards import choose_MRO_keyboard, \
    show_bills_keyboard, \
    submit_readings_and_get_meter_keyboard


def handle_main_menu(message, chat_id, bills):
    user_message = message.text.lower()
    if bills:
        text = 'Выберите нужный пункт в меню снизу.'
    else:
        text = 'Введите лицевой счёт'
    if 'показания' in user_message:
        if check_reading_period():
            send_message(
                chat_id,
                text,
                submit_readings_and_get_meter_keyboard(bills)
            )
            state = SUBMIT_READINGS
        else:
            send_message(
                chat_id,
                "Показания принимаются с 15 по 25 число каждого месяца."
            )
            state = MAIN_MENU
    elif 'прибор' in user_message:
        send_message(
            chat_id,
            text,
            submit_readings_and_get_meter_keyboard(bills)
        )
        state = METER_INFO
    elif 'счета' in user_message or 'мои' in user_message:
        all_bills = '\n'.join(bills)
        send_message(
            chat_id,
            f'Ваши лицевые счета:\n{all_bills}',
            'Выберите нужный пункт в меню снизу.',
            show_bills_keyboard()
        )
        state = FAVORITES
    elif 'контакты' in user_message:
        send_message(
            chat_id,
            'Выберите МРО',
            choose_MRO_keyboard()
        )
        state = CONTACT_INFO
    else:
        state = send_fallback(chat_id)

    return state


def handle_start(chat_id):
    send_message(
        chat_id,
        "Здравствуйте!\n"
        "Вас приветствует чат-бот "
        "АО «Чувашская энергосбытовая компания»\n"
        "\n"
        "Здесь Вы сможете передавать показания\n"
        "приборов учёта, узнать информацию об ИПУ\n"
        "и получить контактную информацию."
    )
    return MAIN_MENU


def check_reading_period():
    today = timezone.now()
    READING_PERIOD_START = 15
    READING_PERIOD_END = 25
    return READING_PERIOD_START <= today.day <= READING_PERIOD_END
