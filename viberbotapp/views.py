import json

from rest_framework import generics, serializers
from .models import Mro
from django.views.decorators.csrf import csrf_exempt
from viberbot.api.bot_configuration import BotConfiguration
from viberbot import Api
from django.http import HttpResponse
from environs import Env


env = Env()
env.read_env()


class MroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mro
        fields = '__all__'


class Mros(generics.ListCreateAPIView):
    queryset = Mro.objects.all()
    serializer_class = MroSerializer


BASE_URL = 'https://ab10-178-155-5-88.ngrok-free.app'
vb_token = env.str('VB_TOKEN')

bot_configuration = BotConfiguration(
    name="ch-sk bot",
    avatar=None,
    auth_token=vb_token,
)
viber_api = Api(bot_configuration)


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        viber = json.loads(request.body.decode('utf-8'))
        print(viber)
        if viber['event'] == 'webhook':
            print(viber)
            print("Webhook успешно установлен")
            return HttpResponse(status=200)
        else:
            print("Это не Webhook - пробуй еще раз")
            return HttpResponse(status=500)
