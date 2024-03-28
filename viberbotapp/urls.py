from django.urls import path
from .views import webhook, Mros

urlpatterns = [
    path('api/mros/', Mros.as_view(), name='Mros'),
    path('', webhook, name='viber_webhook'),
]
