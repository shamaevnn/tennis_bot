from telegram import Update
from telegram.ext import CallbackContext

from admin_bot.view_schedule.keyboards import (
    show_grouptrainingday_available_change_keyboard,
    show_grouptrainingday_available_change_confirm_keyboard,
)
from admin_bot.view_schedule import static_text
from admin_bot.view_schedule.manage_data import SHOW_GROUPDAY_INFO
from admin_bot.view_schedule.static_text import (
    CONFIRM_CANCEL_TRAIN,
    CONFIRM_AVAILABLE_TRAIN,
    DAY_FIND_ERROR,
)
from admin_bot.view_schedule.utils import schedule_players_info
from base.common_for_bots.static_text import ERROR_UNKNOWN_AVAILABLE_STATUS
from base.models import GroupTrainingDay, TrainingGroup

from base.common_for_bots.utils import (
    bot_edit_message,
    get_time_info_from_tr_day,
    get_actual_players_without_absent,
    separate_callback_data,
)

from base.utils.change_available_status import (
    change_tr_day_available_status_and_send_alert,
    get_text_about_the_available_status_change,
)


def show_trainingroupday_info(update, context: CallbackContext):
    tr_day_id = update.callback_query.data[len(SHOW_GROUPDAY_INFO) :]
    tr_day: GroupTrainingDay = (
        GroupTrainingDay.objects.select_related("group")
        .prefetch_related("visitors", "pay_visitors", "pay_bonus_visitors")
        .get(id=tr_day_id)
    )
    tr_day_status = tr_day.status

    availability = (
        f"{static_text.NO_TRAIN}\n"
        if tr_day.available_status != GroupTrainingDay.AVAILABLE
        else ""
    )

    if tr_day_status == GroupTrainingDay.INDIVIDUAL_TRAIN:
        status = static_text.INDIVIDUAL_TRAIN
    elif tr_day_status == GroupTrainingDay.RENT_COURT_STATUS:
        status = static_text.RENT
    else:
        status = static_text.GROUP_TRAIN

    group_name = f"{tr_day.group.name}\n"

    if tr_day_status == GroupTrainingDay.GROUP_ADULT_TRAIN:
        players = get_actual_players_without_absent(tr_day)
        group_players = (
            f"{static_text.PLAYERS_FROM_GROUP}:\n{schedule_players_info(players)}\n"
        )
        visitors = (
            f"\n{static_text.HAVE_COME_FROM_OTHERS}:\n{schedule_players_info(tr_day.visitors)}\n"
            if tr_day.visitors.exists()
            else ""
        )
        pay_visitors = (
            f"\n{static_text.HAVE_COME_FOR_MONEY}:\n{schedule_players_info(tr_day.pay_visitors)}\n"
            if tr_day.pay_visitors.exists()
            else ""
        )
        pay_bonus_visitors = (
            f"\n{static_text.HAVE_COME_FOR_PAY_BONUS_LESSON}:\n{schedule_players_info(tr_day.pay_bonus_visitors)}\n"
            if tr_day.pay_bonus_visitors.exists()
            else ""
        )
        absents = (
            f"\n{static_text.ARE_ABSENT}:\n{schedule_players_info(tr_day.absent)}\n"
            if tr_day.absent.exists()
            else ""
        )
        group_level = f"{TrainingGroup.GROUP_LEVEL_DICT[tr_day.group.level]}\n"
    else:
        (
            group_players,
            visitors,
            pay_visitors,
            pay_bonus_visitors,
            absents,
            group_level,
        ) = ("", "", "", "", "", "")

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)

    general_info = (
        f"<b>{date_tlg} ({day_of_week})\n{time_tlg}</b>\n{availability}{status}\n\n"
    )
    players_info = f"{group_name}{group_level}{group_players}{visitors}{pay_visitors}{pay_bonus_visitors}{absents}"
    text = f"{general_info}{players_info}"

    markup = show_grouptrainingday_available_change_keyboard(tr_day)

    bot_edit_message(context.bot, text, update, markup)


def confirm_change_available_status_handler(update: Update, context: CallbackContext):
    """
    Обработчик для создания подтверждения перед изменением: available_status у дня по его id
    """
    query = update.callback_query
    (_, action, tr_day_id) = separate_callback_data(query.data)
    markup = show_grouptrainingday_available_change_confirm_keyboard(action, tr_day_id)

    if action == GroupTrainingDay.AVAILABLE:
        text = CONFIRM_AVAILABLE_TRAIN

    elif action in (GroupTrainingDay.NOT_AVAILABLE, GroupTrainingDay.CANCELLED):
        text = CONFIRM_CANCEL_TRAIN

    else:
        raise ValueError(ERROR_UNKNOWN_AVAILABLE_STATUS.format(action))

    bot_edit_message(context.bot, text, update, markup)


def change_available_status_handler(update: Update, context: CallbackContext):
    """
    Обработчик для изменения: available_status у дня по его id
    """
    query = update.callback_query
    (_, action, tr_day_id) = separate_callback_data(query.data)

    tr_day = GroupTrainingDay.objects.filter(id=tr_day_id).first()

    if tr_day is not None:
        change_tr_day_available_status_and_send_alert(
            tr_day=tr_day, available_status=action
        )

        text = get_text_about_the_available_status_change(tr_day, action)

        bot_edit_message(context.bot, text, update)
    else:
        bot_edit_message(context.bot, DAY_FIND_ERROR, update)
