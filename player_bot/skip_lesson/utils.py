from datetime import datetime

from django.db.models import ExpressionWrapper, F, DurationField, Q

from player_bot.skip_lesson.static_text import USER_CANCELLED_IND_TRAIN, USER_SKIPPED_TRAIN_FOR_BONUS, \
    USER_SKIPPED_TRAIN_FOR_MONEY, USER_SKIPPED_TRAIN_FOR_PAY_BONUS, USER_SKIPPED_TRAIN_IN_HIS_GROUP, \
    CANT_CANCEL_LESSON_TOO_LATE, OKAY_TRAIN_CANCELLED
from base.common_for_bots.static_text import ATTENTION
from base.models import GroupTrainingDay
from base.common_for_bots.utils import get_actual_players_without_absent, moscow_datetime, create_calendar
from player_bot.skip_lesson.keyboards import construct_menu_skipping_much_lesson, \
    construct_detail_menu_for_skipping


def select_tr_days_for_skipping(user, **filters):
    now = moscow_datetime(datetime.now())
    available_grouptraining_days = GroupTrainingDay.objects.annotate(
        diff=ExpressionWrapper(
            F('start_time') + F('date') - now,
            output_field=DurationField()
        )
    ).filter(
        Q(group__users__in=[user]) |
        Q(visitors__in=[user]) |
        Q(pay_visitors__in=[user]) |
        Q(pay_bonus_visitors__in=[user]),
        date__gte=now.date(),
        diff__gt=user.time_before_cancel,
        **filters
    ).exclude(
        absent__in=[user]
    ).select_related('group').order_by('id').distinct('id')

    return available_grouptraining_days


def make_group_name_group_players_info_for_skipping(tr_day):
    all_players = get_actual_players_without_absent(tr_day).values('first_name', 'last_name')

    all_players = '\n'.join((f"{x['first_name']} {x['last_name']}" for x in all_players))
    if not tr_day.is_individual:
        group_name = f"{tr_day.group.name}\n"
        group_players = f'Присутствующие:\n{all_players}\n'
    else:
        group_name = "🧞‍♂индивидуальная тренировка🧞‍♂️\n"
        group_players = ''
    return group_name, group_players


def calendar_skipping(user, purpose, date_my):
    training_days = select_tr_days_for_skipping(user, date=date_my)
    if training_days.exists():
        if training_days.count() > 1:
            markup = construct_menu_skipping_much_lesson(training_days)
            text = 'Выбери время'
        else:
            training_day = training_days.first()
            group_name, group_players = make_group_name_group_players_info_for_skipping(training_day)

            markup, text = construct_detail_menu_for_skipping(training_day, purpose, group_name,
                                                              group_players)
    else:
        text = 'Нет тренировки в этот день, выбери другой.\n' \
               '✅ -- дни, доступные для отмены.'
        markup = create_calendar(purpose, date_my.year, date_my.month,
                                 list(select_tr_days_for_skipping(user).values_list('date', flat=True)))
    return text, markup


def handle_skipping_train(training_day, user, date_info):
    if datetime.combine(training_day.date, training_day.start_time) - moscow_datetime(
            datetime.now()) < user.time_before_cancel:
        text = CANT_CANCEL_LESSON_TOO_LATE.format(round(user.time_before_cancel.seconds / 3600))
        admin_text = ""
    else:
        text = OKAY_TRAIN_CANCELLED.format(date_info)

        if training_day.is_individual:
            training_day.delete()

            admin_text = USER_CANCELLED_IND_TRAIN.format(ATTENTION, user.first_name, user.last_name, date_info)
        else:
            if user in training_day.visitors.all():
                user.bonus_lesson += 1
                training_day.visitors.remove(user)
                admin_text = USER_SKIPPED_TRAIN_FOR_BONUS.format(user.first_name, user.last_name, date_info)
            elif user in training_day.pay_visitors.all():
                # в этом случае не должно поменяться кол-во отыгрышей
                training_day.pay_visitors.remove(user)
                admin_text = USER_SKIPPED_TRAIN_FOR_MONEY.format(user.first_name, user.last_name, date_info)
            elif user in training_day.pay_bonus_visitors.all():
                user.bonus_lesson += 1
                training_day.pay_bonus_visitors.remove(user)
                admin_text = USER_SKIPPED_TRAIN_FOR_PAY_BONUS.format(user.first_name, user.last_name, date_info)
            else:
                user.bonus_lesson += 1
                training_day.absent.add(user)
                admin_text = USER_SKIPPED_TRAIN_IN_HIS_GROUP.format(user.first_name, user.last_name, date_info)
            user.save()
    return text, admin_text
