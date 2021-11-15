from django.db.models import QuerySet
from admin_bot.view_schedule import static_text
from base.common_for_bots.static_text import DATE_INFO
from base.common_for_bots.utils import get_time_info_from_tr_day
from base.models import User, GroupTrainingDay, TrainingGroup


def schedule_users_info(users: QuerySet[User]):
    return '\n'.join((
        f"{i + 1}. {x['last_name']} {x['first_name']}"
        for i, x in enumerate(users.values('first_name', 'last_name').order_by('last_name'))
    ))


class ViewSchedule:
    @staticmethod
    def _get_tr_day_status(tr_day: GroupTrainingDay) -> str:
        if tr_day.is_individual:
            return static_text.INDIVIDUAL_TRAIN
        else:
            if tr_day.tr_day_status == GroupTrainingDay.RENT_COURT_STATUS:
                return static_text.RENT
            else:
                return static_text.MY_TRAIN

    @staticmethod
    def _get_group_name(tr_day: GroupTrainingDay) -> str:
        return tr_day.group.name

    @staticmethod
    def _get_availability(tr_day: GroupTrainingDay) -> str:
        return static_text.NO_TRAIN if not tr_day.is_available else ''

    @staticmethod
    def _get_group_players(tr_day: GroupTrainingDay) -> str:
        group_players = tr_day.group.users.all().difference(tr_day.absent.all())
        return f'{static_text.PLAYERS_FROM_GROUP}:\n{schedule_users_info(group_players)}'

    @staticmethod
    def _get_visitors(tr_day: GroupTrainingDay) -> str:
        visitors = tr_day.visitors
        if visitors.exists():
            return f'{static_text.HAVE_COME_FROM_OTHERS}:\n{schedule_users_info(visitors)}'
        return ''

    @staticmethod
    def _get_pay_visitors(tr_day: GroupTrainingDay) -> str:
        pay_visitors = tr_day.pay_visitors
        if pay_visitors.exists():
            return f'{static_text.HAVE_COME_FOR_MONEY}:\n{schedule_users_info(pay_visitors)}'
        return ''

    @staticmethod
    def _get_pay_bonus_visitors(tr_day: GroupTrainingDay) -> str:
        pay_bonus_visitors = tr_day.pay_bonus_visitors
        if pay_bonus_visitors.exists():
            return f'{static_text.HAVE_COME_FOR_PAY_BONUS_LESSON}:\n{schedule_users_info(pay_bonus_visitors)}'
        return ''

    @staticmethod
    def _get_absents(tr_day: GroupTrainingDay) -> str:
        absents = tr_day.absent
        if absents.exists():
            return f'{static_text.ARE_ABSENT}:\n{schedule_users_info(absents)}'
        return ''

    @staticmethod
    def _get_group_level(tr_day: GroupTrainingDay) -> str:
        return f"{TrainingGroup.GROUP_LEVEL_DICT[tr_day.group.level]}"

    @staticmethod
    def _get_players_info(tr_day: GroupTrainingDay) -> str:
        if tr_day.is_individual or tr_day.tr_day_status == GroupTrainingDay.RENT_COURT_STATUS:
            return ''
        else:
            group_level = ViewSchedule._get_group_level(tr_day)
            group_players = ViewSchedule._get_group_players(tr_day)
            visitors = ViewSchedule._get_visitors(tr_day)
            pay_visitors = ViewSchedule._get_pay_visitors(tr_day)
            pay_bonus_visitors = ViewSchedule._get_pay_bonus_visitors(tr_day)
            absents = ViewSchedule._get_absents(tr_day)
            return '\n'.join([
                group_level, group_players, visitors, pay_visitors, pay_bonus_visitors, absents
            ])

    @staticmethod
    def _get_general_info(tr_day: GroupTrainingDay) -> str:
        availability = ViewSchedule._get_availability(tr_day)
        tr_day_status = ViewSchedule._get_tr_day_status(tr_day)
        group_name = ViewSchedule._get_group_name(tr_day)
        texts = list(filter)
        return '\n'.join([
            availability, tr_day_status, group_name
        ])

    @staticmethod
    def _get_date_info(tr_day: GroupTrainingDay) -> str:
        time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
        return DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    @staticmethod
    def get_text(tr_day: GroupTrainingDay) -> str:
        general_info = ViewSchedule._get_general_info(tr_day)
        users_info = ViewSchedule._get_players_info(tr_day)
        date_info = ViewSchedule._get_date_info(tr_day)
        return '\n'.join([
            general_info, users_info, date_info
        ])
