from telegram import Update
from telegram.ext import CallbackContext

from base.common_for_bots.static_text import DATE_INFO
from base.models import Player, GroupTrainingDay
from player_bot.menu_and_commands.keyboards import construct_main_menu
from base.common_for_bots.utils import (
    bot_edit_message,
    get_time_info_from_tr_day,
    create_calendar,
    get_actual_players_without_absent,
)
from base.common_for_bots.tasks import send_message_to_coaches
from player_bot.skip_lesson.keyboards import construct_detail_menu_for_skipping
from player_bot.skip_lesson.manage_data import (
    SELECT_SKIP_TIME_BUTTON,
    SHOW_INFO_ABOUT_SKIPPING_DAY,
)
from player_bot.calendar.manage_data import CLNDR_ACTION_SKIP
from player_bot.registration.utils import check_status_decor
from player_bot.skip_lesson.static_text import (
    ONLY_ONE_LEFT,
    CHOOSE_DATE_TO_CANCEL,
    TRAIN_CANCELLED_BY_COACH_TEMPLATE,
    NO_LESSONS_TO_SKIP,
)
from player_bot.skip_lesson.utils import (
    select_tr_days_for_skipping,
    make_group_name_group_players_info_for_skipping,
    handle_skipping_train,
)


@check_status_decor
def skip_lesson_main_menu_button(update: Update, context: CallbackContext):
    player, _ = Player.get_player_and_created(update, context)
    available_grouptraining_dates = list(select_tr_days_for_skipping(player))
    if len(available_grouptraining_dates):
        context.bot.send_message(
            player.tg_id,
            CHOOSE_DATE_TO_CANCEL,
            reply_markup=create_calendar(
                CLNDR_ACTION_SKIP,
                dates_to_highlight=[
                    tr_day.date for tr_day in select_tr_days_for_skipping(player)
                ],
            ),
        )
    else:
        context.bot.send_message(
            chat_id=player.tg_id,
            text=NO_LESSONS_TO_SKIP,
            reply_markup=construct_main_menu(player),
        )


def skip_lesson_when_geq_2(update: Update, context):
    tr_day_id = update.callback_query.data[len(SELECT_SKIP_TIME_BUTTON) :]
    training_day = GroupTrainingDay.objects.get(id=tr_day_id)

    group_name, group_players = make_group_name_group_players_info_for_skipping(
        training_day
    )
    markup, text = construct_detail_menu_for_skipping(
        training_day, CLNDR_ACTION_SKIP, group_name, group_players
    )
    bot_edit_message(context.bot, text, update, markup)


def skip_lesson(update: Update, context: CallbackContext):
    player = Player.from_update(update)

    tr_day_id = update.callback_query.data[len(SHOW_INFO_ABOUT_SKIPPING_DAY) :]
    tr_day: GroupTrainingDay = GroupTrainingDay.objects.select_related("group").get(
        id=tr_day_id
    )

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    if not tr_day.is_available:
        text = TRAIN_CANCELLED_BY_COACH_TEMPLATE.format(date_tlg, time_tlg)
        bot_edit_message(context.bot, text, update)

        skip_lesson_main_menu_button(update, context)
        return

    if tr_day.status == GroupTrainingDay.GROUP_ADULT_TRAIN:
        # отправляем тренеру сообщение, что в группе остался 1 игрок
        n_players_left_for_this_lesson = get_actual_players_without_absent(
            tr_day
        ).count()
        if n_players_left_for_this_lesson == 2:
            send_message_to_coaches(
                text=ONLY_ONE_LEFT.format(tr_day.group.name, date_info),
            )

    text, admin_text = handle_skipping_train(tr_day, player, date_info)
    if admin_text:
        send_message_to_coaches(
            text=admin_text,
        )

    bot_edit_message(context.bot, text, update)
