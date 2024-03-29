
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
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

vb_token = env.str('VB_TOKEN')

bot_configuration = BotConfiguration(
    name="ch-sk bot",
    avatar=None,
    auth_token=vb_token,
)
viber = Api(bot_configuration)


START, CHOICE, END = range(3)

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
        print(state)
        if state == START:
            viber.send_messages(viber_request.sender.id, [
                TextMessage(
                    text='Hello! Please choose an option: \n a) Option A \n b) Option B \n c) Option C')
            ])
            state = CHOICE
        elif state == CHOICE:
            if message.text.lower() == 'a':
                viber.send_messages(viber_request.sender.id, [
                    TextMessage(text='You chose Option A')
                ])
            elif message.text.lower() == 'b':
                viber.send_messages(viber_request.sender.id, [
                    TextMessage(text='You chose Option B')
                ])
            elif message.text.lower() == 'c':
                viber.send_messages(viber_request.sender.id, [
                    TextMessage(text='You chose Option C')
                ])
            else:
                viber.send_messages(viber_request.sender.id, [
                    TextMessage(text='Invalid choice. Please choose again.')
                ])
            state = END

    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warning("client failed receiving message. failure: {0}".format(
            viber_request))

    return Response(status=200)
