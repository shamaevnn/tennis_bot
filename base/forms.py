import calendar
from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import ExpressionWrapper, F, DateTimeField, Count
from django.utils.safestring import mark_safe

from base.models import TrainingGroup, GroupTrainingDay, Player
from base.django_admin.utils import send_alert_about_changing_tr_day_status, send_alert_about_changing_tr_day_time
from player_bot.menu_and_commands.keyboards import construct_main_menu
from base.common_for_bots.utils import DT_BOT_FORMAT, TM_TIME_SCHEDULE_FORMAT, moscow_datetime
from base.common_for_bots.tasks import clear_broadcast_messages
from base.django_admin.static_text import ERROR_LIMIT_MAX_PLAYERS, ERROR_MAX_PLAYERS_IN_FUTURE, \
    ERROR_CANT_ADD_NEW_TRAIN
from player_bot.skip_lesson.static_text import CANCEL_TRAIN_PLUS_BONUS_LESSON
from player_bot.registration.static_text import NOW_YOU_HAVE_ACCESS_CONGRATS
from base.common_for_bots.static_text import from_eng_to_rus_day_week


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'parent', 'status', 'time_before_cancel',
                  'bonus_lesson', 'add_info']

    def clean(self):
        if 'status' in self.changed_data:
            new_status = self.cleaned_data.get('status')
            if self.instance.status == Player.STATUS_WAITING and (
                    new_status == Player.STATUS_ARBITRARY or new_status == Player.STATUS_TRAINING):
                text = NOW_YOU_HAVE_ACCESS_CONGRATS
                reply_markup = construct_main_menu(self.instance)

                clear_broadcast_messages(
                    chat_ids=[self.instance.id],
                    message=text,
                    reply_markup=reply_markup
                )


class TrainingGroupForm(forms.ModelForm):
    class Meta:
        model = TrainingGroup
        fields = ['name', 'players', 'max_players', 'status', 'level', 'tarif_for_one_lesson',
                  'available_for_additional_lessons']

    def clean(self):
        users = self.cleaned_data.get('users')
        max_players = self.cleaned_data.get('max_players')
        if users.count() > max_players:
            raise ValidationError(
                {'max_players': ERROR_LIMIT_MAX_PLAYERS.format(max_players, users.count())})

        if 'users' in self.changed_data:
            tr_day = GroupTrainingDay.objects.filter(
                group__max_players__gt=1,
                group=self.instance,
                is_available=True
            ).annotate(
                start=ExpressionWrapper(F('start_time') + F('date'), output_field=DateTimeField()),
                group_users_cnt=Count('group__users', distinct=True),
                absent_cnt=Count('absent', distinct=True),
                visitors_cnt=Count('visitors', distinct=True),
                pay_visitors_cnt=Count('pay_visitors', distinct=True),
                pay_bonus_visitors_cnt=Count('pay_bonus_visitors', distinct=True),
                max_players=F('group__max_players')
            ).filter(
                start__gte=moscow_datetime(datetime.now()),
                group_users_cnt__lt=users.count(),
                max_players=F('visitors_cnt') +
                            F('pay_visitors_cnt') +
                            F('pay_bonus_visitors_cnt') +
                            F('group_users_cnt') -
                            F('absent_cnt')
            ).distinct().values('id', 'date', 'start_time')
            if tr_day.exists():
                error_ids = "\n".join(['<a href="http://vladlen82.fvds.ru/tgadmin/base/grouptrainingday/{}/change/">{} {}</a>'.format(x['id'], x['date'], x['start_time']) for x in tr_day])
                error_text = f"{ERROR_MAX_PLAYERS_IN_FUTURE}:\n{error_ids}"
                raise ValidationError(
                    {'users': mark_safe(error_text)})


class GroupTrainingDayForm(forms.ModelForm):
    class Meta:
        model = GroupTrainingDay
        fields = [
            'group',
            'absent',
            'visitors',
            'pay_visitors',
            'pay_bonus_visitors',
            'date',
            'is_available',
            'is_individual',
            'tr_day_status',
            'start_time',
            'duration'
        ]

    def clean(self):
        def send_alert_about_cancel_in_visitors(self, type_of_visitors='visitors'):
            canceled_users = None
            if type_of_visitors == 'visitors':
                if self.cleaned_data.get(type_of_visitors).count() < self.instance.visitors.count():
                    canceled_users = self.instance.visitors.all().exclude(
                        id__in=self.cleaned_data.get(type_of_visitors))
            elif type_of_visitors == 'pay_visitors':
                if self.cleaned_data.get(type_of_visitors).count() < self.instance.pay_visitors.count():
                    canceled_users = self.instance.pay_visitors.all().exclude(
                        id__in=self.cleaned_data.get(type_of_visitors))
            elif type_of_visitors == 'pay_bonus_visitors':
                if self.cleaned_data.get(type_of_visitors).count() < self.instance.pay_bonus_visitors.count():
                    canceled_users = self.instance.pay_bonus_visitors.all().exclude(
                        id__in=self.cleaned_data.get(type_of_visitors))

            if canceled_users:
                text = CANCEL_TRAIN_PLUS_BONUS_LESSON.format(self.cleaned_data.get("date"))

                clear_broadcast_messages(
                    list(canceled_users.values_list('id', flat=True)),
                    text,
                    reply_markup=construct_main_menu()
                )

                canceled_users.update(bonus_lesson=F('bonus_lesson') + 1)

        group = self.cleaned_data.get('group')

        if not group:
            raise ValidationError('Не выбрана группа')

        current_amount_of_players = self.cleaned_data.get('visitors').count() + \
                                    self.cleaned_data.get('pay_visitors').count() + \
                                    self.cleaned_data.get('pay_bonus_visitors').count() + \
                                    group.users.count() - self.cleaned_data.get('absent').count()

        if group.available_for_additional_lessons:
            if current_amount_of_players > 6:
                raise ValidationError(ERROR_LIMIT_MAX_PLAYERS.format(6, current_amount_of_players))
        else:
            if current_amount_of_players > group.max_players:
                raise ValidationError(ERROR_LIMIT_MAX_PLAYERS.format(group.max_players, current_amount_of_players))

        if 'start_time' in self.changed_data or 'duration' in self.changed_data or 'date' in self.changed_data:
            """
                Если добавляется новый grouptrainingday, то нужно
                проверить, не накладывается ли время тренировки
                на уже существущие.
            """
            exist_trainings = GroupTrainingDay.objects.filter(date=self.cleaned_data.get('date'))
            start_time = datetime.combine(self.cleaned_data.get('date'), self.cleaned_data.get('start_time'))

            for train in exist_trainings:
                exist_train_start_time = datetime.combine(train.date, train.start_time)
                if exist_train_start_time <= start_time < exist_train_start_time + train.duration:
                    raise ValidationError(ERROR_CANT_ADD_NEW_TRAIN.format(train.start_time, train.duration))

            # send alert to players about changing lesson parameters
            # check only existing tr_days
            if GroupTrainingDay.objects.filter(group=self.cleaned_data.get('group'), date=self.cleaned_data.get('date'),
                                               start_time=self.cleaned_data.get('start_time'),
                                               duration=self.cleaned_data.get('duration'),
                                               ).count():
                changed_data_custom = []
                before_after_text = ''
                if 'start_time' in self.changed_data:
                    changed_data_custom.append('время начала тренировки')
                    before_after_text += self.instance.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
                    before_after_text += f" 🔜 {self.cleaned_data.get('start_time').strftime(TM_TIME_SCHEDULE_FORMAT)}\n"
                if 'duration' in self.changed_data:
                    changed_data_custom.append('продолжительность занятия')
                    before_after_text += str(self.instance.duration)
                    before_after_text += f" 🔜 {self.cleaned_data.get('duration')}\n"
                if 'date' in self.changed_data:
                    changed_data_custom.append('дата проведения занятия')
                    before_after_text += self.instance.date.strftime(DT_BOT_FORMAT)
                    before_after_text += f" 🔜 {self.cleaned_data.get('date').strftime(DT_BOT_FORMAT)}"

                day_of_week = from_eng_to_rus_day_week[calendar.day_name[self.instance.date.weekday()]]
                text = f'⚠️ATTENTION⚠️\n' \
                       f'Изменились следующие параметры тренировки {self.instance.date.strftime(DT_BOT_FORMAT)}' \
                       f' ({day_of_week}): {", ".join(changed_data_custom)}\n' \
                       f'{before_after_text}'
                send_alert_about_changing_tr_day_time(self.instance, text)

        if 'is_available' in self.changed_data:  # если статут дня меняется, то отсылаем алерт об изменении
            send_alert_about_changing_tr_day_status(self.instance, self.cleaned_data.get('is_available'))

        if 'visitors' in self.changed_data:
            send_alert_about_cancel_in_visitors(self, 'visitors')

        if 'pay_visitors' in self.changed_data:
            send_alert_about_cancel_in_visitors(self, 'pay_visitors')

        if 'pay_bonus_visitors' in self.changed_data:
            send_alert_about_cancel_in_visitors(self, 'pay_bonus_visitors')