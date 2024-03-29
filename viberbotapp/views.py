import json

import logging
from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from viberbot.api.messages import TextMessage
from viberbot.api.viber_requests import ViberMessageRequest, \
    ViberSubscribedRequest, ViberFailedRequest

from .models import Mro
from django.views.decorators.csrf import csrf_exempt
from viberbot.api.bot_configuration import BotConfiguration
from viberbot import Api
from django.http import HttpResponse
from environs import Env


env = Env()
env.read_env()
url = env('NGROK')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class MroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mro
        fields = '__all__'


class Mros(generics.ListCreateAPIView):
    queryset = Mro.objects.all()
    serializer_class = MroSerializer


BASE_URL = url
vb_token = env.str('VB_TOKEN')

bot_configuration = BotConfiguration(
    name="ch-sk bot",
    avatar=None,
    auth_token=vb_token,
)
viber = Api(bot_configuration)


@api_view(['POST'])
@csrf_exempt
def webhook(request):
    post_data = request.body.decode('utf-8')
    logger.debug("received request. post data: {0}".format(post_data))
    viber_request = viber.parse_request(post_data)
    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warning("client failed receiving message. failure: {0}".format(
            viber_request))

    return Response(status=200)