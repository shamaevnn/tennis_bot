from base.models import User, Payment


def check_if_players_not_in_payments(group_id, payments, year, month):
    payment_user_ids = list(payments.values_list('player_id', flat=True))
    users_not_in_payments = User.objects.filter(traininggroup__id=group_id).exclude(id__in=payment_user_ids)
    if users_not_in_payments.exists():
        for player in users_not_in_payments:
            Payment.objects.create(player=player, month=month, year=year)