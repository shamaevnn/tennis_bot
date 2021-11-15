import player_bot.take_lesson.group.manage_data
from base.common_for_bots.static_text import DATE_INFO
from base.common_for_bots.tasks import clear_broadcast_messages
from base.common_for_bots.utils import get_time_info_from_tr_day, get_actual_players_without_absent, get_n_free_places, \
    bot_edit_message
from base.models import GroupTrainingDay, TrainingGroup, User
from player_bot.take_lesson import manage_data
from player_bot.take_lesson.group.keyboards import take_lesson_back_keyboard
from player_bot.take_lesson.group.utils import handle_taking_group_lesson, \
    handle_choosing_type_of_payment_for_pay_visiting_when_have_bonus_lessons
from tennis_bot.settings import ADMIN_TELEGRAM_TOKEN


def select_group_time(update, context):
    """
    после того, как выбрал точное время для групповой тренировки,
    показываем инфу об этом дне с кнопкой записаться и назад
    """

    tr_day_id = update.callback_query.data[len(player_bot.take_lesson.group.manage_data.SELECT_PRECISE_GROUP_TIME):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    # сколько сейчас свободных мест
    players = get_actual_players_without_absent(tr_day)
    n_free_places = get_n_free_places(tr_day)
    all_players = players.values('first_name', 'last_name')
    text = ''
    if n_free_places <= 0 and tr_day.group.max_players < 6 and tr_day.group.available_for_additional_lessons:
        text = f'⚠️ATTENTION⚠️\n' \
               f'<b>Это занятие платное!</b>\n\n'

    all_players = '\n'.join((f"{x['first_name']} {x['last_name']}" for x in all_players))
    text += f'{tr_day.group.name} -- {TrainingGroup.GROUP_LEVEL_DICT[tr_day.group.level]}\n' \
            f'{DATE_INFO.format(date_tlg, day_of_week, time_tlg)}' \
            f'👥Присутствующие:\n{all_players}\n\n' \
            f'Свободные места: {n_free_places if n_free_places > 0 else "есть за деньги"}'

    markup = take_lesson_back_keyboard(
        tr_day_id=tr_day_id,
        year=tr_day.date.year,
        month=tr_day.date.month,
        day=tr_day.date.day,
    )

    bot_edit_message(context.bot, text, update, markup)


def confirm_group_lesson(update, context):
    tr_day_id = update.callback_query.data[len(player_bot.take_lesson.group.manage_data.CONFIRM_GROUP_LESSON):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)
    user, _ = User.get_user_and_created(update, context)

    user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(user, tr_day)
    bot_edit_message(context.bot, user_text, update, user_markup)

    if admin_text:
        admins = User.objects.filter(is_staff=True, is_blocked=False)

        clear_broadcast_messages(
            user_ids=list(admins.values_list('id', flat=True)),
            message=admin_text,
            reply_markup=admin_markup,
            tg_token=ADMIN_TELEGRAM_TOKEN
        )


def choose_type_of_payment_for_pay_visiting(update, context):
    payment_choice, tr_day_id = update.callback_query.data[len(
        player_bot.take_lesson.group.manage_data.PAYMENT_VISITING):].split('|')
    tr_day = GroupTrainingDay.objects.get(id=tr_day_id)
    user, _ = User.get_user_and_created(update, context)

    user_text, admin_text = handle_choosing_type_of_payment_for_pay_visiting_when_have_bonus_lessons(
        user, tr_day, payment_choice
    )

    bot_edit_message(context.bot, user_text, update)

    if admin_text:
        admins = User.objects.filter(is_staff=True, is_blocked=False)

        clear_broadcast_messages(
            user_ids=list(admins.values_list('id', flat=True)),
            message=admin_text,
            reply_markup=None,
            tg_token=ADMIN_TELEGRAM_TOKEN
        )