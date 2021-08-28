from django.db.models import QuerySet

from base.models import User


def schedule_users_info(users: QuerySet[User]):
    return '\n'.join((
        f"{i + 1}. {x['last_name']} {x['first_name']}"
        for i, x in enumerate(users.values('first_name', 'last_name').order_by('last_name'))
    ))
