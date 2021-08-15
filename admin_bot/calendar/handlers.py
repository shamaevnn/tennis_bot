from datetime import date, timedelta

from admin_bot.calendar.keyboard_utils import day_buttons_coach_info
from admin_bot.calendar.static_text import TRAIN_DAYS, NO_TRAINS_THIS_DAY
from base.models import GroupTrainingDay
from base.common_for_bots.utils import bot_edit_message, get_time_info_from_tr_day, create_calendar, \
    separate_callback_data
from base.common_for_bots import manage_data
from admin_bot.view_schedule.manage_data import SHOW_GROUPDAY_INFO, CLNDR_ADMIN_VIEW_SCHEDULE


def admin_calendar_selection(bot, update):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    """
    query = update.callback_query
    (purpose, action, year, month, day) = separate_callback_data(query.data)
    curr = date(int(year), int(month), 1)

    if action == manage_data.CLNDR_IGNORE:
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == manage_data.CLNDR_DAY:
        bot_edit_message(bot, query.message.text, update)
        return True, purpose, date(int(year), int(month), int(day))
    elif action == manage_data.CLNDR_PREV_MONTH:
        pre = curr - timedelta(days=1)
        bot_edit_message(bot, query.message.text, update, create_calendar(purpose, int(pre.year), int(pre.month)))
    elif action == manage_data.CLNDR_NEXT_MONTH:
        ne = curr + timedelta(days=31)
        bot_edit_message(bot, query.message.text, update, create_calendar(purpose, int(ne.year), int(ne.month)))
    elif action == manage_data.CLNDR_ACTION_BACK:
        if purpose == CLNDR_ADMIN_VIEW_SCHEDULE:
            text = TRAIN_DAYS
        else:
            text = TRAIN_DAYS
        bot_edit_message(bot, text, update, create_calendar(purpose, int(year), int(month)))
    else:
        bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
    return False, purpose, []


def inline_calendar_handler(update, context):
    selected, purpose, date_my = admin_calendar_selection(context.bot, update)
    if selected:
        if purpose == CLNDR_ADMIN_VIEW_SCHEDULE:
            tr_days = GroupTrainingDay.objects.filter(date=date_my).select_related('group').order_by('start_time')
            if tr_days.exists():
                markup = day_buttons_coach_info(tr_days, SHOW_GROUPDAY_INFO)
                _, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_days.first())
                text = '📅{} ({})'.format(date_tlg, day_of_week)
            else:
                text = NO_TRAINS_THIS_DAY
                markup = create_calendar(purpose, date_my.year, date_my.month)
            bot_edit_message(context.bot, text, update, markup)


def show_coach_schedule(update, context):
    update.message.reply_text(
        text=TRAIN_DAYS,
        reply_markup=create_calendar(CLNDR_ADMIN_VIEW_SCHEDULE)
    )