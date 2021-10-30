YES = 'Да'
NO = 'Нет'
WILL_SAY_RENT_COURT_IS_CANCELLED = 'Хорошо, сообщу {last_name} {first_name}, что аренда корта отменена.\n{date_info}'
WILL_SAY_RENT_IS_ACCEPTED = 'Хорошо, сообщу {last_name} {first_name}, что можно арендовать корт.\n{date_info}'
RENT_COURT_IS_ALREADY_CANCELLED = 'Аренда корта уже отменена.'

PLAYER_WANTS_TO_RENT_COURT = """
<b>{first_name} {last_name} — {phone_number}</b>
Хочет арендовать корт на <b>{n_players} игроков</b> за <b>{price}₽</b>

<b>Разрешить?</b>

{date_info}
"""