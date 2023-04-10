from base.common_for_bots.static_text import (
    ATTENTION, ATTENTION_2,
    DAYS_AVAILABLE_TO_GROUP_CANCEL,
    DAYS_AVAILABLE_TO_GROUP_TRAIN
    )



PLAYER_CANCELLED_IND_TRAIN = "{}\n{} {} отменил индивидуальную тренировку\n{}"
PLAYER_CANCELLED_RENT_COURT = "{}\n{} {} отменил аренду корта\n{}"
PLAYER_SKIPPED_TRAIN_FOR_BONUS = "{} {} пропускает тренировку за <b>отыгрыш</b>\n{}"
PLAYER_SKIPPED_TRAIN_FOR_MONEY = "{} {} пропускает тренировку за <b>оплату</b>\n{}"
PLAYER_SKIPPED_TRAIN_FOR_PAY_BONUS = (
    "{} {} пропускает тренировку за <b>платный отыгрыш</b>\n{}"
)
PLAYER_SKIPPED_TRAIN_IN_HIS_GROUP = (
    "{} {} пропускает тренировку в <b>своей группе</b>\n{}"
)


SKIP_LESSON_BUTTON = "Пропустить занятие"
CANT_CANCEL_LESSON_TOO_LATE = "Неа, уже нельзя отменить занятие.\nКоличество часов, за которое тебе нужно отменять: {}"
OKAY_TRAIN_CANCELLED = "Окей, занятие отменено.\n{}"
CANCEL_TRAIN_PLUS_BONUS_LESSON = (
    f"{ATTENTION}\n"
    "У тебя есть запись на тренировку на <b> {}.</b>\n"
    "<b>Тренер ее отменил.</b> Но не отчаивайся, я добавлю тебе отыгрыш 🎾"
)

ONLY_ONE_LEFT = (
    f"{ATTENTION_2}\n" "На тренировке в группе {} остался только один игрок\n" "{}"
)
CANT_SKIP_UNAVAILABLE_LESSON = "Занятие отменено тренером, его нельзя пропустить."

CHOOSE_DATE_TO_CANCEL = f"Выбери дату тренировки для отмены.\n {DAYS_AVAILABLE_TO_GROUP_CANCEL}"

TRAIN_CANCELLED_BY_COACH_TEMPLATE = "{} в {} ❌нет тренировки❌, т.к. она отменена тренером, поэтому ее нельзя пропустить."
NO_LESSONS_TO_SKIP = "Пока что нечего пропускать."
INDIVIDUAL_TRAIN_DECOR_TEXT = "🧞‍♂индивидуальная тренировка🧞‍♂️\n"
RENT_COURT_DECOR_TEXT = "💸 аренда корта ️💸\n"
ATTENDING_INFO_TEMPLATE = "Присутствующие:\n{}\n"

SELECT_TIME_TEXT = "Выбери время"

NO_TRAIN_ON_THIS_DAY = (
    f"Нет тренировки в этот день, выбери другой.\n"
    f"{DAYS_AVAILABLE_TO_GROUP_TRAIN}"
)
