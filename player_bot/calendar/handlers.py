import re
from datetime import datetime, timedelta, date

from base.common_for_bots.manage_data import CLNDR_IGNORE, CLNDR_DAY, CLNDR_PREV_MONTH, CLNDR_NEXT_MONTH, \
    CLNDR_ACTION_BACK
from base.common_for_bots.utils import separate_callback_data, bot_edit_message, create_calendar
from base.models import User
from player_bot.calendar.manage_data import CLNDR_ACTION_SKIP, CLNDR_ACTION_TAKE_GROUP, CLNDR_ACTION_TAKE_IND
from player_bot.skip_lesson.utils import select_tr_days_for_skipping, calendar_skipping
from player_bot.take_lesson.utils import get_potential_days_for_group_training, calendar_taking_lesson, \
    calendar_taking_ind_lesson
from player_bot.registration.utils import check_status_decor


def process_calendar_selection(update, context):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    """
    user, _ = User.get_user_and_created(update, context)

    query = update.callback_query
    (purpose, action, year, month, day) = separate_callback_data(query.data)
    curr = datetime(int(year), int(month), 1)

    if purpose == CLNDR_ACTION_SKIP:
        highlight_dates = list(select_tr_days_for_skipping(user).values_list('date', flat=True))
    elif purpose == CLNDR_ACTION_TAKE_GROUP:
        training_days = get_potential_days_for_group_training(user)
        highlight_dates = list(training_days.values_list('date', flat=True))
    elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
        highlight_dates = None

    if action == CLNDR_IGNORE:
        context.bot.answer_callback_query(callback_query_id=query.id)
    # elif action == CLNDR_CHANGE_FREE_OR_FOR_MONEY:
    #     pass
    elif action == CLNDR_DAY:
        bot_edit_message(context.bot, query.message.text, update)
        return True, purpose, datetime(int(year), int(month), int(day))
    elif action == CLNDR_PREV_MONTH:
        pre = curr - timedelta(days=1)
        bot_edit_message(context.bot, query.message.text, update, create_calendar(purpose, int(pre.year), int(pre.month),
                                                                          highlight_dates))
    elif action == CLNDR_NEXT_MONTH:
        ne = curr + timedelta(days=31)
        bot_edit_message(context.bot, query.message.text, update, create_calendar(purpose, int(ne.year), int(ne.month),
                                                                          highlight_dates))
    elif action == CLNDR_ACTION_BACK:
        if purpose == CLNDR_ACTION_SKIP:
            text = 'Выбери дату тренировки для отмены.\n' \
                   '✅ -- дни, доступные для отмены.'
        elif purpose == CLNDR_ACTION_TAKE_GROUP:
            text = 'Выбери дату тренировки\n' \
                   '✅ -- дни, доступные для групповых тренировок'
        elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
            text = 'Выбери дату индивидуальной тренировки'
        bot_edit_message(context.bot, text, update, create_calendar(purpose, int(year), int(month), highlight_dates))

    else:
        context.bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
    return False, purpose, []


@check_status_decor
def inline_calendar_handler(update, context):
    user, _ = User.get_user_and_created(update, context)
    selected, purpose, date_my = process_calendar_selection(update, context)
    if selected:
        date_comparison = date(date_my.year, date_my.month, date_my.day)
        if purpose == CLNDR_ACTION_SKIP:
            text, markup = calendar_skipping(user, purpose, date_my)
        elif purpose == CLNDR_ACTION_TAKE_GROUP:
            text, markup = calendar_taking_lesson(user, purpose, date_my, date_comparison)
        elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
            text, markup = calendar_taking_ind_lesson(purpose, date_my, date_comparison)
        bot_edit_message(context.bot, text, update, markup)