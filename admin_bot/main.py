from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    CommandHandler,
    RegexHandler,
    ConversationHandler,
    MessageHandler,
    Filters
)
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()

from tennis_bot.config import ADMIN_TELEGRAM_TOKEN
from admin_bot.handlers import (
    start,
    permission_for_ind_train,
    show_coach_schedule,
    show_traingroupday_info,
    inline_calendar_handler, redirect_to_site, start_payment, cancel, year_payment,
    month_payment, group_payment, change_payment_data, get_id_amount, START_CHANGE_PAYMENT, CONFIRM_OR_CANCEL,
    confirm_or_cancel_changing_payment
)
from tele_interface.manage_data import (
    PERMISSION_FOR_IND_TRAIN,
    ADMIN_TIME_SCHEDULE_BUTTON,
    SHOW_GROUPDAY_INFO, ADMIN_SITE, ADMIN_PAYMENT, PAYMENT_YEAR, PAYMENT_YEAR_MONTH, PAYMENT_YEAR_MONTH_GROUP,
    CLNDR_ADMIN_VIEW_SCHEDULE, PAYMENT_START_CHANGE, PAYMENT_CONFIRM_OR_CANCEL
)

payment_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(change_payment_data, pattern=f'{PAYMENT_START_CHANGE}')],

    states={
        START_CHANGE_PAYMENT: [MessageHandler(Filters.text, get_id_amount)],
        CONFIRM_OR_CANCEL: [CallbackQueryHandler(confirm_or_cancel_changing_payment, pattern=f"^{PAYMENT_CONFIRM_OR_CANCEL}")]
    },

    fallbacks=[CommandHandler('cancel', cancel),
               CallbackQueryHandler(month_payment, pattern='^{}'.format(PAYMENT_YEAR_MONTH))]

)


def add_handlers(updater):
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(payment_handler)
    dp.add_handler(CallbackQueryHandler(permission_for_ind_train, pattern='^{}'.format(PERMISSION_FOR_IND_TRAIN)))
    dp.add_handler(RegexHandler(fr'^{ADMIN_TIME_SCHEDULE_BUTTON}$', show_coach_schedule))
    dp.add_handler(RegexHandler(f'{ADMIN_SITE}', redirect_to_site))
    dp.add_handler(RegexHandler(f'{ADMIN_PAYMENT}', start_payment))
    dp.add_handler(CallbackQueryHandler(start_payment, pattern=f'^{ADMIN_PAYMENT}'))
    dp.add_handler(CallbackQueryHandler(show_traingroupday_info, pattern='^{}'.format(SHOW_GROUPDAY_INFO)))
    dp.add_handler(CallbackQueryHandler(year_payment, pattern='^{}'.format(PAYMENT_YEAR)))
    dp.add_handler(CallbackQueryHandler(month_payment, pattern='^{}'.format(PAYMENT_YEAR_MONTH)))
    dp.add_handler(CallbackQueryHandler(group_payment, pattern='^{}'.format(PAYMENT_YEAR_MONTH_GROUP)))
    dp.add_handler(CallbackQueryHandler(inline_calendar_handler, pattern='^{}'.format(CLNDR_ADMIN_VIEW_SCHEDULE)))


def main():
    updater = Updater(ADMIN_TELEGRAM_TOKEN)
    add_handlers(updater)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()