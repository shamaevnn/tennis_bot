from base.common_for_bots.static_text import ATTENTION, DAYS_AVAILABLE_FOR_GROUP_TRAIN


CANT_TAKE_LESSON_MAX_IN_FUTURE = """
Не могу записать тебя на тренировку, тк максимум в будущем не в свои группы ты можешь записаться на {max_lessons} занятий.
В данный момент {now_count_lessons}
"""

THIS_TRAIN_IS_PAID = f"{ATTENTION}\n <b>Это занятие платное!</b>\n\n"
CHOOSE_TRAIN_TIME_TEMPLATE = "Выбери время занятия на {} ({})."

NO_AVAILABLE_TRAIN_THIS_DAY = (
    "Нет доступных тренировок в этот день, выбери другой.\n"
    f"{DAYS_AVAILABLE_FOR_GROUP_TRAIN}"
)

ADMIN_TEXT_GROUP_TRAIN = (
    f"{ATTENTION}\n"
    "{} {} придёт на гр. тренировку "
    "<b>не за счет отыгрышей, не забудь взять {}₽.</b>\n"
    "{}"
)

ADMIN_TEXT_SINGLE_TRAIN_BONUSS = (
    f"{ATTENTION}\n"
    "{} {} придёт на гр. тренировку "
    "<b>не за счет отыгрышей, не забудь взять {}₽.</b>\n"
    "{}"
)


ADMIN_TEXT_SINGLE_TRAIN_PAY_BONUSS = (
    f"{ATTENTION}\n"
    "{} {} придёт "
    "<b> за счёт платных отыгрышей, не забудь взять {}₽.</b>\n{}"
)

ADMIN_TEXT_GROUP_TRAIN_PAY_BONUSS = (
    f"{ATTENTION}\n"
    "{} {} придёт на гр. "
    "<b> за счёт платных отыгрышей, не забудь взять {}₽.</b>\n{}"
)
ADMIN_TEXT_SINGLE_TRAIN_DOP_TIME = (
    f"{ATTENTION}\n"
    "{} {} придёт "
    "<b>в дополнительное время, не забудь взять {}₽.</b>\n{}"
)


PLAYER_VISIT_GROUP_TRAIN_BONUSS = "{} {} придёт на гр. тренировку за отыгрыш.\n{}"

PLAYER_WRITTEN_TO_TRAIN_SHORT = "Записал тебя на тренировку.\n{}"
PLAYER_WRITTEN_TO_TRAIN = (
    "Записал тебя на тренировку"
    f"{ATTENTION}\n"
    "Не забудь заплатить <b>{}₽</b>\n"
    "{}"
)
