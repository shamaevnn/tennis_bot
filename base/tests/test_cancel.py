
from django.test import TestCase
from base.models import GroupTrainingDay
from base.utils.for_tests import CreateData
from  base.django_admin import utils

class CancelLessonCase(TestCase):
   
    # если ученик записался на занятие в счёт отыгрыша, то "отмена" не начисляется, а возвращается 1 "отыгрыш".
    def test_cancel_lesson_for_visitor(self)-> None:
        
        player = CreateData.group_player(tg_id=350490234, first_name="Nikita")
      
        group = CreateData.group()
        group.players.add(player)
        trday = CreateData.tr_day_for_group(group)
        trday.visitors.add(player)
        
    
        trday.available_status = GroupTrainingDay.AVAILABLE
        trday.save();
        utils.schange_tr_day_status(trday,GroupTrainingDay.CANCELLED)
        
        visitor = trday.visitors.first();
        self.assertEqual (visitor.bonus_lesson, 1)
    
    # если занятие не доступно то всем начисляется 1 отыгрышь
    def test_cancel_lesson_for_visitor(self)-> None:
        
        player = CreateData.group_player(tg_id=350490234, first_name="Nikita")
      
        group = CreateData.group()
        group.players.add(player)
        trday = CreateData.tr_day_for_group(group)
        trday.visitors.add(player)
        
        trday.available_status = GroupTrainingDay.AVAILABLE
        trday.save();
        utils.change_tr_day_status(trday,GroupTrainingDay.NOTAVAILABLE)
        
        visitor = trday.visitors.first();
        self.assertEqual (visitor.bonus_lesson, 1)
        
    # если у ученика занятие по расписанию группы, то ему начисляется в личный кабинет одна "отмена". 
    def test_cancel_lesson_for_pay_visitor(self)-> None:
        
        player = CreateData.group_player(tg_id=350490234, first_name="Nikita")

        group = CreateData.group()
        group.players.add(player)
        trday = CreateData.tr_day_for_group(group)
       
        
        trday.pay_visitors.add(player)
        trday.available_status = GroupTrainingDay.AVAILABLE
        trday.save();
        utils.change_tr_day_status(trday,GroupTrainingDay.CANCELLED)
        
        payVisitor = trday.pay_visitors.first();
        
        self.assertEqual (payVisitor.n_cancelled_lessons,1)
    
    # У игрока 0 отыгрышей и он записался на занятие за отыгрыш:   
    # в случае "отмены" занятия: ни отмена, ни отыгрыш не добавляется. 

    def test_cancel_lesson_for_pay_bonus_visitors(self)-> None:
        
        player = CreateData.group_player(tg_id=350490234, first_name="Nikita")

        group = CreateData.group()
        group.players.add(player)
        trday = CreateData.tr_day_for_group(group)
        trday.pay_bonus_visitors.add(player)
        
    
        trday.available_status = GroupTrainingDay.AVAILABLE
        trday.save();
        utils.change_tr_day_status(trday,GroupTrainingDay.CANCELLED)
        
        payVisitor = trday.pay_bonus_visitors.first()
    
        self.assertEqual (payVisitor.n_cancelled_lessons,0)
        self.assertEqual (payVisitor.bonus_lesson,0)
        

   