from viberbot.api.messages import KeyboardMessage


def main_menu_keyboard(bills=False):
    keyboard = {
        "Type": "keyboard",
        "Buttons": [
            {
                "ActionType": "reply",
                "ActionBody": "Передать показания",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Передать показания</b></font>",
            },
            {
                "ActionType": "reply",
                "ActionBody": "Информация по прибору учета",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Информация по прибору учета</b></font>",
            },
            {
                "ActionType": "reply",
                "ActionBody": "Контакты и режим работы",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Контакты и режим работы</b></font>",
            }
        ]
    }
    if not bills:
        pass
    else:
        favorites = {
            "ActionType": "reply",
            "ActionBody": "Мои лицевые счета",
            "BgColor": "#ae9ef4",
            "Text": "<font color='#e5e1ff'><b>Мои лицевые счета</b></font>",
        }
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
            {
                "ActionType": "reply",
                "ActionBody": "Чебоксарское",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Чебоксарское МРО</b></font>",
            },
            {
                "ActionType": "reply",
                "ActionBody": "Алатырское",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Алатырское МРО</b></font>",
            },
            {
                "ActionType": "reply",
                "ActionBody": "Батыревское",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Батыревское МРО</b></font>",
            },
            {
                "ActionType": "reply",
                "ActionBody": "Канашское",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Канашское МРО</b></font>",
            },
            {
                "ActionType": "reply",
                "ActionBody": "Новочебоксарское",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Новочебоксарское МРО</b></font>",
            },
            {
                "ActionType": "reply",
                "ActionBody": "Цивильское",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Цивильское МРО</b></font>",
            },{
                "ActionType": "reply",
                "ActionBody": "Шумерлинское",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Шумерлинское МРО</b></font>",
            },
            {
                "ActionType": "reply",
                "ActionBody": "Ядринское",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Ядринское МРО</b></font>",
            },
            {
                "ActionType": "reply",
                "ActionBody": "Управление",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Управление</b></font>",
            },
            {
                "ActionType": "reply",
                "ActionBody": "Главное меню",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Главное меню</b></font>",
            }
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
        "Buttons": [
            {
                "ActionType": "reply",
                "ActionBody": f"{i}",
                "BgColor": "#ae9ef4",
                "Text": f"<font color='#e5e1ff'><b>{i}</b></font>",
            }
            for i in addresses
        ]
        +
        [
            {
                "ActionType": "reply",
                "ActionBody": "Главное меню",
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Главное меню</b></font>",
            }
        ]
    }
    keyboard_message = KeyboardMessage(
        keyboard=keyboard,
        min_api_version=6
    )
    return keyboard_message
