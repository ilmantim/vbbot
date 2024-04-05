from viberbotapp.bot_config import MAIN_MENU, FAVORITES
from viberbotapp.commands.helper import send_fallback, send_message
from viberbotapp.commands.keyboards import delete_bills_keyboard, \
    show_bills_keyboard
from viberbotapp.models import Person


def favorites(message, chat_id, info):
    user_message = message.text.lower()
    if user_message.isdigit() and user_message in info:
        user, created = Person.objects.get_or_create(
            chat_id=chat_id
        )
        user.favorites.get(bill__value=int(user_message)).delete()
        send_message(
            chat_id,
            f'Лицевой счет {user_message} удален из вашего списка.'
        )
        state = MAIN_MENU
    elif 'удалить' in user_message:
        send_message(
            chat_id,
            "Выберите лицевой счёт, который Вы хотите удалить.",
            delete_bills_keyboard(info)
        )
        state = FAVORITES
    elif 'назад' in user_message:
        all_bills = '\n'.join(info)
        send_message(
            chat_id,
            f'Ваши лицевые счета:\n{all_bills}',
            'Выберите нужный пункт в меню снизу.',
            show_bills_keyboard()
        )
        state = FAVORITES
    elif 'меню' in user_message:
        state = MAIN_MENU
    else:
        state = send_fallback(chat_id)

    return state
