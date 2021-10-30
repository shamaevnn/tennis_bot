from typing import Tuple

from telegram import InlineKeyboardMarkup

from base.common_for_bots.static_text import DATE_INFO
from base.common_for_bots.utils import get_time_info_from_tr_day, get_n_free_places
from base.models import User, GroupTrainingDay
from player_bot.take_lesson.group.keyboards import choose_type_of_payment_for_group_lesson_keyboard, \
    back_to_group_times_when_no_left_keyboard
from player_bot.take_lesson.group.manage_data import PAYMENT_MONEY_AND_BONUS_LESSONS, PAYMENT_MONEY
from player_bot.take_lesson.static_text import CHOOSE_TYPE_OF_PAYMENT, NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER
from tennis_bot.settings import TARIF_ARBITRARY, TARIF_GROUP, TARIF_PAYMENT_ADD_LESSON


def handle_taking_group_lesson(
        user: User,
        tr_day: GroupTrainingDay
) -> Tuple[str, InlineKeyboardMarkup, str, InlineKeyboardMarkup]:
    time_tlg, _, _, date_tlg, day_of_week, _, end_time = get_time_info_from_tr_day(tr_day)
    date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    n_free_places = get_n_free_places(tr_day)

    admin_text = ''
    admin_markup = None
    if n_free_places > 0:
        tr_day.visitors.add(user)
        user_text = f'Записал тебя на тренировку.\n{date_info}'
        user_markup = None

        if user.bonus_lesson > 0 and user.status == User.STATUS_TRAINING:
            admin_text = f'{user.first_name} {user.last_name} придёт на гр. тренировку за отыгрыш.\n{date_info}'
            user.bonus_lesson -= 1
            user.save()
        else:
            admin_text = f'⚠️ATTENTION⚠️\n' \
                         f'{user.first_name} {user.last_name} придёт на гр. тренировку ' \
                         f'<b>не за счет отыгрышей, не забудь взять {TARIF_ARBITRARY}₽.</b>\n' \
                         f'{date_info}'
    else:
        if tr_day.group.max_players - n_free_places < 6 and tr_day.group.available_for_additional_lessons:
            tarif = TARIF_ARBITRARY if user.status == User.STATUS_ARBITRARY else TARIF_GROUP
            if user.bonus_lesson == 0:
                tr_day.pay_visitors.add(user)
                user_text = f'Записал тебя на тренировку' \
                            f'⚠️ATTENTION⚠️\n' \
                            f'Не забудь заплатить <b>{tarif}₽</b>\n' \
                            f'{date_info}'
                admin_text = f'⚠️ATTENTION⚠️\n' \
                             f'{user.first_name} {user.last_name} придёт на гр. тренировку ' \
                             f'<b>не за счет отыгрышей, не забудь взять {tarif}₽.</b>\n' \
                             f'{date_info}'
                user_markup = None
            else:
                user_text = CHOOSE_TYPE_OF_PAYMENT
                user_markup = choose_type_of_payment_for_group_lesson_keyboard(
                    payment_add_lesson=TARIF_PAYMENT_ADD_LESSON,
                    tr_day_id=tr_day.id,
                    tarif=tarif,
                )
        else:
            user_text = NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER
            user_markup = back_to_group_times_when_no_left_keyboard(
                year=tr_day.date.year,
                month=tr_day.date.month,
                day=tr_day.date.day
            )

    return user_text, user_markup, admin_text, admin_markup


def handle_choosing_type_of_payment_for_pay_visiting_when_have_bonus_lessons(
        user: User, tr_day: GroupTrainingDay, payment_choice: str
):
    # todo: tests on this function
    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    user_text, admin_text = '', ''
    if payment_choice == PAYMENT_MONEY_AND_BONUS_LESSONS:
        user.bonus_lesson -= 1
        user.save()

        tr_day.pay_bonus_visitors.add(user)
        user_text = f'Записал тебя на тренировку\n' \
                    f'⚠️ATTENTION⚠️\n' \
                    f'Не забудь заплатить <b>{TARIF_PAYMENT_ADD_LESSON}₽</b>\n{date_info}'

        admin_text = f'⚠️ATTENTION⚠️\n' \
                     f'{user.first_name} {user.last_name} придёт ' \
                     f'<b>за счёт платных отыгрышей, не забудь взять {TARIF_PAYMENT_ADD_LESSON}₽.</b>\n{date_info}'

    elif payment_choice == PAYMENT_MONEY:
        tr_day.pay_visitors.add(user)
        tarif = TARIF_ARBITRARY if user.status == User.STATUS_ARBITRARY else TARIF_GROUP

        user_text = f'Записал тебя на тренировку\n' \
                    f'⚠️ATTENTION⚠️\n' \
                    f'Не забудь заплатить <b>{tarif}₽</b>\n{date_info}'

        admin_text = f'⚠️ATTENTION⚠️\n' \
                     f'{user.first_name} {user.last_name} придёт ' \
                     f'<b>в дополнительное время, не забудь взять {tarif}₽.</b>\n{date_info}'

    return user_text, admin_text