from viberbot.api.messages import TextMessage

from viberbotapp.bot_config import viber
from viberbotapp.commands.keyboards import choose_MRO_keyboard, \
    main_menu_keyboard

START, MAIN_MENU, SUBMIT_READINGS, METER_INFO, FAVORITES, CONTACT_INFO = range(
    6)


def handle_main_menu(message, chat_id):
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
    elif 'счета' in user_message or 'мои' in user_message:  # добавить условие, что избранные счета вообще существуют
        viber.send_messages(chat_id, [
            TextMessage(text='Ваши лицевые счета:')
        ])
        state = FAVORITES
    elif 'контакты' in user_message:
        viber.send_messages(chat_id, [
            TextMessage(text='Выберите МРО'),
            choose_MRO_keyboard()
        ])
        state = CONTACT_INFO
    else:
        viber.send_messages(chat_id, [
            TextMessage(text='Не понял команду. Давайте начнем сначала.')
        ])
        state = MAIN_MENU

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


def choose_section(chat_id):
    viber.send_messages(chat_id, [
        TextMessage(text='Главное меню. Выберите раздел'),
        main_menu_keyboard()
    ])