from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters, Dispatcher
)
import os
import django

from tennis_bot.celery import app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()
import telegram


from tennis_bot.settings import ADMIN_TELEGRAM_TOKEN
from admin_bot.go_to_site.handlers import redirect_to_site
from admin_bot.calendar.handlers import inline_calendar_handler, show_coach_schedule
from admin_bot.ind_train.handlers import permission_for_ind_train, save_many_ind_trains
from admin_bot.view_schedule.handlers import show_trainingroupday_info
from admin_bot.send_message import handlers as send_message_handlers
from admin_bot.payment import handlers as payment_handlers
from admin_bot.menu_and_commands.handlers import start, cancel
from admin_bot.send_message.manage_data import SEND_MESSAGE
from admin_bot.view_schedule.manage_data import SHOW_GROUPDAY_INFO, CLNDR_ADMIN_VIEW_SCHEDULE
from admin_bot.ind_train.manage_data import PERMISSION_FOR_IND_TRAIN, AMOUNT_OF_IND_TRAIN
from admin_bot.payment.manage_data import PAYMENT_YEAR, PAYMENT_YEAR_MONTH, PAYMENT_YEAR_MONTH_GROUP, \
    PAYMENT_START_CHANGE, PAYMENT_CONFIRM_OR_CANCEL
from admin_bot.view_schedule.static_text import ADMIN_TIME_SCHEDULE_BUTTON
from admin_bot.send_message.static_text import ADMIN_SEND_MESSAGE
from admin_bot.go_to_site.static_text import ADMIN_SITE
from admin_bot.payment.static_text import ADMIN_PAYMENT

payment_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(payment_handlers.change_payment_data, pattern=f'{PAYMENT_START_CHANGE}')],
    states={
        payment_handlers.START_CHANGE_PAYMENT: [MessageHandler(Filters.text, payment_handlers.get_id_amount)],
        payment_handlers.CONFIRM_OR_CANCEL: [
            CallbackQueryHandler(
                payment_handlers.confirm_or_cancel_changing_payment, pattern=f"^{PAYMENT_CONFIRM_OR_CANCEL}"
            )
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        CallbackQueryHandler(payment_handlers.month_payment, pattern='^{}'.format(PAYMENT_YEAR_MONTH))
    ]

)
send_message_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(send_message_handlers.select_groups_where_should_send, pattern=f'^{SEND_MESSAGE}'),
        MessageHandler(Filters.regex(f'{ADMIN_SEND_MESSAGE}'), send_message_handlers.select_groups_where_should_send)
    ],
    states={
        send_message_handlers.GROUP_IDS: [
            CallbackQueryHandler(send_message_handlers.text_to_send, pattern=f"^{SEND_MESSAGE}")
        ],
        send_message_handlers.TEXT_TO_SEND: [MessageHandler(Filters.text, send_message_handlers.receive_text_and_send)]
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        CallbackQueryHandler(payment_handlers.month_payment, pattern='^{}'.format(PAYMENT_YEAR_MONTH))
    ]
)


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(send_message_handler)
    dp.add_handler(payment_handler)

    # ind train
    dp.add_handler(CallbackQueryHandler(permission_for_ind_train, pattern='^{}'.format(PERMISSION_FOR_IND_TRAIN)))
    dp.add_handler(CallbackQueryHandler(save_many_ind_trains, pattern='^{}'.format(AMOUNT_OF_IND_TRAIN)))

    # main menu
    dp.add_handler(MessageHandler(Filters.regex(fr'^{ADMIN_TIME_SCHEDULE_BUTTON}$'), show_coach_schedule))
    dp.add_handler(MessageHandler(Filters.regex(f'{ADMIN_SITE}'), redirect_to_site))
    dp.add_handler(MessageHandler(Filters.regex(f'{ADMIN_PAYMENT}'), payment_handlers.start_payment))
    dp.add_handler(CallbackQueryHandler(payment_handlers.start_payment, pattern=f'^{ADMIN_PAYMENT}'))

    # payment
    dp.add_handler(CallbackQueryHandler(show_trainingroupday_info, pattern='^{}'.format(SHOW_GROUPDAY_INFO)))
    dp.add_handler(CallbackQueryHandler(payment_handlers.year_payment, pattern='^{}'.format(PAYMENT_YEAR)))
    dp.add_handler(CallbackQueryHandler(payment_handlers.month_payment, pattern='^{}'.format(PAYMENT_YEAR_MONTH)))
    dp.add_handler(CallbackQueryHandler(payment_handlers.group_payment, pattern='^{}'.format(PAYMENT_YEAR_MONTH_GROUP)))

    # calendar
    dp.add_handler(CallbackQueryHandler(inline_calendar_handler, pattern='^{}'.format(CLNDR_ADMIN_VIEW_SCHEDULE)))

    return dp


def main():
    updater = Updater(ADMIN_TELEGRAM_TOKEN)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(ADMIN_TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")

    updater.start_polling()
    updater.idle()


@app.task(ignore_result=True)
def process_admin_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, admin_bot)
    dispatcher_admin.process_update(update)


admin_bot = telegram.Bot(ADMIN_TELEGRAM_TOKEN)
dispatcher_admin = setup_dispatcher(Dispatcher(admin_bot, None, workers=0, use_context=True))


if __name__ == '__main__':
    main()