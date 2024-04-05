from viberbotapp.bot_config import MAIN_MENU
from viberbotapp.commands.helper import send_message
from viberbotapp.models import Person, Bill


def show_bill(chat_id):
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
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
        send_message(
            chat_id,
            f'📟 Информация о приборе учета:\n'
            f'-----------------------------------\n'
            f'- Лицевой счет: {bill.value}\n'
            f'- Прибор учета: {device_title} - {modification} (№{serial_number})\n'
            f'- Номер счетчика: {serial_number}\n'
            f'{rate_info}'
            f'-----------------------------------\n'
        )

    return MAIN_MENU
