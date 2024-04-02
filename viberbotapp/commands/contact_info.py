from viberbot.api.messages import TextMessage

from viberbotapp.bot_config import viber
from viberbotapp.commands.keyboards import choose_address_keyboard
from viberbotapp.models import Person, Mro


START, MAIN_MENU, SUBMIT_READINGS, METER_INFO, FAVORITES, CONTACT_INFO = range(
    6)


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
