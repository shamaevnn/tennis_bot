from datetime import datetime, date

from django.contrib import admin

# Register your models here.
from django.db.models import Q
from django.utils.http import urlencode

from .common_for_bots.utils import get_prev_month, get_next_month
from .common_for_bots.static_text import from_digit_to_month
from .forms import PlayerForm, TrainingGroupForm, GroupTrainingDayForm
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import ValidationError
from django import forms
from django.shortcuts import redirect
from django.utils.html import format_html

from .models import (
    TrainingGroup,
    Player,
    GroupTrainingDay,
    Payment,
    Photo,
    User,
    PlayerCancelLesson,
)
from .utils.change_available_status import (
    change_tr_day_available_status_and_send_alert,
)


class PlayerTabularForm(forms.ModelForm):
    def clean(self):
        tr_group = self.cleaned_data.get("traininggroup")
        if tr_group and tr_group.status == TrainingGroup.STATUS_GROUP:
            players = tr_group.players.all()
            max_players = tr_group.max_players
            if players.count() > max_players:
                raise ValidationError(
                    {
                        "traininggroup": "Количество игроков в группе должно быть не больше {}, вы указали {}.".format(
                            max_players, players.count() + 1
                        )
                    }
                )


class PlayerTabularInline(admin.StackedInline):
    model = TrainingGroup.players.through
    max_num = 2
    form = PlayerTabularForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name")


@admin.register(PlayerCancelLesson)
class PlayerCancelLessonAdmin(admin.ModelAdmin):
    list_display = ("player", "date", "n_cancelled_lessons")

    date_hierarchy = "date"

    def changelist_view(self, request, extra_context=None):
        """
        Если заходим на главную страницу,
        то сразу редиректим с фильтрами на текущий месяц
        """
        if (
            request.GET
            or "/tgadmin/base/playercancellesson/?date__year"
            in request.META.get("HTTP_REFERER")
        ):
            return super().changelist_view(request, extra_context=extra_context)

        today_date = datetime.now().date()
        params = ["month", "year"]
        field_keys = ["{}__{}".format(self.date_hierarchy, i) for i in params]
        field_values = [getattr(today_date, i) for i in params]
        query_params = dict(zip(field_keys, field_values))
        url = "{}?{}".format(request.path, urlencode(query_params))
        return redirect(url)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    form = PlayerForm
    inlines = [PlayerTabularInline]
    list_display = ("tg_id", "first_name", "last_name", "phone_number", "status")
    search_fields = ("first_name", "last_name")
    readonly_fields = ("tg_id", "cancels_for_player")
    list_filter = ("status",)
    ordering = ["first_name"]

    def cancels_for_player(self, obj: Player):
        today = date.today()

        prev_month = get_prev_month(today.month)
        first_date_of_prev_month = today.replace(month=prev_month, day=1)

        next_month = get_next_month(today.month)
        first_date_of_next_month = today.replace(month=next_month, day=1)

        player_cancels_for_three_months = PlayerCancelLesson.objects.filter(
            player=obj,
            date__gte=first_date_of_prev_month,
            date__lte=first_date_of_next_month,
        )

        cancels_by_months = []
        for x in player_cancels_for_three_months.values(
            "n_cancelled_lessons", "date__month"
        ):
            month = from_digit_to_month[x["date__month"]]
            n_cancelled = x["n_cancelled_lessons"]
            cancels_by_months.append(f"{month} -- {n_cancelled}")

        return ", ".join(cancels_by_months)

    cancels_for_player.short_description = "Отмены для игрока"


class DefaultGroupStatus(SimpleListFilter):
    title = "Статус"

    parameter_name = "status"

    def lookups(self, request, model_admin):
        return TrainingGroup.GROUP_STATUSES

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": cl.get_query_string(
                    {
                        self.parameter_name: lookup,
                    },
                    [],
                ),
                "display": title,
            }

    def queryset(self, request, queryset):
        if self.value() in (
            TrainingGroup.STATUS_SECTION,
            TrainingGroup.STATUS_FEW,
            TrainingGroup.STATUS_4IND,
            TrainingGroup.STATUS_GROUP,
        ):
            return queryset.filter(status=self.value())
        elif self.value() is None:
            return queryset.filter(status=TrainingGroup.STATUS_GROUP)


def make_group_orange(modeladmin, request, queryset):
    queryset.update(level=TrainingGroup.LEVEL_ORANGE)


def make_group_green(modeladmin, request, queryset):
    queryset.update(level=TrainingGroup.LEVEL_GREEN)


make_group_orange.short_description = "Сделать группу 🧡"
make_group_green.short_description = "Сделать группу 🍏"


@admin.register(TrainingGroup)
class TrainingGroupAdmin(admin.ModelAdmin):
    form = TrainingGroupForm
    list_display = (
        "name",
        "max_players",
        "level",
        "available_for_additional_lessons",
        "tarif_for_one_lesson",
    )
    filter_horizontal = ("players",)
    list_filter = [DefaultGroupStatus]
    actions = [make_group_green, make_group_orange]


def make_trday_unavailable(modeladmin, request, queryset):
    change_available_state(request, queryset, GroupTrainingDay.NOT_AVAILABLE)


def make_trday_available(modeladmin, request, queryset):
    change_available_state(request, queryset, GroupTrainingDay.AVAILABLE)


def make_trday_cancelled(modeladmin, request, queryset):
    change_available_state(request, queryset, GroupTrainingDay.CANCELLED)


def change_available_state(request, queryset, new_available_status):
    # исключает попадание дней имеющих данный статус
    tr_days = queryset.exclude(available_status=new_available_status).all()

    for day in tr_days:
        change_tr_day_available_status_and_send_alert(day, new_available_status)


make_trday_unavailable.short_description = "Сделать выбранные дни недоступными"
make_trday_available.short_description = "Сделать выбранные дни доступными"

make_trday_cancelled.short_description = "Отменить занятие в выбранные дни"


@admin.register(GroupTrainingDay)
class GroupTrainingDayAdmin(admin.ModelAdmin):
    form = GroupTrainingDayForm
    list_display = (
        "group",
        "date",
        "start_time",
        "duration",
        "status",
        "available_status",
    )

    list_filter = ("available_status", "status", "date", "group")
    filter_horizontal = ("visitors", "pay_visitors", "pay_bonus_visitors", "absent")
    date_hierarchy = "date"
    actions = [make_trday_unavailable, make_trday_available, make_trday_cancelled]
    ordering = ["date", "start_time"]
    change_form_template = "admin/tennis_bot/GroupTrainingDay/submit_line.html"

    def get_queryset(self, request):
        return (
            super(GroupTrainingDayAdmin, self)
            .get_queryset(request)
            .filter(is_deleted=False)
        )

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field=from_field)
        # Cache object for use in formfield_for_manytomany
        request.report_obj = obj
        return obj

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "absent" and hasattr(request, "report_obj"):
            kwargs["queryset"] = Player.objects.filter(
                traininggroup__id=request.report_obj.group.id
            )
        if db_field.name == "visitors" and hasattr(request, "report_obj"):
            kwargs["queryset"] = Player.objects.exclude(
                Q(traininggroup__id=request.report_obj.group.id)
                | Q(
                    id__in=request.report_obj.pay_visitors.all()
                    .union(request.report_obj.pay_bonus_visitors.all())
                    .values("id")
                )
            )
        if db_field.name == "pay_visitors" and hasattr(request, "report_obj"):
            kwargs["queryset"] = Player.objects.exclude(
                Q(traininggroup__id=request.report_obj.group.id)
                | Q(
                    id__in=request.report_obj.visitors.all()
                    .union(request.report_obj.pay_bonus_visitors.all())
                    .values("id")
                )
            )
        if db_field.name == "pay_bonus_visitors" and hasattr(request, "report_obj"):
            kwargs["queryset"] = Player.objects.exclude(
                Q(traininggroup__id=request.report_obj.group.id)
                | Q(
                    id__in=request.report_obj.visitors.all()
                    .union(request.report_obj.pay_visitors.all())
                    .values("id")
                )
            )

        return super(GroupTrainingDayAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )

    def changelist_view(self, request, extra_context=None):
        if (
            request.GET
            or "/tgadmin/base/grouptrainingday/?date__year"
            in request.META.get("HTTP_REFERER")
        ):
            return super().changelist_view(request, extra_context=extra_context)

        today_date = datetime.now().date()
        params = ["month", "year"]
        field_keys = ["{}__{}".format(self.date_hierarchy, i) for i in params]
        field_values = [getattr(today_date, i) for i in params]
        query_params = dict(zip(field_keys, field_values))
        url = "{}?{}".format(request.path, urlencode(query_params))
        return redirect(url)

    def response_add(self, request, obj: GroupTrainingDay, post_url_continue=None):
        if "_saveonce" in request.POST:
            pass
        else:
            obj.create_tr_days_for_future()

        return super().response_add(request, obj)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "month",
        "year",
        "theory_amount",
        "n_fact_visiting",
        "fact_amount",
    )
    list_filter = ("year", "month", "player")
    search_fields = ("player__first_name", "player__last_name")
    readonly_fields = ("theory_amount", "n_fact_visiting")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("pk", "show_url", "thumb")
    readonly_fields = ("telegram_id",)

    def show_url(self, obj):
        return format_html('<a href="{}">{}</a>'.format(obj.url, obj.text))

    show_url.allow_tags = True

    def thumb(self, obj):
        return format_html("<img src='{}' width='40' height='40'/>".format(obj.url))
