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
from player_bot.skip_lesson.static_text import ONLY_ONE_LEFT
from player_bot.skip_lesson.utils import (
    select_tr_days_for_skipping,
    make_group_name_group_players_info_for_skipping,
    handle_skipping_train,
)


@check_status_decor
def skip_lesson_main_menu_button(update: Update, context: CallbackContext):
    player, _ = Player.get_player_and_created(update, context)
    available_grouptraining_dates = select_tr_days_for_skipping(player)
    if available_grouptraining_dates.exists():
        context.bot.send_message(
            player.tg_id,
            "Выбери дату тренировки для отмены.\n" "✅ -- дни, доступные для отмены.",
            reply_markup=create_calendar(
                CLNDR_ACTION_SKIP,
                dates_to_highlight=list(
                    available_grouptraining_dates.values_list("date", flat=True)
                ),
            ),
        )
    else:
        context.bot.send_message(
            chat_id=player.tg_id,
            text="Пока что нечего пропускать.",
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
    training_day = GroupTrainingDay.objects.get(id=tr_day_id)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(
        training_day
    )
    date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    if not training_day.is_available:
        text = "{} в {} ❌нет тренировки❌, т.к. она отменена тренером, поэтому ее нельзя пропустить.".format(
            date_tlg, time_tlg
        )
        bot_edit_message(context.bot, text, update)

        skip_lesson_main_menu_button(context.bot, update)
    else:
        text, admin_text = handle_skipping_train(training_day, player, date_info)

        send_message_to_coaches(
            text=admin_text,
        )

        n_players_left_for_this_lesson = get_actual_players_without_absent(
            training_day
        ).count()
        if n_players_left_for_this_lesson == 1:
            send_message_to_coaches(
                text=ONLY_ONE_LEFT.format(training_day.group.name, date_info),
            )

        bot_edit_message(context.bot, text, update)
