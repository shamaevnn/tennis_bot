from django.db.models import F

from base.common_for_bots.static_text import ERROR_UNKNOWN_AVAILABLE_STATUS
from base.common_for_bots.utils import (
    get_actual_players_without_absent,
    get_dttm_info_for_tr_day,
)
from base.django_admin.static_text import (
    CANCEL_TRAIN_PLUS_BONUS_LESSON_2,
    TRAIN_IS_AVAILABLE_CONGRATS,
)

from base.models import GroupTrainingDay, Player
from base.common_for_bots.tasks import broadcast_messages
from base.common_for_bots.utils import get_players_for_tr_day
from player_bot.menu_and_commands.keyboards import construct_main_menu


def change_tr_day_available_status(tr_day: GroupTrainingDay, available_status):
    if tr_day.available_status != available_status:
        # обновляем статус, если он не был изменён ранее, другой функцией
        tr_day.available_status = available_status
        tr_day.save()

    if available_status == GroupTrainingDay.AVAILABLE:
        return

    if available_status == GroupTrainingDay.NOT_AVAILABLE:

        players = get_actual_players_without_absent(tr_day)
        player_ids = players.values("id")

        Player.objects.filter(id__in=player_ids).update(
            bonus_lesson=F("bonus_lesson") + 1
        )

    elif available_status == GroupTrainingDay.CANCELLED:

        players = get_actual_players_without_absent(tr_day)
        visitors = tr_day.visitors.all()
        pay_bonus_visitors = tr_day.pay_bonus_visitors.all()

        if tr_day.status == GroupTrainingDay.GROUP_ADULT_TRAIN:
            # обход всех  игроков
            for player in players:
                # если ученик записался на занятие в счёт отыгрыша, то "отмена" не начисляется,
                # а возвращается 1 "отыгрыш".
                if player in visitors:
                    player.bonus_lesson += 1
                # у игрока 0 отыгрышей и он записался на занятие за отыгрыш:
                # в случае "отмены" занятия ни отмена, ни отыгрыш не добавляется.
                elif player in pay_bonus_visitors:
                    continue
                # если у ученика занятие по расписанию группы, то ему начисляется в личный кабинет одна "отмена".
                else:
                    player.n_cancelled_lessons += 1

                player.save()
    else:
        raise ValueError(ERROR_UNKNOWN_AVAILABLE_STATUS.format(available_status))


def get_text_about_the_available_status_change(
    tr_day: GroupTrainingDay, available_status
):
    text = ""
    date_info = get_dttm_info_for_tr_day(tr_day=tr_day)

    if available_status == GroupTrainingDay.AVAILABLE:
        text = TRAIN_IS_AVAILABLE_CONGRATS.format(date_info=date_info)

    elif available_status in (
        GroupTrainingDay.CANCELLED,
        GroupTrainingDay.NOT_AVAILABLE,
    ):
        text = CANCEL_TRAIN_PLUS_BONUS_LESSON_2.format(date_info=date_info)

    else:
        raise ValueError(ERROR_UNKNOWN_AVAILABLE_STATUS.format(available_status))

    return text


# Отправка уведомлений об изменении статуса
def send_alert_changing_tr_day_status(tr_day: GroupTrainingDay, available_status):
    text = get_text_about_the_available_status_change(tr_day, available_status)

    players = get_actual_players_without_absent(tr_day)
    if players.count() > 0:
        broadcast_messages(
            chat_ids=list(players.values_list("tg_id", flat=True)),
            message=text,
            reply_markup=construct_main_menu(),
        )


def change_tr_day_available_status_and_send_alert(
    tr_day: GroupTrainingDay, available_status
):
    change_tr_day_available_status(tr_day, available_status)
    send_alert_changing_tr_day_status(tr_day, available_status)
