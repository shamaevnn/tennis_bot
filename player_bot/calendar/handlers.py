import re
from datetime import datetime, timedelta, date

from base.common_for_bots.manage_data import CLNDR_IGNORE, CLNDR_DAY, CLNDR_PREV_MONTH, CLNDR_NEXT_MONTH, \
    CLNDR_ACTION_BACK
from base.common_for_bots.utils import separate_callback_data, bot_edit_message, create_calendar
from base.models import User
from player_bot.calendar.manage_data import CLNDR_ACTION_SKIP, CLNDR_ACTION_TAKE_GROUP, CLNDR_ACTION_TAKE_IND, \
    CLNDR_ACTION_TAKE_RENT
from player_bot.skip_lesson.utils import select_tr_days_for_skipping, calendar_skipping
from player_bot.take_lesson.group.calendar import calendar_taking_group_lesson
from player_bot.take_lesson.group.query import get_potential_days_for_group_training
from player_bot.registration.utils import check_status_decor
from player_bot.take_lesson.individual.manage_data import SELECT_PRECISE_IND_TIME
from player_bot.take_lesson.rent.manage_data import SELECT_PRECISE_RENT_TIME
from player_bot.take_lesson.static_text import CHOOSE_DATE_OF_TRAIN
from player_bot.take_lesson.utils import calendar_taking_rent_and_ind_lesson


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
    else:
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
            text = f'{CHOOSE_DATE_OF_TRAIN}\n' \
                   f'✅ -- дни, доступные для групповых тренировок'
        elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
            text = 'Выбери дату индивидуальной тренировки'
        elif re.findall(rf'({CLNDR_ACTION_TAKE_RENT})(\d.\d)', purpose):
            text = 'Выбери дату аренды корта'
        bot_edit_message(context.bot, text, update, create_calendar(purpose, int(year), int(month), highlight_dates))

    else:
        context.bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
    return False, purpose, []


@check_status_decor
def inline_calendar_handler(update, context):
    user, _ = User.get_user_and_created(update, context)
    selected, purpose, date_time = process_calendar_selection(update, context)
    if selected:

        if purpose == CLNDR_ACTION_SKIP:
            text, markup = calendar_skipping(user, purpose, date_time)
        elif purpose == CLNDR_ACTION_TAKE_GROUP:
            text, markup = calendar_taking_group_lesson(user, purpose, date_time)
        elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
            text, markup = calendar_taking_rent_and_ind_lesson(CLNDR_ACTION_TAKE_IND, SELECT_PRECISE_IND_TIME, purpose, date_time)
        elif re.findall(rf'({CLNDR_ACTION_TAKE_RENT})(\d.\d)', purpose):
            text, markup = calendar_taking_rent_and_ind_lesson(CLNDR_ACTION_TAKE_RENT, SELECT_PRECISE_RENT_TIME, purpose, date_time)
        bot_edit_message(context.bot, text, update, markup)