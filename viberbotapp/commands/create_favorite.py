from viberbotapp.models import Favorite, Person, Bill


def create_favorite(message, chat_id):
    user_message = message.text.title()
    user, created = Person.objects.get_or_create(
        chat_id=chat_id
    )
    bill = Bill.objects.get(value=user.context)
    bill.persons.add(user)
    if user_message == 'Да':
        Favorite.objects.create(person=user, bill=bill)

    return user.prev_step
