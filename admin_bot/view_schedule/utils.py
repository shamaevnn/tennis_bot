from django.db.models import QuerySet

from base.models import Player


def schedule_players_info(player: QuerySet[Player]):
    return '\n'.join((
        f"{i + 1}. {x['last_name']} {x['first_name']}"
        for i, x in enumerate(player.values('first_name', 'last_name').order_by('last_name'))
    ))
