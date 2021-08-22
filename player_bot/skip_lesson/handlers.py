from base.common_for_bots.static_text import DATE_INFO
from base.models import User, GroupTrainingDay
from player_bot.menu_and_commands.keyboard_utils import construct_main_menu
from base.common_for_bots.utils import clear_broadcast_messages, bot_edit_message, get_time_info_from_tr_day,\
    create_calendar
from player_bot.skip_lesson.keyboard_utils import construct_detail_menu_for_skipping
from player_bot.skip_lesson.manage_data import SELECT_SKIP_TIME_BUTTON, SHOW_INFO_ABOUT_SKIPPING_DAY
from player_bot.calendar.manage_data import CLNDR_ACTION_SKIP
from player_bot.registration.utils import check_status_decor
from player_bot.skip_lesson.utils import select_tr_days_for_skipping, \
    make_group_name_group_players_info_for_skipping, handle_skipping_train
from tennis_bot.settings import ADMIN_TELEGRAM_TOKEN


@check_status_decor
def skip_lesson_main_menu_button(update, context):
    user, _ = User.get_user_and_created(update, context)
    available_grouptraining_dates = select_tr_days_for_skipping(user)
    if available_grouptraining_dates.exists():
        context.bot.send_message(
            user.id,
            'Выбери дату тренировки для отмены.\n'
            '✅ -- дни, доступные для отмены.',
            reply_markup=create_calendar(CLNDR_ACTION_SKIP,
                                         dates_to_highlight=list(
                                             available_grouptraining_dates.values_list('date', flat=True))
                                         )
        )
    else:
        context.bot.send_message(
            user.id,
            'Пока что нечего пропускать.',
            reply_markup=construct_main_menu(user)
        )


@check_status_decor
def skip_lesson_when_geq_2(update, context):
    tr_day_id = update.callback_query.data[len(SELECT_SKIP_TIME_BUTTON):]
    training_day = GroupTrainingDay.objects.get(id=tr_day_id)

    group_name, group_players = make_group_name_group_players_info_for_skipping(training_day)
    markup, text = construct_detail_menu_for_skipping(training_day, CLNDR_ACTION_SKIP, group_name, group_players)
    bot_edit_message(context.bot, text, update, markup)


@check_status_decor
def skip_lesson(update, context):
    user, _ = User.get_user_and_created(update, context)

    tr_day_id = update.callback_query.data[len(SHOW_INFO_ABOUT_SKIPPING_DAY):]
    training_day = GroupTrainingDay.objects.get(id=tr_day_id)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(training_day)
    date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    admins = User.objects.filter(is_superuser=True, is_blocked=False)
    if not training_day.is_available:
        text = "{} в {} ❌нет тренировки❌, т.к. она отменена тренером, поэтому ее нельзя пропустить.".format(date_tlg, time_tlg)
        bot_edit_message(context.bot, text, update)

        skip_lesson_main_menu_button(context.bot, update)
    else:
        text, admin_text = handle_skipping_train(training_day, user, date_info)

        clear_broadcast_messages(
            user_ids=list(admins.values_list('id', flat=True)),
            message=admin_text,
            tg_token=ADMIN_TELEGRAM_TOKEN,
        )

        bot_edit_message(context.bot, text, update)