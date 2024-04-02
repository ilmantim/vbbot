import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from viberbot.api.viber_requests import ViberMessageRequest

from viberbotapp.bot_config import viber
from viberbotapp.commands.contact_info import contact_info
from viberbotapp.commands.favorites import favorites
from viberbotapp.commands.main_menu import handle_main_menu, handle_start, \
    choose_section
from viberbotapp.commands.meter_info import meter_info
from viberbotapp.commands.submit_readings import submit_readings
from viberbotapp.models import Person

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


START, MAIN_MENU, SUBMIT_READINGS, METER_INFO, FAVORITES, CONTACT_INFO = range(
    6)


@api_view(['POST'])
@csrf_exempt
def webhook(request):
    post_data = request.body.decode('utf-8')
    viber_request = viber.parse_request(post_data)

    if isinstance(viber_request, ViberMessageRequest) and (
            viber_request.sender.id == '2qimAURso5+5B7yav4ZDIA==' or
            viber_request.sender.id == 'cn+6wVEyC20yMu9iGETumw=='
    ):
        message_handler(viber_request)

    return Response(status=200)


def message_handler(viber_request):
    user, created = Person.objects.get_or_create(
        chat_id=viber_request.sender.id,
        name=viber_request.sender.name
    )
    state = user.state
    chat_id = user.chat_id
    message = viber_request.message
    print('Сейчас такой номер стейта: ', state)
    print('Сейчас такое сообщение: ', message)
    print('Сейчас такое id: ', chat_id)
    print('Это контекст сейчас', user.context)
    if state == START:
        state = handle_start(chat_id)
    elif state == MAIN_MENU:
        state = handle_main_menu(message, chat_id)
    elif state == SUBMIT_READINGS:
        state = submit_readings(chat_id)
    elif state == METER_INFO:
        state = meter_info(chat_id)
    elif state == FAVORITES:
        state = favorites(chat_id)
    elif state == CONTACT_INFO:
        state, mro_name = contact_info(message, chat_id)
        user.context = mro_name
    if state == MAIN_MENU:
        choose_section(chat_id)
    user.state = state
    user.save()
