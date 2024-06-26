from django.utils import timezone

from viberbotapp.bot_config import MAIN_MENU
from viberbotapp.commands.helper import send_message, send_fallback
from viberbotapp.commands.show_bill import show_rate, send_readings
from viberbotapp.models import Person, Rate


def input_readings(message, chat_id):
    user_message = message.text.lower()
    if user_message.isdigit():
        context = save_reading(user_message, chat_id)
        state, context = show_rate(chat_id, context)
        return state, context
    elif 'меню' in user_message:
        send_readings(chat_id)
        state = MAIN_MENU
    else:
        state = send_fallback(chat_id)

    return state, None


def save_reading(message, chat_id):
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    rates_str = user.context
    rates = rates_str.split(',')
    rate = Rate.objects.get(id=rates[0])
    if rate.readings:
        readings_1 = rate.readings
        readings_2 = int(message)
        subtraction = readings_2 - readings_1
        k = readings_2 / readings_1
        if subtraction >= 0 and k <= 2:
            text = f'Ваш расход составил {subtraction} квт*ч'
            send_message(
                chat_id,
                text
            )
        else:
            if subtraction < 0:
                text = ('Значение не может быть отрицательным, '
                           'перепроверьте показания и попробуйте снова.')
            else:
                text = ('Недопустимые данные, перепроверьте показания '
                           'и попробуйте снова.')
            send_message(
                chat_id,
                text
            )
            return ','.join(rates)
    rate.readings = int(message)
    rate.registration_date = timezone.now()
    rate.save()
    send_message(
        chat_id,
        'Показания сохранены.'
    )
    rates.pop(0)
    return ','.join(rates)
