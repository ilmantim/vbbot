import pytz
import requests

from viberbotapp.bot_config import MAIN_MENU, METER_INFO, SUBMIT_READINGS, \
    INPUT_READINGS, logger
from viberbotapp.commands.helper import send_message, send_fallback
from viberbotapp.commands.keyboards import return_to_main_menu_keyboard
from viberbotapp.commands.retrieve_bill_info import API_BASE_URL
from viberbotapp.models import Person, Bill, Rate


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
            str(rate.id) for device in devices for rate in
            device.rates.all()
        ]
        print('ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ', rates_ids)
        print('ЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁЁ', ','.join(rates_ids))
        context = ','.join(rates_ids)
        state, context = show_rate(chat_id, context)
        return state, context
    else:
        state = send_fallback(chat_id)

    return state


def show_rate(chat_id, context):
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    if not context:
        send_readings(chat_id)
        state = MAIN_MENU
    else:
        rates_str = context
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
            'Введите показание:',
            return_to_main_menu_keyboard()
        )
        return INPUT_READINGS, context

    return state, None


def send_readings(chat_id):
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    rates_str = user.details
    rates = rates_str.split(',')
    rates = [Rate.objects.get(id=id) for id in rates]
    devices = list({rate.device for rate in rates})
    data = [
        {
            "id_device": device.id_device,
            "id_receiving_method": 60,
            "id_reading_status": 6,
            "rates": [
                {
                    "id_tariff": rate.id_tariff,
                    "id_indication": rate.id_indication,
                    "reading": rate.readings
                } for rate in device.rates.all()
            ]
        } for device in devices
    ]
    url = f'https://{API_BASE_URL}/api/v0/cabinet/terminal/submitReadings'
    for device_data in data:
        response = requests.post(url, json=device_data)
        if response.status_code == 200:
            logger.info('Success!')
        else:
            logger.info('Error: %s', str(response.status_code))
