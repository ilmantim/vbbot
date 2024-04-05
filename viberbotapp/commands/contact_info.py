from django.db.models import Q

from viberbotapp.bot_config import MAIN_MENU, CONTACT_INFO
from viberbotapp.commands.helper import send_message, send_fallback
from viberbotapp.commands.keyboards import choose_address_keyboard
from viberbotapp.models import Person, Mro


def contact_info(message, chat_id):
    user_message = message.text.title()
    user = Person.objects.get(chat_id=chat_id)
    if user_message.isdigit():
        mro = Mro.objects.get(name=user.context)
        addresses = mro.addresses.all()
        address = addresses.get(num=int(user_message))
        send_message(
            chat_id,
            address.name
        )
        return MAIN_MENU, None
    else:
        mro = Mro.objects.filter(
            Q(name__icontains=f'{user_message} ') | Q(name=user_message)
        ).first()
        if mro:
            send_message(
                chat_id,
                mro.general
            )
            if mro.addresses.count() > 0:
                addresses = [str(i + 1) for i in range(mro.addresses.count())]
                send_message(
                    chat_id,
                    "Выберите номер удобного для Вас МРО в меню снизу",
                    choose_address_keyboard(addresses)
                )
                return CONTACT_INFO, mro.name
        elif 'меню' in message.text.lower():
            pass
        else:
            send_fallback(chat_id)

        return MAIN_MENU, None
