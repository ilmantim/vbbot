import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from viberbot.api.viber_requests import ViberMessageRequest

from viberbotapp.bot_config import viber, START, MAIN_MENU, SUBMIT_READINGS, \
    METER_INFO, FAVORITES, CONTACT_INFO, FIND_BILL, CREATE_FAVORITE
from viberbotapp.commands.contact_info import contact_info
from viberbotapp.commands.create_favorite import create_favorite
from viberbotapp.commands.favorites import favorites
from viberbotapp.commands.find_bill import find_bill
from viberbotapp.commands.main_menu import handle_main_menu, handle_start, \
    choose_section
from viberbotapp.commands.meter_info import meter_info
from viberbotapp.commands.submit_readings import submit_readings
from viberbotapp.models import Person



@require_POST
@csrf_exempt
def webhook(request):
    post_data = request.body.decode('utf-8')
    viber_request = viber.parse_request(post_data)

    if isinstance(viber_request, ViberMessageRequest) and (
            viber_request.sender.id == '2qimAURso5+5B7yav4ZDIA==' or
            viber_request.sender.id == 'cn+6wVEyC20yMu9iGETumw=='
    ):
        message_handler(viber_request)

    return HttpResponse(status=200)


def message_handler(viber_request):
    user, created = Person.objects.get_or_create(
        chat_id=viber_request.sender.id,
        name=viber_request.sender.name
    )
    state = user.state
    chat_id = user.chat_id
    message = viber_request.message
    if user.favorites.count() > 0:
        bills = True
        user_bills = [str(favorite.bill.value) for favorite in
                      user.favorites.all()]
        all_bills = '\n'.join(user_bills)
    else:
        bills = False
        user_bills = []
        all_bills = ''
    print('Сейчас такой номер стейта: ', state)
    print('Сейчас такое сообщение: ', message)
    print('Сейчас такое id: ', chat_id)
    print('Это контекст сейчас', user.context)
    if state == START:
        state = handle_start(chat_id)
    elif state == MAIN_MENU:
        state = handle_main_menu(message, chat_id, all_bills)
    elif state == SUBMIT_READINGS:
        state = submit_readings(message, chat_id)
    elif state == METER_INFO:
        state, bill_value = meter_info(message, chat_id)
        if bill_value:
            user.context = bill_value
    elif state == FAVORITES:
        state = favorites(message, chat_id, user_bills)
    elif state == CONTACT_INFO:
        state, mro_name = contact_info(message, chat_id)
        user.context = mro_name
    elif state == FIND_BILL:
        state, bill_value = find_bill(message, chat_id)
    elif state == CREATE_FAVORITE:
        state = create_favorite(message, chat_id)
    if state == MAIN_MENU:
        choose_section(chat_id, bills)
    user.state = state
    user.save()
