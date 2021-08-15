import telegram

from .static_text import *
from base.models import User, GroupTrainingDay
from base.utils import bot_edit_message, get_time_info_from_tr_day, info_about_users
from tele_interface.manage_data import PERMISSION_FOR_IND_TRAIN, SHOW_GROUPDAY_INFO, \
    CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_ACTION_BACK, CLNDR_NEXT_MONTH, CLNDR_DAY, CLNDR_IGNORE, \
    CLNDR_PREV_MONTH, AMOUNT_OF_IND_TRAIN
from tele_interface.utils import separate_callback_data, create_tr_days_for_future
from tele_interface.keyboard_utils import create_calendar
from .keyboard_utils import day_buttons_coach_info, \
    back_from_show_grouptrainingday_info_keyboard, how_many_trains_to_save_keyboard, go_to_site_keyboard
from tennis_bot.settings import TELEGRAM_TOKEN
from datetime import date, timedelta


def permission_for_ind_train(update, context):
    permission, user_id, tr_day_id = update.callback_query.data[len(PERMISSION_FOR_IND_TRAIN):].split('|')

    player = User.objects.get(id=user_id)
    tr_day = GroupTrainingDay.objects.filter(id=tr_day_id)

    if tr_day.exists():
        tr_day = tr_day.first()
        time_tlg, _, _, date_tlg, _, _, _ = get_time_info_from_tr_day(tr_day)
        markup = None

        if permission == 'yes':
            markup = how_many_trains_to_save_keyboard(tr_day_id=tr_day_id)
            admin_text = HOW_MANY_TRAINS_TO_SAVE

            user_text = f'Отлично, тренер подтвердил тренировку <b>{date_tlg}</b>\n' \
                        f'Время: <b>{time_tlg}</b>\n' \
                        f'Не забудь!'

        else:
            admin_text = WILL_SAY_THAT_TRAIN_IS_CANCELLED.format(
                player.last_name,
                player.first_name,
                date_tlg,
                time_tlg
            )

            user_text = f'Внимание!!!\nИндивидуальная тренировка <b> {date_tlg}</b>\n' \
                        f'в <b>{time_tlg}</b>\n' \
                        f'<b>ОТМЕНЕНА</b>'

            tr_day.delete()

        tennis_bot = telegram.Bot(TELEGRAM_TOKEN)
        tennis_bot.send_message(
            player.id,
            user_text,
            parse_mode='HTML'
        )

    else:
        admin_text = TRAIN_IS_ALREADY_CANCELLED
        markup = None

    bot_edit_message(context.bot, admin_text, update, markup=markup)


def save_many_ind_trains(update, context):
    tr_day_id, num_lessons = update.callback_query.data[len(AMOUNT_OF_IND_TRAIN):].split("|")
    tr_day = GroupTrainingDay.objects.get(id=tr_day_id)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    text = WISH_GOOD_TRAIN.format(
        date_tlg,
        day_of_week,
        time_tlg
    )
    if num_lessons == 'one':
        text += SAVED_ONCE
    else:
        create_tr_days_for_future(tr_day)
        text += SAVED_2_MONTHS_AHEAD

    bot_edit_message(context.bot, text, update)


def admin_calendar_selection(bot, update):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    """
    query = update.callback_query
    (purpose, action, year, month, day) = separate_callback_data(query.data)
    curr = date(int(year), int(month), 1)

    if action == CLNDR_IGNORE:
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == CLNDR_DAY:
        bot_edit_message(bot, query.message.text, update)
        return True, purpose, date(int(year), int(month), int(day))
    elif action == CLNDR_PREV_MONTH:
        pre = curr - timedelta(days=1)
        bot_edit_message(bot, query.message.text, update, create_calendar(purpose, int(pre.year), int(pre.month)))
    elif action == CLNDR_NEXT_MONTH:
        ne = curr + timedelta(days=31)
        bot_edit_message(bot, query.message.text, update, create_calendar(purpose, int(ne.year), int(ne.month)))
    elif action == CLNDR_ACTION_BACK:
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
            if tr_days.count():
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


def redirect_to_site(update, context):
    markup = go_to_site_keyboard()
    update.message.reply_text(
        text=ADMIN_SITE,
        reply_markup=markup
    )


GROUP_IDS, TEXT_TO_SEND = 2, 3


def show_traingroupday_info(update, context):
    tr_day_id = update.callback_query.data[len(SHOW_GROUPDAY_INFO):]
    tr_day = GroupTrainingDay.objects.select_related('group').prefetch_related('visitors', 'pay_visitors', 'pay_bonus_visitors').get(id=tr_day_id)

    availability = f'{NO_TRAIN}\n' if not tr_day.is_available else ''
    is_individual = f'{INDIVIDUAL_TRAIN}\n' if tr_day.is_individual else f'{GROUP_TRAIN}️\n'
    affiliation = f'{MY_TRAIN}\n\n' if tr_day.tr_day_status == GroupTrainingDay.MY_TRAIN_STATUS else f'{RENT}\n\n'

    group_name = f"{tr_day.group.name}\n"

    if not tr_day.is_individual:
        group_players = f'{PLAYERS_FROM_GROUP}:\n{info_about_users(tr_day.group.users.all().difference(tr_day.absent.all()), for_admin=True)}\n'
        visitors = f'\n{HAVE_COME_FROM_OTHERS}:\n{info_about_users(tr_day.visitors, for_admin=True)}\n' if tr_day.visitors.exists() else ''
        pay_visitors = f'\n{HAVE_COME_FOR_MONEY}:\n{info_about_users(tr_day.pay_visitors, for_admin=True)}\n' if tr_day.pay_visitors.exists() else ''
        pay_bonus_visitors = f'\n{HAVE_COME_FOR_PAY_BONUS_LESSON}:\n{info_about_users(tr_day.pay_bonus_visitors, for_admin=True)}\n' if tr_day.pay_bonus_visitors.exists() else ''
        absents = f'\n{ARE_ABSENT}:\n{info_about_users(tr_day.absent, for_admin=True)}\n' if tr_day.absent.exists() else ''
        group_level = f"{GROUP_LEVEL_DICT[tr_day.group.level]}\n"
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
