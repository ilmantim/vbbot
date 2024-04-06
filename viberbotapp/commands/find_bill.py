from django.utils import timezone

from viberbotapp.bot_config import MAIN_MENU, METER_INFO, FIND_BILL, \
    CREATE_FAVORITE, logger, SUBMIT_READINGS
from viberbotapp.commands.helper import send_fallback, send_message
from viberbotapp.commands.keyboards import yes_no_keyboard
from viberbotapp.commands.retrieve_bill_info import retrieve_bill_info
from viberbotapp.commands.show_bill import show_bill
from viberbotapp.models import Person, Bill, Device, Rate, Favorite


def find_bill(message, chat_id):
    user_message = message.text.lower()
    if user_message == 'нет':
        send_message(
            chat_id,
            "Проверьте правильность введения номера лицевого счета.\n"
            "Возможно, по данному адресу приборы учёта отсутствуют или "
            "закончился срок поверки.\n"
            "Для уточнения информации обратитесь к специалисту контакт-центра"
        )
        state = MAIN_MENU
    elif user_message == 'да':
        send_message(
            chat_id,
            "Вы хотите добавить этот лицевой счёт в избранное?",
            yes_no_keyboard()
        )
        state = CREATE_FAVORITE
    elif 'меню' in user_message:
        state = MAIN_MENU
    else:
        try:
            response_bill = retrieve_bill_info(user_message)
        except Exception as e:
            logger.info(f'Exception occurred:{e}')
            state = send_fallback(chat_id)
        else:
            if response_bill and user_message in response_bill.values():
                bill_value = create_bill(user_message, response_bill)
                send_message(
                    chat_id,
                    "Счет успешно найден."
                )
                user, created = Person.objects.get_or_create(
                    chat_id=chat_id
                )
                user_bills = Favorite.objects.filter(person=user)
                if user_bills.filter(bill__value=bill_value).exists():
                    if user.prev_step == METER_INFO:
                        state = show_bill(user_message, chat_id)
                    elif user.prev_step == SUBMIT_READINGS:
                        state, context = show_bill(user_message, chat_id)
                        return state, context
                    else:
                        state = MAIN_MENU
                else:
                    bill = Bill.objects.get(value=bill_value)
                    device = bill.devices.first()
                    send_message(
                        chat_id,
                        f'Адрес объекта - {device.address}?',
                        yes_no_keyboard()
                    )
                    state = FIND_BILL
                return state, bill_value
            else:
                send_message(
                    chat_id,
                    "Проверьте правильность введения номера лицевого счета.\n"
                    "Возможно, по данному адресу приборы учёта отсутствуют "
                    "или закончился срок поверки.\n"
                    "Для уточнения информации обратитесь "
                    "к специалисту контакт-центра"
                )
                state = MAIN_MENU

    return state, None


def create_bill(message, response_bill):
    bill, created = Bill.objects.get_or_create(
        value=int(message),
    )
    for device_num in range(len(response_bill["core_devices"])):
        device, created = Device.objects.get_or_create(
            device_title=f'{response_bill["core_devices"][device_num]["device_title"]}',
            modification=f'{response_bill["core_devices"][device_num]["modification"]}',
            serial_number=f'{response_bill["core_devices"][device_num]["serial_number"]}',
            id_device=response_bill["core_devices"][device_num][
                "id_meter"],
            address=(
                f'{response_bill["core_devices"][device_num]["type_locality"]}. '
                f'{response_bill["core_devices"][device_num]["locality"]} '
                f'{response_bill["core_devices"][device_num]["type_street"]}. '
                f'{response_bill["core_devices"][device_num]["street"]} '
                f'{response_bill["core_devices"][device_num]["type_house"]} '
                f'{response_bill["core_devices"][device_num]["house"]} '
                f'{response_bill["core_devices"][device_num]["type_building"]} '
                f'{response_bill["core_devices"][device_num]["building"]} '
                f'{response_bill["core_devices"][device_num]["condos_types"]} '
                f'{response_bill["core_devices"][device_num]["condos_number"]} '
            ),
            bill=bill
        )

        for rate_num in range(len(
                response_bill["core_devices"][device_num][
                    "rates"])):
            rate, created = Rate.objects.update_or_create(
                title=
                response_bill["core_devices"][device_num]["rates"][
                    rate_num]["title"],
                id_tariff=
                response_bill["core_devices"][device_num]["rates"][
                    rate_num]["id_tariff"],
                device=device,
                defaults={
                    'id_indication':
                        response_bill["core_devices"][device_num][
                            "rates"][rate_num]["id_indication"],
                    'cost':
                        response_bill["core_devices"][device_num][
                            "rates"][rate_num]["cost"]
                }
            )
            readings = \
                response_bill["core_devices"][device_num]["rates"][
                    rate_num]["reading"]
            if readings:
                rate.readings = int(
                    round(float(readings)))
            else:
                rate.readings = None

            date = \
                response_bill["core_devices"][device_num]["rates"][
                    rate_num]["date_reading"]
            if date:
                moscow_timezone = timezone.get_fixed_timezone(180)
                try:
                    rate.registration_date = timezone.datetime.strptime(
                        date,
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ).astimezone(tz=moscow_timezone)
                except ValueError:
                    rate.registration_date = timezone.datetime.strptime(
                        date,
                        "%Y-%m-%dT%H:%M:%SZ"
                    ).astimezone(tz=moscow_timezone)
            else:
                rate.registration_date = None
            rate.save()
    bill.save()

    return bill.value
