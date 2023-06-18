from typing import Dict

from django.db.models import QuerySet

from base.models import Payment, Player


def check_if_players_not_in_payments(group_id, payments, year, month):
    payment_player_ids = list(payments.values_list("player_id", flat=True))
    players_not_in_payments = Player.objects.filter(traininggroup__id=group_id).exclude(
        id__in=payment_player_ids
    )
    if players_not_in_payments.exists():
        for player in players_not_in_payments:
            Payment.objects.create(player=player, month=month, year=year)


def have_not_paid_players_info(payments_values: QuerySet[Dict]):
    return "\n".join(
        (
            f"<b>{x['id']}</b>. {x['player__last_name']} {x['player__first_name']} — {x['n_fact_visiting']} ({x['group_name']})"
            for x in payments_values
        )
    )


def payment_players_info(payments_values: QuerySet[Dict]):
    return "\n".join(
        (
            f"<b>{x['id']}</b>. {x['player__last_name']} {x['player__first_name']} — {x['fact_amount']}₽, {x['n_fact_visiting']}"
            for x in payments_values
        )
    )
