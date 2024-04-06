from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from viberbot.api.viber_requests import ViberMessageRequest

from viberbotapp.bot_config import viber, START, MAIN_MENU, SUBMIT_READINGS, \
    METER_INFO, FAVORITES, CONTACT_INFO, FIND_BILL, CREATE_FAVORITE, \
    INPUT_READINGS
from viberbotapp.commands.contact_info import contact_info
from viberbotapp.commands.create_favorite import create_favorite
from viberbotapp.commands.favorites import favorites
from viberbotapp.commands.find_bill import find_bill
from viberbotapp.commands.input_readings import input_readings
from viberbotapp.commands.main_menu import handle_main_menu, handle_start
from viberbotapp.commands.helper import choose_section
from viberbotapp.commands.meter_info import meter_info
from viberbotapp.commands.submit_readings import submit_readings
from viberbotapp.models import Person


@require_POST
@csrf_exempt
def webhook(request):
    post_data = request.body.decode('utf-8')
    viber_request = viber.parse_request(post_data)

    if (isinstance(viber_request, ViberMessageRequest) and (
            viber_request.sender.id == '2qimAURso5+5B7yav4ZDIA==' or
            viber_request.sender.id == 'cn+6wVEyC20yMu9iGETumw=='
    )) and check_time(viber_request.timestamp):
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
    user_bills = [str(favorite.bill.value) for favorite in user.favorites.all()]
    print('Сейчас такой номер стейта: ', state)
    print('Сейчас такое сообщение: ', message)
    print('Сейчас такое id: ', chat_id)
    print('Это контекст сейчас', user.context)
    if state == START:
        state = handle_start(chat_id)
    elif state == MAIN_MENU:
        state = handle_main_menu(message, chat_id, user_bills)
    elif state == SUBMIT_READINGS or state == METER_INFO:
        if state == SUBMIT_READINGS:
            state, context = submit_readings(message, chat_id)
            user.prev_step = SUBMIT_READINGS
        else:
            state, context = meter_info(message, chat_id)
            user.prev_step = METER_INFO
        if context:
            user.context = context
            user.details = context
    elif state == FAVORITES:
        state = favorites(message, chat_id, user_bills)
    elif state == CONTACT_INFO:
        state, mro_name = contact_info(message, chat_id)
        user.context = mro_name
    elif state == FIND_BILL:
        state, context = find_bill(message, chat_id)
    elif state == CREATE_FAVORITE:
        state, context = create_favorite(message, chat_id)
        user.context = context
        user.details = context
    elif state == INPUT_READINGS:
        state, context = input_readings(message, chat_id)
        user.context = context
    if state == MAIN_MENU:
        bills = bool(user.favorites.count())
        state = choose_section(chat_id, bills)
    user.state = state
    user.save()


def check_time(timestamp):
    current_time_ms = int(round(timezone.now().timestamp() * 1000))
    print('ЭТО ВРЕМЯ РЕКВЕСТА', timestamp)
    print('ЭТО ВРЕМЯ СЕЙЧАС', current_time_ms)
    diff_ms = abs(current_time_ms - timestamp)
    diff_sec = diff_ms / 1000
    if diff_sec <= 5:
        return True
    else:
        return False
