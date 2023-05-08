from django.db.models import F

from base.common_for_bots.utils import (
    get_actual_players_without_absent,
    get_players_for_tr_day, get_dttm_info_for_tr_day,
)
from base.common_for_bots.tasks import broadcast_messages
from base.models import GroupTrainingDay, Player, TrainingGroup
from player_bot.menu_and_commands.keyboards import construct_main_menu
from base.django_admin.static_text import (
    CANCEL_TRAIN_PLUS_BONUS_LESSON_2,
    TRAIN_IS_AVAILABLE_CONGRATS,
)


def send_alert_about_changing_tr_day_status(tr_day: GroupTrainingDay, available_status):
    date_info = get_dttm_info_for_tr_day(tr_day=tr_day)
   
    if available_status == GroupTrainingDay.AVAILABLE:
        text = TRAIN_IS_AVAILABLE_CONGRATS.format(date_info=date_info)
    
    elif available_status == GroupTrainingDay.NOTAVAILABLE:
        text = CANCEL_TRAIN_PLUS_BONUS_LESSON_2.format(date_info=date_info)
        players = get_actual_players_without_absent(tr_day)
        player_ids = players.values("id")
        
        Player.objects.filter(id__in=player_ids).update(
            bonus_lesson=F("bonus_lesson") + 1
        )
         
    elif  available_status == GroupTrainingDay.CANCELLED:
        text = CANCEL_TRAIN_PLUS_BONUS_LESSON_2.format(date_info=date_info)
        players = get_actual_players_without_absent(tr_day)
        
        if tr_day.status == GroupTrainingDay.GROUP_ADULT_TRAIN:
            #Обход всех  игроков
            for player in players:
                # если ученик записался на занятие в счёт отыгрыша, то "отмена" не начисляется, 
                # а возвращается 1 "отыгрыш".
                if player in tr_day.visitors.all():
                    player.bonus_lesson += 1
                #У игрока 0 отыгрышей и он записался на занятие за отыгрыш:
                #в случае "отмены" занятия ни отмена, ни отыгрыш не добавляется. 
                elif player in tr_day.pay_bonus_visitors.all():
                    continue;
                #если у ученика занятие по расписанию группы, то ему начисляется в личный кабинет одна "отмена". 
                else:
                    player.n_cancelled_lessons += 1
            
    else:
        text = TRAIN_IS_AVAILABLE_CONGRATS.format(date_info=date_info)
        
   
    broadcast_messages(
        chat_ids=list(get_players_for_tr_day(tr_day).values_list("tg_id", flat=True)),
        message=text,
        reply_markup=construct_main_menu(),
    )
        

def send_alert_about_changing_tr_day_time(tr_day: GroupTrainingDay, text: str):
    absents = tr_day.absent.all()
    broadcast_messages(
        chat_ids=list(
            get_players_for_tr_day(tr_day).union(absents).values_list("tg_id", flat=True)
        ),
        message=text,
        reply_markup=construct_main_menu(),
    )
