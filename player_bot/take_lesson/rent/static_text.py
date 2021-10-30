HOW_MANY_PEOPLE_WILL_COME = 'Сколько человек придет на занятие?'
TRAIN_RENT_INFO = """
Аренда на {n_players} игроков будет стоить <b>{price}₽</b>

📅Дата: <b>{date} ({day_of_week})</b>
⏰Время: <b>{start_time} — {end_time}</b>
"""

RENT_KORT = 'Арендовать корт'

WILL_SAY_TO_COACH_ABOUT_RENTING = """
Сообщу тренеру, что ты хочешь арендовать корт за <b>{price}₽</b> на {n_players} игроков

📅Дата: <b>{date} ({day_of_week})</b>
⏰Время: <b>{start_time} — {end_time}</b>
"""

COACH_ACCEPTED_RENT_KORT = """
Отлично, тренер подтвердил, что можно арендовать корт, не забудь!
{date_info}
"""
COACH_CANCELLED_RENT_CORT = """
{attention}
Аренда корта <b>ОТМЕНЕНА</b>
{date_info}
"""