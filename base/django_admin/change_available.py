
from django.db.models import F
from base.common_for_bots.utils import get_actual_players_without_absent, get_dttm_info_for_tr_day
from base.django_admin.static_text import (
    CANCEL_TRAIN_PLUS_BONUS_LESSON_2, 
    ERROR_UNKNOWN_AVAILABLE_STATUS, TRAIN_IS_AVAILABLE_CONGRATS)

from base.models import GroupTrainingDay, Player


def change_players_on_available_status(tr_day: GroupTrainingDay, available_status):
    if available_status == GroupTrainingDay.NOTAVAILABLE:
       
        players = get_actual_players_without_absent(tr_day)
        player_ids = players.values("id")
        
        Player.objects.filter(id__in=player_ids).update(
            bonus_lesson = F("bonus_lesson") + 1
        )
         
    elif available_status == GroupTrainingDay.CANCELLED:
       
        players = get_actual_players_without_absent(tr_day)
        visitors = tr_day.visitors.all();
        pay_bonus_visitors = tr_day.pay_bonus_visitors.all();
        
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
    
def get_text_about_the_available_status_change(tr_day: GroupTrainingDay, available_status):
    text =  ""
    date_info = get_dttm_info_for_tr_day(tr_day=tr_day)
    
    if available_status == GroupTrainingDay.AVAILABLE:
        text = TRAIN_IS_AVAILABLE_CONGRATS.format(date_info=date_info)
    
    elif available_status == GroupTrainingDay.NOTAVAILABLE:
        text = CANCEL_TRAIN_PLUS_BONUS_LESSON_2.format(date_info=date_info)
        

    elif available_status == GroupTrainingDay.CANCELLED:
        text = CANCEL_TRAIN_PLUS_BONUS_LESSON_2.format(date_info=date_info)
    
    else :
        raise ValueError(ERROR_UNKNOWN_AVAILABLE_STATUS.format(available_status))
    
    return text
        
    