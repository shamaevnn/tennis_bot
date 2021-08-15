import base.common_for_bots
from base.models import User
from player_bot.registration.static_text import COACH_HAVE_NOT_CONFIRMED_YET


def check_status_decor(func):
    def wrapper(update, context):
        res = None
        user, _ = User.get_user_and_created(update, context)
        if user.status != User.STATUS_WAITING and user.status != User.STATUS_FINISHED:
            res = func(update, context)
        else:
            base.common_for_bots.utils.send_message(user.id, COACH_HAVE_NOT_CONFIRMED_YET)
        return res

    return wrapper