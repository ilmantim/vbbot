from viberbot.api.messages import TextMessage

from viberbotapp.bot_config import viber, SUBMIT_READINGS, METER_INFO, \
    FAVORITES, CONTACT_INFO, MAIN_MENU
from viberbotapp.commands.keyboards import choose_MRO_keyboard, \
    main_menu_keyboard, show_bills_keyboard


def handle_main_menu(message, chat_id, bills):
    user_message = message.text.lower()
    if 'показания' in user_message:  # добавить проверку наличия избранных счетов
        viber.send_messages(chat_id, [
            TextMessage(text='Введите лицевой счёт')
        ])
        state = SUBMIT_READINGS
    elif 'прибор' in user_message:  # добавить проверку наличия избранных счетов
        viber.send_messages(chat_id, [
            TextMessage(text='Введите лицевой счёт')
        ])
        state = METER_INFO
    elif 'счета' in user_message or 'мои' in user_message:
        viber.send_messages(chat_id, [
            TextMessage(text=f'Ваши лицевые счета:\n{bills}'),
            TextMessage(text='Выберите нужный пункт в меню снизу.'),
            show_bills_keyboard(),
        ])
        state = FAVORITES
    elif 'контакты' in user_message:
        viber.send_messages(chat_id, [
            TextMessage(text='Выберите МРО'),
            choose_MRO_keyboard()
        ])
        state = CONTACT_INFO
    else:
        state = send_fallback(chat_id)

    return state


def handle_start(chat_id):
    viber.send_messages(chat_id, [
        TextMessage(
            text=
            "Здравствуйте!\n"
            "Вас приветствует чат-бот "
            "АО «Чувашская энергосбытовая компания»\n"
            "\n"
            "Здесь Вы сможете передавать показания\n"
            "приборов учёта, узнать информацию об ИПУ\n"
            "и получить контактную информацию."
        )
    ])

    return MAIN_MENU


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
