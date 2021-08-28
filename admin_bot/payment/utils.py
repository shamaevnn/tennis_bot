from django.db.models import QuerySet

from base.models import User, Payment


def check_if_players_not_in_payments(group_id, payments, year, month):
    payment_user_ids = list(payments.values_list('player_id', flat=True))
    users_not_in_payments = User.objects.filter(traininggroup__id=group_id).exclude(id__in=payment_user_ids)
    if users_not_in_payments.exists():
        for player in users_not_in_payments:
            Payment.objects.create(player=player, month=month, year=year)


def have_not_paid_users_info(payments_values):
    return '\n'.join(
        (
            f"<b>{x['id']}</b>. {x['player__last_name']} {x['player__first_name']} -- {x['n_fact_visiting']} ({x['group_name']})"
            for x in payments_values
        )
    )


def payment_users_info(users: QuerySet[Payment]):
    return '\n'.join((
        f"<b>{x['id']}</b>. {x['player__last_name']} {x['player__first_name']} -- {x['fact_amount']}₽, {x['n_fact_visiting']}"
        for x in users.values(
            'player__first_name', 'player__last_name', 'fact_amount', 'n_fact_visiting', 'id'
        ).order_by(
                'player__last_name',
                'player__first_name'
        ))
    )
