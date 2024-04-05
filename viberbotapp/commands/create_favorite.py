from viberbotapp.bot_config import METER_INFO, SUBMIT_READINGS, MAIN_MENU
from viberbotapp.commands.helper import send_fallback
from viberbotapp.commands.meter_info import meter_info
from viberbotapp.commands.submit_readings import submit_readings
from viberbotapp.models import Favorite, Person, Bill


def create_favorite(message, chat_id):
    user_message = message.text.lower()
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    bill = Bill.objects.get(value=user.context)
    bill.persons.add(user)
    if user_message == 'да':
        fav, created = Favorite.objects.get_or_create(person=user, bill=bill)
    if user_message in ['да', 'нет']:
        if user.prev_step == METER_INFO:
            state, context = meter_info(message, chat_id)
        elif user.prev_step == SUBMIT_READINGS:
            state, context = submit_readings(message, chat_id)
        else:
            state = MAIN_MENU
            context = None
        return state, context
    elif 'меню' in user_message:
        state = MAIN_MENU
    else:
        state = send_fallback(chat_id)

    return state, None
