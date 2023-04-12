from base.common_for_bots.static_text import ATTENTION, DAYS_AVAILABLE_FOR_GROUP_TRAIN
from tennis_bot.settings import TARIF_ARBITRARY


TAKE_LESSON_BUTTON = "Записаться на занятие"
CHOOSE_TYPE_OF_TRAIN = "Выбери тип тренировки."
TYPE_IND = "Индивидуальная 🏌️"
TYPE_GROUP = "Групповая 🧑‍🤝‍🧑🧑‍🤝‍🧑"
TYPE_RENT = "Аренда корта 🧑‍🤝‍🧑💸"
CHOOSE_DATE_OF_TRAIN = "Выбери дату тренировки."
CHOOSE_TIME = "Выбери время"

NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER = (
    "Упс, похоже уже не осталось свободных мест на это время, выбери другое."
)
CHOOSE_TYPE_OF_PAYMENT = "Выбери тип оплаты"

CHOOSE_DURATION_OF_TRAIN = "Выбери продолжительность занятия"

CANT_TAKE_TRAIN_CHOOSE_ANOTHER_DAY = "Нельзя записаться на этот день, выбери другой."
NO_GAMES_IN_MOMENT = (
    f"{ATTENTION}\n"
    f"В данный момент у тебя нет отыгрышей.\n"
    f"<b> Занятие будет стоить {TARIF_ARBITRARY}₽ </b>\n"
    f"{DAYS_AVAILABLE_FOR_GROUP_TRAIN}"
)

YOU_SACRIFICE_ONE_GAME = (
    f"<b>Пожертвуешь одним отыгрышем.</b>\n"
    f"{DAYS_AVAILABLE_FOR_GROUP_TRAIN}"
)

