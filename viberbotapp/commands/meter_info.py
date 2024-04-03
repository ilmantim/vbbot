from viberbot.api.messages import TextMessage

from viberbotapp.bot_config import viber, MAIN_MENU, METER_INFO
from viberbotapp.commands.find_bill import find_bill
from viberbotapp.commands.main_menu import send_fallback, handle_find_bill_info
from viberbotapp.commands.retrieve_bill_info import retrieve_bill_info
from viberbotapp.models import Person, Bill, Device, Rate, Favorite

from django.utils import timezone


def meter_info(message, chat_id):
    user_message = message.text.title()
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    if user.prev_step == METER_INFO and user_message in ['Да', 'Нет']:
        bill = Bill.objects.get(value=int(user.context))
        devices = bill.devices.all()
        for device_here in devices:
            device_title = device_here.device_title
            modification = device_here.modification
            serial_number = device_here.serial_number
            rates = device_here.rates.all()
            rates_of_device = {}
            for rate_here in rates:
                rates_of_device[rate_here.title] = rate_here.cost
            rate_info = "- Величина тарифа:\n"
            for rate_key, rate_value in rates_of_device.items():
                rate_info += f"  - {rate_key}: {rate_value}₽\n"
            viber.send_messages(chat_id, [
                TextMessage(
                    text=
                    f'📟 Информация о приборе учета:\n'
                    f'-----------------------------------\n'
                    f'- Лицевой счет: {bill.value}\n'
                    f'- Прибор учета: {device_title} - {modification} (№{serial_number})\n'
                    f'- Номер счетчика: {serial_number}\n'
                    f'{rate_info}'
                    f'-----------------------------------\n'
                )
            ])
        state = MAIN_MENU
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
        state = METER_INFO
    else:
        state = send_fallback(chat_id)

    return state, None
