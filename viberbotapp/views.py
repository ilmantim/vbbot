import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response
from viberbot.api.messages import TextMessage
from viberbot.api.viber_requests import ViberMessageRequest, \
    ViberSubscribedRequest, ViberFailedRequest

from django.views.decorators.csrf import csrf_exempt
from viberbot.api.bot_configuration import BotConfiguration
from viberbot import Api

from environs import Env

env = Env()
env.read_env()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

vb_token = env.str('VB_TOKEN')

bot_configuration = BotConfiguration(
    name="ch-sk bot",
    avatar=None,
    auth_token=vb_token,
)
viber = Api(bot_configuration)

START, MAIN_MENU, SUBMIT_READINGS, METER_INFO, FAVORITES, CONTACT_INFO = range(
    6)

state = START


@api_view(['POST'])
@csrf_exempt
def webhook(request):
    post_data = request.body.decode('utf-8')
    logger.debug("received request. post data: {0}".format(post_data))
    viber_request = viber.parse_request(post_data)

    global state

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        print('Сейчас такой номер стейта: ', state)
        print('Сейчас такое сообщение: ', message)
        if state == START:
            handle_start(viber_request.sender.id)
            state = MAIN_MENU
        elif state == MAIN_MENU:
            state = handle_main_menu(message, viber_request.sender.id)
        elif state == SUBMIT_READINGS:
            state = submit_readings(viber_request.sender.id)
        elif state == METER_INFO:
            state = meter_info(viber_request.sender.id)
        elif state == FAVORITES:
            state = favorites(viber_request.sender.id)
        elif state == CONTACT_INFO:
            state = contact_info(message, viber_request.sender.id)

    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warning("client failed receiving message. failure: {0}".format(
            viber_request))

    return Response(status=200)


def handle_start(person_id):
    viber.send_messages(person_id, [
        TextMessage(
            text=
            "Здравствуйте!\n"
            "Вас приветствует чат-бот "
            "АО «Чувашская энергосбытовая компания»\n"
            "\n"
            "Здесь Вы сможете передавать показания\n"
            "приборов учёта, узнать информацию об ИПУ\n"
            "и получить контактную информацию."
        )
    ])


def handle_main_menu(message, person_id):
    if message.text.lower() == 'передать показания':  # добавить проверку наличия избранных счетов
        viber.send_messages(person_id, [
            TextMessage(text='Введите лицевой счёт')
        ])
        state = SUBMIT_READINGS
    elif message.text.lower() == 'информация по прибору учета':  # добавить проверку наличия избранных счетов
        viber.send_messages(person_id, [
            TextMessage(text='Введите лицевой счёт')
        ])
        state = METER_INFO
    elif message.text.lower() == 'мои лицевые счета':  # добавить условие, что избранные счета вообще существуют
        viber.send_messages(person_id, [
            TextMessage(text='Ваши лицевые счета:')
        ])
        state = FAVORITES
    elif message.text.lower() == 'контакты и режим работы':
        viber.send_messages(person_id, [
            TextMessage(text='Выберите МРО')
        ])
        state = CONTACT_INFO
    else:
        viber.send_messages(person_id, [
            TextMessage(text='Не понял команду. Давайте начнем сначала.')
        ])
        state = MAIN_MENU

    return state


def submit_readings(person_id):
    viber.send_messages(person_id, [
        TextMessage(
            text=
            "Этот раздел находится в разбработке. Возвращаю в главное меню"
        )
    ])
    state = MAIN_MENU
    return state


def meter_info(person_id):
    viber.send_messages(person_id, [
        TextMessage(
            text=
            "Этот раздел находится в разбработке. Возвращаю в главное меню"
        )
    ])
    state = MAIN_MENU
    return state


def favorites(person_id):
    viber.send_messages(person_id, [
        TextMessage(
            text=
            "Этот раздел находится в разбработке. Возвращаю в главное меню"
        )
    ])
    state = MAIN_MENU
    return state


def contact_info(message, person_id):
    # здесь нужно добавить логику поиска названия МРО в базе данных по message
    if 'алатырское' in message.text.lower():  # добавить проверку наличия избранных счетов
        viber.send_messages(person_id, [
            TextMessage(
                text=
                """Адрес: 429820, Чувашская Республика, 
                г. Алатырь, ул. Московская/Жуковского, д. 64/57,
                Телефон: 8 (83531) 2-36-30,
                Режим работы: ПН-ПТ 08:00-17:00 
                (технический перерыв с 13:00 до 14:00)"""
            )
        ])
        state = MAIN_MENU
    elif 'чебоксарское' in message.text.lower():  # добавить проверку наличия избранных счетов
        viber.send_messages(person_id, [
            TextMessage(
                text=
                """1 — 428018, г. Чебоксары, пр. Московский, д.41, корп.1
                2 — 428022, Чувашская Республика, г. Чебоксары, ул. 50 лет Октября, д. 4, пом. 2
                3 — 428000, Чувашская Республика, г. Чебоксары, Эгерский б-р, д. 33б"""
            )
        ])
        state = MAIN_MENU
    else:
        viber.send_messages(person_id, [
            TextMessage(text='Не понял команду. Давайте начнем сначала.')
        ])
        state = MAIN_MENU

    return state
