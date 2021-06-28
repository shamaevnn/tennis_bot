import django
import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
# django.setup()
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters, Dispatcher
)

import telegram

from tele_interface.handlers import (
    get_help,
    inline_calendar_handler, INSERT_FIO,
    INSERT_PHONE_NUMBER, )
from tele_interface.user_info.handlers import user_main_info
from tele_interface.onboarding import get_first_last_name, get_phone_number
from tele_interface.skip_lesson.handlers import skip_lesson_main_menu_button, skip_lesson_when_geq_2, skip_lesson
from tele_interface.take_lesson.handlers import choose_type_of_training, take_lesson, select_dt_for_ind_lesson, \
    select_precise_ind_lesson_time, select_precise_group_lesson_time, confirm_group_lesson, \
    choose_type_of_payment_for_pay_visiting
from tele_interface.commands import start, cancel
from tennis_bot.celery import app
from tele_interface.manage_data import (
    SELECT_PRECISE_GROUP_TIME,
    SELECT_TRAINING_TYPE,
    SELECT_DURATION_FOR_IND_TRAIN,
    SELECT_PRECISE_IND_TIME,
    CONFIRM_GROUP_LESSON,
    SHOW_INFO_ABOUT_SKIPPING_DAY,
    SELECT_SKIP_TIME_BUTTON, PAYMENT_VISITING,
)
from tele_interface.static_text import TAKE_LESSON_BUTTON, MY_DATA_BUTTON, SKIP_LESSON_BUTTON, HELP_BUTTON
from tennis_bot.settings import TELEGRAM_TOKEN

registration_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],

    states={
        INSERT_FIO: [MessageHandler(Filters.regex(r'^\w+\s\w+$'), get_first_last_name)],
        INSERT_PHONE_NUMBER: [MessageHandler(Filters.regex(r'^\d+$'), get_phone_number)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]

)


def setup_dispatcher(dp):

    dp.add_handler(registration_handler)

    dp.add_handler(MessageHandler(Filters.regex(SKIP_LESSON_BUTTON), skip_lesson_main_menu_button))
    dp.add_handler(MessageHandler(Filters.regex(TAKE_LESSON_BUTTON), choose_type_of_training))
    dp.add_handler(MessageHandler(Filters.regex(MY_DATA_BUTTON), user_main_info))
    dp.add_handler(MessageHandler(Filters.regex(HELP_BUTTON), get_help))

    dp.add_handler(CallbackQueryHandler(select_precise_group_lesson_time,
                                        pattern='^{}'.format(SELECT_PRECISE_GROUP_TIME)))
    dp.add_handler(CallbackQueryHandler(take_lesson,
                                        pattern='^{}'.format(SELECT_TRAINING_TYPE)))
    dp.add_handler(CallbackQueryHandler(select_dt_for_ind_lesson,
                                        pattern='^{}'.format(SELECT_DURATION_FOR_IND_TRAIN)))
    dp.add_handler(CallbackQueryHandler(select_precise_ind_lesson_time,
                                        pattern='^{}'.format(SELECT_PRECISE_IND_TIME)))
    dp.add_handler(CallbackQueryHandler(choose_type_of_training,
                                        pattern='^{}'.format(TAKE_LESSON_BUTTON)))
    dp.add_handler(CallbackQueryHandler(confirm_group_lesson,
                                        pattern='^{}'.format(CONFIRM_GROUP_LESSON)))
    dp.add_handler(CallbackQueryHandler(skip_lesson,
                                        pattern='^{}'.format(SHOW_INFO_ABOUT_SKIPPING_DAY)))
    dp.add_handler(CallbackQueryHandler(skip_lesson_when_geq_2,
                                        pattern='^{}'.format(SELECT_SKIP_TIME_BUTTON)))
    dp.add_handler(CallbackQueryHandler(choose_type_of_payment_for_pay_visiting,
                                        pattern='^{}'.format(PAYMENT_VISITING)))
    dp.add_handler(CallbackQueryHandler(inline_calendar_handler))

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


if __name__ == '__main__':
    main()
