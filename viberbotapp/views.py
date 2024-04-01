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

from viberbotapp.keyboards import main_menu_keyboard, choose_MRO_keyboard, \
    choose_address_keyboard
from viberbotapp.models import Person, Mro
from time import sleep

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


@api_view(['POST'])
@csrf_exempt
def webhook(request):
    post_data = request.body.decode('utf-8')
    #logger.debug("received request. post data: {0}".format(post_data))
    viber_request = viber.parse_request(post_data)

    if isinstance(viber_request, ViberMessageRequest) and (viber_request.sender.id == '2qimAURso5+5B7yav4ZDIA==' or viber_request.sender.id == 'cn+6wVEyC20yMu9iGETumw=='):
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
            viber.send_messages(chat_id, [
                TextMessage(text='Главное меню. Выберите раздел'),
                main_menu_keyboard()
            ])
        user.state = state
        user.save()

    return Response(status=200)


def handle_start(chat_id):
    viber.send_messages(chat_id, [
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

    return MAIN_MENU


def handle_main_menu(message, chat_id):
    user_message = message.text.lower()
    if 'показания' in user_message:  # добавить проверку наличия избранных счетов
        viber.send_messages(chat_id, [
            TextMessage(text='Введите лицевой счёт')
        ])
        state = SUBMIT_READINGS
    elif 'прибор' in user_message:  # добавить проверку наличия избранных счетов
        viber.send_messages(chat_id, [
            TextMessage(text='Введите лицевой счёт')
        ])
        state = METER_INFO
    elif 'счета' in user_message or 'мои' in user_message:  # добавить условие, что избранные счета вообще существуют
        viber.send_messages(chat_id, [
            TextMessage(text='Ваши лицевые счета:')
        ])
        state = FAVORITES
    elif 'контакты' in user_message:
        viber.send_messages(chat_id, [
            TextMessage(text='Выберите МРО'),
            choose_MRO_keyboard()
        ])
        state = CONTACT_INFO
    else:
        viber.send_messages(chat_id, [
            TextMessage(text='Не понял команду. Давайте начнем сначала.')
        ])
        state = MAIN_MENU

    return state


def submit_readings(chat_id):
    # сюда переносим логику из бота тг
    viber.send_messages(chat_id, [
        TextMessage(
            text=
            "Этот раздел находится в разбработке. Возвращаю в главное меню"
        )
    ])
    state = MAIN_MENU
    return state


def meter_info(chat_id):
    # сюда переносим логику из бота тг
    viber.send_messages(chat_id, [
        TextMessage(
            text=
            "Этот раздел находится в разбработке. Возвращаю в главное меню"
        )
    ])
    state = MAIN_MENU
    return state


def favorites(chat_id):
    # сюда переносим логику из бота тг
    viber.send_messages(chat_id, [
        TextMessage(
            text=
            "Этот раздел находится в разбработке. Возвращаю в главное меню"
        )
    ])
    state = MAIN_MENU
    return state


def contact_info(message, chat_id):
    user_message = message.text.title()
    user = Person.objects.get(chat_id=chat_id)
    if user_message.isdigit():
        mro = Mro.objects.get(name=user.context)
        addresses = mro.addresses.all()
        address = addresses.get(num=int(user_message))
        viber.send_messages(chat_id, [
            TextMessage(
                text=address.name
            )
        ])
        return MAIN_MENU, None
    else:
        mro = Mro.objects.filter(name__icontains=user_message).first()
        if mro:
            viber.send_messages(chat_id, [
                TextMessage(
                    text=mro.general
                )
            ])
            if mro.addresses.count() > 0:
                addresses = [str(i + 1) for i in range(mro.addresses.count())]
                viber.send_messages(chat_id, [
                    TextMessage(
                        text="Выберите номер удобного для Вас МРО в меню снизу"
                    ),
                    choose_address_keyboard(addresses)
                ])
                return CONTACT_INFO, mro.name
        elif 'меню' in message.text.lower():
            pass
        else:
            viber.send_messages(chat_id, [
                TextMessage(text='Не понял команду. Давайте начнем сначала.')
            ])

        return MAIN_MENU, None
