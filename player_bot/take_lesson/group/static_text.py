from base.common_for_bots.static_text import ATTENTION, DAYS_AVAILABLE_TO_GROUP_TRAIN


CANT_TAKE_LESSON_MAX_IN_FUTURE = """
Не могу записать тебя на тренировку, тк максимум в будущем не в свои группы ты можешь записаться на {max_lessons} занятий.
В данный момент {now_count_lessons}
"""

THIS_TRAIN_IS_PAID = f"{ATTENTION}\n <b>Это занятие платное!</b>\n\n"
CHOOSE_TRAIN_TIME_TEMPLATE = "Выбери время занятия на {} ({})."

NO_AVAILABLE_TRAIN_THIS_DAY = (
    "Нет доступных тренировок в этот день, выбери другой.\n"
    f"{DAYS_AVAILABLE_TO_GROUP_TRAIN}"
)

SIGNED_TO_TRAIN_TEMPLATE_PAYMENT =  (
            f"Записал тебя на тренировку\n"
            f"{ATTENTION}\n"
            "Не забудь заплатить <b>{}₽</b>\n{}"
            )

