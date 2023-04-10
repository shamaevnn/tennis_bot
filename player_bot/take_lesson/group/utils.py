from typing import Tuple, Optional

from telegram import InlineKeyboardMarkup

from base.common_for_bots.static_text import DATE_INFO
from base.common_for_bots.utils import get_time_info_from_tr_day, get_n_free_places
from base.models import GroupTrainingDay, Player
from player_bot.take_lesson.group.keyboards import (
    choose_type_of_payment_for_group_lesson_keyboard,
    back_to_group_times_when_no_left_keyboard,
)
from player_bot.take_lesson.group.manage_data import (
    PAYMENT_MONEY_AND_BONUS_LESSONS,
    PAYMENT_MONEY,
)
from player_bot.take_lesson.group.static_text import ADMIN_TEXT_GROUP_TRAIN, ADMIN_TEXT_SINGLE_TRAIN_DOP_TIME, ADMIN_TEXT_SINGLE_TRAIN_PAY_BONUSS, CANT_TAKE_LESSON_MAX_IN_FUTURE, PLAYER_VISIT_GROUP_TRAIN_BONUSS, PLAYER_WRITTEN_TO_TRAIN, PLAYER_WRITTEN_TO_TRAIN_SHORT
from player_bot.take_lesson.static_text import (
    CHOOSE_TYPE_OF_PAYMENT,
    NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER,
)
from tennis_bot.settings import TARIF_ARBITRARY, TARIF_GROUP, TARIF_PAYMENT_ADD_LESSON


def handle_taking_group_lesson(
    player: Player, tr_day: GroupTrainingDay
) -> Tuple[
    str, Optional[InlineKeyboardMarkup], Optional[str], Optional[InlineKeyboardMarkup]
]:
    admin_text = ""
    admin_markup = None

    max_lessons_in_future = player.max_lessons_for_bonus_in_future
    now_count_lessons_in_future = player.count_not_self_group_trainings_in_future()
    if now_count_lessons_in_future >= max_lessons_in_future:
        player_text = CANT_TAKE_LESSON_MAX_IN_FUTURE.format(
            max_lessons=max_lessons_in_future,
            now_count_lessons=now_count_lessons_in_future,
        )
        player_markup = back_to_group_times_when_no_left_keyboard(
            year=tr_day.date.year, month=tr_day.date.month, day=tr_day.date.day
        )
        return player_text, player_markup, admin_text, admin_markup

    time_tlg, _, _, date_tlg, day_of_week, _, end_time = get_time_info_from_tr_day(
        tr_day
    )
    date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    n_free_places = get_n_free_places(tr_day)
    if n_free_places > 0:
        tr_day.visitors.add(player)
        player_text = PLAYER_WRITTEN_TO_TRAIN_SHORT.format(date_info)
        player_markup = None

        if player.bonus_lesson > 0 and player.status == Player.STATUS_TRAINING:
            admin_text = PLAYER_VISIT_GROUP_TRAIN_BONUSS.format(player.first_name, player.last_name, 
                                                                date_info)
            player.bonus_lesson -= 1
            player.save()
        else:
            admin_text = ADMIN_TEXT_GROUP_TRAIN.format(player.first_name, player.last_name, TARIF_ARBITRARY, date_info)

    else:
        if (
            tr_day.group.max_players - n_free_places < 6
            and tr_day.group.available_for_additional_lessons
        ):
            tarif = (
                TARIF_ARBITRARY
                if player.status == Player.STATUS_ARBITRARY
                else TARIF_GROUP
            )
            if player.bonus_lesson == 0:
                tr_day.pay_visitors.add(player)
                player_text = PLAYER_WRITTEN_TO_TRAIN.format(tarif,date_info);
                  
                admin_text = ADMIN_TEXT_GROUP_TRAIN.format(player.first_name,player.last_name,tarif,date_info)  
                   
                player_markup = None
            else:
                player_text = CHOOSE_TYPE_OF_PAYMENT
                player_markup = choose_type_of_payment_for_group_lesson_keyboard(
                    payment_add_lesson=TARIF_PAYMENT_ADD_LESSON,
                    tr_day_id=tr_day.id,
                    tarif=tarif,
                )
        else:
            player_text = NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER
            player_markup = back_to_group_times_when_no_left_keyboard(
                year=tr_day.date.year, month=tr_day.date.month, day=tr_day.date.day
            )

    return player_text, player_markup, admin_text, admin_markup


def handle_choosing_type_of_payment_for_pay_visiting_when_have_bonus_lessons(
    player: Player, tr_day: GroupTrainingDay, payment_choice: str
):
    # todo: tests on this function
    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    player_text, admin_text = "", ""
    if payment_choice == PAYMENT_MONEY_AND_BONUS_LESSONS:
        player.bonus_lesson -= 1
        player.save()

        tr_day.pay_bonus_visitors.add(player)
        player_text = PLAYER_WRITTEN_TO_TRAIN.format(TARIF_PAYMENT_ADD_LESSON,date_info)
          

        admin_text = ADMIN_TEXT_SINGLE_TRAIN_PAY_BONUSS.format(player.first_name,player.last_name,
                                                               TARIF_PAYMENT_ADD_LESSON,date_info)
         

    elif payment_choice == PAYMENT_MONEY:
        tr_day.pay_visitors.add(player)
        tarif = (
            TARIF_ARBITRARY if player.status == Player.STATUS_ARBITRARY else TARIF_GROUP
        )

        player_text =PLAYER_WRITTEN_TO_TRAIN.format(tarif,date_info) 
         

        admin_text = ADMIN_TEXT_SINGLE_TRAIN_DOP_TIME.format(player.first_name,player.last_name,tarif,date_info) 


    return player_text, admin_text
