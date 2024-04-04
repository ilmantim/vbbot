from viberbot.api.messages import KeyboardMessage


def main_menu_keyboard(bills):
    keyboard = {
        "Type": "keyboard",
        "Buttons": [
            get_button("Передать показания"),
            get_button("Информация по прибору учета"),
            get_button("Контакты и режим работы")
        ]
    }
    if not bills:
        pass
    else:
        favorites = get_button("Мои лицевые счета")
        keyboard['Buttons'].insert(2, favorites)

    keyboard_message = KeyboardMessage(
        keyboard=keyboard,
        min_api_version=6
    )
    return keyboard_message


def choose_MRO_keyboard():
    keyboard = {
        "Type": "keyboard",
        "Buttons": [
            get_button("Чебоксарское"),
            get_button("Алатырское"),
            get_button("Батыревское"),
            get_button("Канашское"),
            get_button("Новочебоксарское"),
            get_button("Цивильское"),
            get_button("Шумерлинское"),
            get_button("Ядринское"),
            get_button("Управление"),
            get_button("Главное меню")
        ]
    }
    keyboard_message = KeyboardMessage(
        keyboard=keyboard,
        min_api_version=6
    )
    return keyboard_message


def choose_address_keyboard(addresses):
    keyboard = {
        "Type": "keyboard",
        "Buttons": [get_button(i) for i in addresses] +
                   [get_button("Главное меню")]
    }
    keyboard_message = KeyboardMessage(
        keyboard=keyboard,
        min_api_version=6
    )
    return keyboard_message


def show_bills_keyboard():
    keyboard = {
        "Type": "keyboard",
        "Buttons": [
            get_button("Удалить ЛС из избранного"),
            get_button("Главное меню")
        ]
    }
    keyboard_message = KeyboardMessage(
        keyboard=keyboard,
        min_api_version=6
    )
    return keyboard_message


def delete_bills_keyboard(info):
    keyboard = {
        "Type": "keyboard",
        "Buttons": [get_button(i) for i in info] +
                   [get_button("Назад"), get_button("Главное меню")]
    }
    keyboard_message = KeyboardMessage(
        keyboard=keyboard,
        min_api_version=6
    )
    return keyboard_message


def submit_readings_and_get_meter_keyboard(info):
    buttons = [
        get_button("Как узнать лицевой счёт"),
        get_button("Главное меню")
    ]
    keyboard = {
        "Type": "keyboard",
        "Buttons": buttons
    }
    if info:
        keyboard = {
            "Type": "keyboard",
            "Buttons": [get_button(i) for i in info] +
                       [get_button("Ввести другой")] +
                       buttons
        }
    keyboard_message = KeyboardMessage(
        keyboard=keyboard,
        min_api_version=6
    )
    return keyboard_message


def yes_no_keyboard():
    keyboard = {
        "Type": "keyboard",
        "Buttons": [
            get_button("Да"),
            get_button("Нет"),
            get_button("Главное меню")
        ]
    }
    keyboard_message = KeyboardMessage(
        keyboard=keyboard,
        min_api_version=6
    )
    return keyboard_message


def get_button(text, background_color='#ae9ef4', font_color='#e5e1ff'):
    button = {
        "ActionType": "reply",
        "ActionBody": f"{text}",
        "BgColor": f"{background_color}",
        "Text": f"<font color={font_color}><b>{text}</b></font>",
    }

    return button
