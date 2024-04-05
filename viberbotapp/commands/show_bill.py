from viberbotapp.bot_config import MAIN_MENU, METER_INFO, SUBMIT_READINGS, \
    INPUT_READINGS
from viberbotapp.commands.helper import send_message, send_fallback
from viberbotapp.models import Person, Bill, Rate
import pytz

def show_bill(message, chat_id):
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    if message.isdigit():
        bill = Bill.objects.get(value=int(message))
    else:
        bill = Bill.objects.get(value=int(user.context))
    devices = bill.devices.all()
    if user.prev_step == METER_INFO:
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

        state = MAIN_MENU
    elif user.prev_step == SUBMIT_READINGS:
        rates_ids = [
            rate.id for device in devices for rate in
            device.rates.all()
        ]
        user.context = ','.join(rates_ids)
        user.save()
        state = MAIN_MENU
    else:
        state = send_fallback(chat_id)

    return state


def show_rate(chat_id):
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    if not user.context:
        state = MAIN_MENU
    else:
        rates_str = user.context
        rates = rates_str.split(',')
        rate = Rate.objects.get(id=rates[0])
        device = rate.device
        bill = device.bill
        device_title = device.device_title
        modification = device.modification
        serial_number = device.serial_number
        readings_str = f'{rate.readings} квт*ч' if rate.readings is not None else "Не указаны"
        moscow_timezone = pytz.timezone('Europe/Moscow')
        registration_date_str = rate.registration_date.astimezone(
            moscow_timezone).strftime("%d.%m.%Y") if (
            rate.registration_date
        ) else "Не указана"
        send_message(
            chat_id,
            f'📋 Информация о лицевом счете:\n'
            f'-----------------------------------\n'
            f'- Лицевой счет: {bill.value}\n'
            f'- Номер и тип прибора учета: {device_title} - {modification} (№{serial_number})\n'
            f'- Дата передачи последнего показания: {registration_date_str}\n'
            f'- Последнее показание: {readings_str}\n'
            f'- Тариф: {rate.cost}\n'
            f'-----------------------------------\n',
            'Введите показание:'
        )
        rates.pop(0)
        if rates:
            user.context = ','.join(rates)
            user.save()
            state = INPUT_READINGS
        else:
            state = MAIN_MENU

    return state

