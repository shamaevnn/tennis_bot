from base.models import User, Payment
from functools import wraps

from tele_interface.manage_data import SEND_MESSAGE
from tennis_bot.settings import DEBUG

import sys
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def check_if_players_not_in_payments(group_id, payments, year, month):
    payment_user_ids = list(payments.values_list('player_id', flat=True))
    users_not_in_payments = User.objects.filter(traininggroup__id=group_id).exclude(id__in=payment_user_ids)
    if users_not_in_payments.exists():
        for player in users_not_in_payments:
            Payment.objects.create(player=player, month=month, year=year)


def handle_selecting_groups_to_send_message_to(ids_counter, group_ids, group_id, button_data_text, button_text):
    if group_id not in group_ids:
        text = button_text
    elif ids_counter[group_id] > 1 and ids_counter[group_id] % 2 == 0:
        text = button_text
        group_ids.remove(group_id)
        group_ids.remove(group_id)
        button_data_text = button_data_text[:len(SEND_MESSAGE)] + "|".join(group_ids)
    else:
        text = f'{button_text} ✅'

    return text, button_data_text


def have_not_paid_users_info(payments_values):
    return '\n'.join(
        (
            f"<b>{x['id']}</b>. {x['player__last_name']} {x['player__first_name']} -- {x['n_fact_visiting']} ({x['group_name']})"
            for x in payments_values
        )
    )