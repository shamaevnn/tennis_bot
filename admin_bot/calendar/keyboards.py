from django.db.models import QuerySet
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.common_for_bots.utils import get_time_info_from_tr_day, create_callback_data
from base.common_for_bots.manage_data import CLNDR_ACTION_BACK
from admin_bot.view_schedule.manage_data import CLNDR_ADMIN_VIEW_SCHEDULE
from base.common_for_bots.static_text import BACK_BUTTON
from base.models import GroupTrainingDay


def day_buttons_coach_info(tr_days: QuerySet[GroupTrainingDay], button_text: str):
    buttons = []
    row = []
    for day in tr_days:
        time_tlg, _, _, _, _, _, _ = get_time_info_from_tr_day(day)
        row.append(
            InlineKeyboardButton(text=day.group.name, callback_data=f"{button_text}{day.id}")
        )
        row.append(
            InlineKeyboardButton(text=time_tlg, callback_data=f"{button_text}{day.id}")
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            BACK_BUTTON,
            callback_data=create_callback_data(
                purpose=CLNDR_ADMIN_VIEW_SCHEDULE,
                action=CLNDR_ACTION_BACK,
                year=tr_days.first().date.year,
                month=tr_days.first().date.month,
                day=0
            )
        ),
    ])

    return InlineKeyboardMarkup(buttons)
