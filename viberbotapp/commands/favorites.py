from viberbot.api.messages import TextMessage

from viberbotapp.bot_config import viber, MAIN_MENU, FAVORITES
from viberbotapp.commands.keyboards import delete_bills_keyboard, \
    show_bills_keyboard
from viberbotapp.commands.main_menu import send_fallback
from viberbotapp.models import Person


def favorites(message, chat_id, info):
    user_message = message.text.lower()
    if user_message.isdigit() and user_message in info:
        user, created = Person.objects.get_or_create(
            chat_id=chat_id
        )
        user.favorites.get(bill__value=int(user_message)).delete()
        viber.send_messages(chat_id, [
            TextMessage(
                text=
                f'Лицевой счет {user_message} удален из вашего списка.'
            )
        ])
        state = MAIN_MENU
    elif 'удалить' in user_message:
        viber.send_messages(chat_id, [
            TextMessage(
                text=
                "Выберите лицевой счёт, который Вы хотите удалить."
            ),
            delete_bills_keyboard(info)
        ])
        state = FAVORITES
    elif 'назад' in user_message:
        all_bills = '\n'.join(info)
        viber.send_messages(chat_id, [
            TextMessage(text=f'Ваши лицевые счета:\n{all_bills}'),
            TextMessage(text='Выберите нужный пункт в меню снизу.'),
            show_bills_keyboard(),
        ])
        state = FAVORITES
    elif 'меню' in user_message:
        state = MAIN_MENU
    else:
        state = send_fallback(chat_id)

    return state
