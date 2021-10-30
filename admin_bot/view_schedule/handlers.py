import base.common_for_bots.static_text
from admin_bot.view_schedule.keyboards import back_from_show_grouptrainingday_info_keyboard
from admin_bot.view_schedule import static_text
from admin_bot.view_schedule.manage_data import SHOW_GROUPDAY_INFO
from admin_bot.view_schedule.utils import schedule_users_info
from base.models import GroupTrainingDay, TrainingGroup
from base.common_for_bots.utils import bot_edit_message, get_time_info_from_tr_day


def show_trainingroupday_info(update, context):
    tr_day_id = update.callback_query.data[len(SHOW_GROUPDAY_INFO):]
    tr_day = GroupTrainingDay.objects.select_related('group').prefetch_related('visitors', 'pay_visitors', 'pay_bonus_visitors').get(id=tr_day_id)

    availability = f'{static_text.NO_TRAIN}\n' if not tr_day.is_available else ''
    is_individual = f'{static_text.INDIVIDUAL_TRAIN}\n' if tr_day.is_individual else f'{static_text.GROUP_TRAIN}️\n'
    affiliation = f'{static_text.MY_TRAIN}\n\n' if tr_day.tr_day_status == GroupTrainingDay.MY_TRAIN_STATUS else f'{static_text.RENT}\n\n'

    group_name = f"{tr_day.group.name}\n"

    if not tr_day.is_individual:
        group_players = f'{static_text.PLAYERS_FROM_GROUP}:\n{schedule_users_info(tr_day.group.users.all().difference(tr_day.absent.all()))}\n'
        visitors = f'\n{static_text.HAVE_COME_FROM_OTHERS}:\n{schedule_users_info(tr_day.visitors)}\n' if tr_day.visitors.exists() else ''
        pay_visitors = f'\n{static_text.HAVE_COME_FOR_MONEY}:\n{schedule_users_info(tr_day.pay_visitors)}\n' if tr_day.pay_visitors.exists() else ''
        pay_bonus_visitors = f'\n{static_text.HAVE_COME_FOR_PAY_BONUS_LESSON}:\n{schedule_users_info(tr_day.pay_bonus_visitors)}\n' if tr_day.pay_bonus_visitors.exists() else ''
        absents = f'\n{static_text.ARE_ABSENT}:\n{schedule_users_info(tr_day.absent)}\n' if tr_day.absent.exists() else ''
        group_level = f"{TrainingGroup.GROUP_LEVEL_DICT[tr_day.group.level]}\n"
    else:
        group_players, visitors, pay_visitors, pay_bonus_visitors, absents, group_level = '', '', '', '', '', ''

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)

    general_info = f'<b>{date_tlg} ({day_of_week})\n{time_tlg}</b>\n{availability}{is_individual}{affiliation}'
    users_info = f'{group_name}{group_level}{group_players}{visitors}{pay_visitors}{pay_bonus_visitors}{absents}'
    text = f'{general_info}{users_info}'

    markup = back_from_show_grouptrainingday_info_keyboard(
        year=tr_day.date.year,
        month=tr_day.date.month,
        day=tr_day.date.day
    )

    bot_edit_message(context.bot, text, update, markup)


