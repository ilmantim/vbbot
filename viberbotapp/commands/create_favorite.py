from viberbotapp.bot_config import METER_INFO, SUBMIT_READINGS, MAIN_MENU
from viberbotapp.commands.meter_info import meter_info
from viberbotapp.commands.submit_readings import submit_readings
from viberbotapp.models import Favorite, Person, Bill


def create_favorite(message, chat_id):
    user_message = message.text.title()
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    bill = Bill.objects.get(value=user.context)
    bill.persons.add(user)
    if user_message == 'Да':
        fav, created = Favorite.objects.get_or_create(person=user, bill=bill)

    if user.prev_step == METER_INFO:
        step, context = meter_info(message, chat_id)
    elif user.prev_step == SUBMIT_READINGS:
        step, context = submit_readings(message, chat_id)
    else:
        step = MAIN_MENU

    return step
