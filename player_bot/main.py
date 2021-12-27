import django
import os

from player_bot.errors.handlers import send_stacktrace_to_tg_chat

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennis_bot.settings")
django.setup()
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
    Dispatcher,
)

import telegram

from player_bot.calendar.handlers import inline_calendar_handler
from player_bot.player_info.handlers import player_main_info
from player_bot.registration.handlers import get_first_last_name, get_phone_number
from player_bot.skip_lesson.handlers import (
    skip_lesson_main_menu_button,
    skip_lesson_when_geq_2,
    skip_lesson,
)
from player_bot.take_lesson.handlers import (
    choose_type_of_training,
    take_lesson,
)
from player_bot.take_lesson.rent.handlers import (
    select_dt_for_rent_lesson,
    select_rent_time,
    take_rent_info_train,
    take_rent,
)
from player_bot.take_lesson.rent.manage_data import (
    SELECT_DURATION_FOR_RENT,
    SELECT_PRECISE_RENT_TIME,
    NUMBER_OF_PEOPLE_TO_RENT_CORT,
    TAKE_RENT_LESSON,
)
from player_bot.take_lesson.group.handlers import (
    select_group_time,
    confirm_group_lesson,
    choose_type_of_payment_for_pay_visiting,
)
from player_bot.take_lesson.individual.handlers import (
    select_dt_for_ind_lesson,
    select_ind_time,
)
from player_bot.menu_and_commands.handlers import (
    start,
    cancel,
    get_help,
    INSERT_FIO,
    INSERT_PHONE_NUMBER,
)
from tennis_bot.celery import app
from player_bot.skip_lesson.manage_data import (
    SELECT_SKIP_TIME_BUTTON,
    SHOW_INFO_ABOUT_SKIPPING_DAY,
)
from player_bot.take_lesson.manage_data import SELECT_TRAINING_TYPE
from player_bot.take_lesson.group.manage_data import (
    SELECT_PRECISE_GROUP_TIME,
    CONFIRM_GROUP_LESSON,
    PAYMENT_VISITING,
)
from player_bot.take_lesson.individual.manage_data import (
    SELECT_DURATION_FOR_IND_TRAIN,
    SELECT_PRECISE_IND_TIME,
)
from player_bot.take_lesson.static_text import TAKE_LESSON_BUTTON
from player_bot.skip_lesson.static_text import SKIP_LESSON_BUTTON
from player_bot.menu_and_commands.static_text import HELP_BUTTON
from player_bot.player_info.static_text import MY_DATA_BUTTON
from tennis_bot.settings import TELEGRAM_TOKEN

registration_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        INSERT_FIO: [MessageHandler(Filters.regex(r"^\w+\s\w+$"), get_first_last_name)],
        INSERT_PHONE_NUMBER: [
            MessageHandler(Filters.regex(r"^\d+$"), get_phone_number)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)


def setup_dispatcher(dp):
    dp.add_handler(registration_handler)

    # главное меню
    dp.add_handler(
        MessageHandler(Filters.regex(SKIP_LESSON_BUTTON), skip_lesson_main_menu_button)
    )
    dp.add_handler(
        MessageHandler(Filters.regex(TAKE_LESSON_BUTTON), choose_type_of_training)
    )
    dp.add_handler(MessageHandler(Filters.regex(MY_DATA_BUTTON), player_main_info))
    dp.add_handler(MessageHandler(Filters.regex(HELP_BUTTON), get_help))

    dp.add_handler(
        CallbackQueryHandler(choose_type_of_training, pattern=f"^{TAKE_LESSON_BUTTON}")
    )

    # групповые тренировки
    dp.add_handler(
        CallbackQueryHandler(confirm_group_lesson, pattern=f"^{CONFIRM_GROUP_LESSON}")
    )
    dp.add_handler(
        CallbackQueryHandler(take_lesson, pattern=f"^{SELECT_TRAINING_TYPE}")
    )
    dp.add_handler(
        CallbackQueryHandler(select_group_time, pattern=f"^{SELECT_PRECISE_GROUP_TIME}")
    )
    dp.add_handler(
        CallbackQueryHandler(
            choose_type_of_payment_for_pay_visiting, pattern=f"^{PAYMENT_VISITING}"
        )
    )

    # индивидуальные тренировки
    dp.add_handler(
        CallbackQueryHandler(
            select_dt_for_ind_lesson, pattern=f"^{SELECT_DURATION_FOR_IND_TRAIN}"
        )
    )
    dp.add_handler(
        CallbackQueryHandler(select_ind_time, pattern=f"^{SELECT_PRECISE_IND_TIME}")
    )

    # арендовать корт
    dp.add_handler(
        CallbackQueryHandler(
            select_dt_for_rent_lesson, pattern=f"^{SELECT_DURATION_FOR_RENT}"
        )
    )
    dp.add_handler(
        CallbackQueryHandler(select_rent_time, pattern=f"^{SELECT_PRECISE_RENT_TIME}")
    )
    dp.add_handler(
        CallbackQueryHandler(
            take_rent_info_train, pattern=f"^{NUMBER_OF_PEOPLE_TO_RENT_CORT}"
        )
    )
    dp.add_handler(CallbackQueryHandler(take_rent, pattern=f"^{TAKE_RENT_LESSON}"))

    # пропустить тренировку
    dp.add_handler(
        CallbackQueryHandler(skip_lesson, pattern=f"^{SHOW_INFO_ABOUT_SKIPPING_DAY}")
    )
    dp.add_handler(
        CallbackQueryHandler(
            skip_lesson_when_geq_2, pattern=f"^{SELECT_SKIP_TIME_BUTTON}"
        )
    )

    # календарь
    dp.add_handler(CallbackQueryHandler(inline_calendar_handler))

    # handling errors
    dp.add_error_handler(send_stacktrace_to_tg_chat)

    return dp


def main():
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")

    updater.start_polling()
    updater.idle()


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher_bot.process_update(update)


bot = telegram.Bot(TELEGRAM_TOKEN)
dispatcher_bot = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))


if __name__ == "__main__":
    main()
