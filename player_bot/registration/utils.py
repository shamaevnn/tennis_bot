from base.models import Player
from player_bot.registration.static_text import COACH_HAVE_NOT_CONFIRMED_YET


def check_status_decor(func):
    def wrapper(update, context):
        res = None
        player, _ = Player.get_player_and_created(update, context)
        if player.status != Player.STATUS_WAITING and player.status != Player.STATUS_FINISHED:
            res = func(update, context)
        else:
            context.bot.send_message(player.id, COACH_HAVE_NOT_CONFIRMED_YET)
        return res

    return wrapper
