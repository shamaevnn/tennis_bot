from telegram.ext import ConversationHandler

from admin_bot.handlers import GROUP_IDS, TEXT_TO_SEND
from admin_bot.send_message.keyboard_utils import construct_menu_groups_for_send_message
from admin_bot.static_text import WHOM_TO_SEND_TO, CHOOSE_GROUP_AFTER_THAT_CONFIRM, SENDING_TO_ALL_GROUPS_TYPE_TEXT, \
    WILL_SEND_TO_ALL_TYPE_TEXT, WILL_SEND_TO_FREE_SCHEDULE, WILL_SEND_TO_THE_FOLLOWING_GROUPS, TYPE_TEXT_OF_MESSAGE, \
    OR_PRESS_CANCEL, CANCEL_COMMAND, UP_TO_YOU, IS_SENT
from base.models import TrainingGroup, User, AlertsLog
from base.utils import bot_edit_message, clear_broadcast_messages
from tele_interface.manage_data import SEND_MESSAGE


def select_groups_where_should_send(update, context):
    text = WHOM_TO_SEND_TO

    banda_groups = TrainingGroup.objects.filter(
        status=TrainingGroup.STATUS_GROUP,
        max_players__gt=1,
        name__iregex=r'БАНДА',
    ).order_by('order')

    if update.callback_query:
        group_ids = update.callback_query.data[len(SEND_MESSAGE):].split("|")
        markup = construct_menu_groups_for_send_message(banda_groups, f'{update.callback_query.data}')

        if len(group_ids) == 2 and group_ids[-1] == '-1':
            # ['', '-1'] -- just pressed confirm
            text = CHOOSE_GROUP_AFTER_THAT_CONFIRM
        bot_edit_message(context.bot, text, update, markup)
        return GROUP_IDS

    else:
        markup = construct_menu_groups_for_send_message(banda_groups, f'{SEND_MESSAGE}')
        update.message.reply_text(
            text=text,
            reply_markup=markup
        )


def text_to_send(update, context):
    group_ids = update.callback_query.data[len(SEND_MESSAGE):].split("|")
    group_ids.remove('')
    if group_ids[-1] == '-1':  # if pressed "confirm"
        list_of_group_ids = list(set([int(x) for x in group_ids if x]))
        if 0 in list_of_group_ids:
            # pressed 'send to all groups'
            text = SENDING_TO_ALL_GROUPS_TYPE_TEXT

            banda_groups = TrainingGroup.objects.filter(status=TrainingGroup.STATUS_GROUP,
                                                        max_players__gt=1).distinct()
            players = User.objects.filter(traininggroup__in=banda_groups).distinct()

        elif -2 in list_of_group_ids:
            # pressed 'send to all'
            text = WILL_SEND_TO_ALL_TYPE_TEXT
            players = User.objects.filter(status__in=[User.STATUS_TRAINING,
                                                      User.STATUS_ARBITRARY,
                                                      User.STATUS_IND_TRAIN])
        elif -3 in list_of_group_ids:
            # pressed 'send to free schedule'
            text = WILL_SEND_TO_FREE_SCHEDULE
            players = User.objects.filter(status=User.STATUS_ARBITRARY)

        else:
            text = WILL_SEND_TO_THE_FOLLOWING_GROUPS

            group_names = "\n".join(list(TrainingGroup.objects.filter(id__in=list_of_group_ids).values_list('name', flat=True)))
            text += group_names
            text += TYPE_TEXT_OF_MESSAGE

            players = User.objects.filter(traininggroup__in=list_of_group_ids).distinct()

        objs = [AlertsLog(player=player, alert_type=AlertsLog.CUSTOM_COACH_MESSAGE) for player in players]
        AlertsLog.objects.bulk_create(objs)

        text += OR_PRESS_CANCEL
        bot_edit_message(context.bot, text, update)

        return TEXT_TO_SEND

    else:
        select_groups_where_should_send(update, context)


def receive_text_and_send(update, context):
    text = update.message.text

    if text == CANCEL_COMMAND:
        update.message.reply_text(
            text=UP_TO_YOU
        )
        return ConversationHandler.END

    else:
        alert_instances = AlertsLog.objects.filter(
            is_sent=False,
            tr_day__isnull=True,
            alert_type=AlertsLog.CUSTOM_COACH_MESSAGE,
            info__isnull=True
        ).distinct()
        player_ids = list(alert_instances.values_list('player', flat=True))

        clear_broadcast_messages(
            user_ids=player_ids,
            message=text
        )

        alert_instances.update(is_sent=True, info=text)

        update.message.reply_text(
            text=IS_SENT
        )

        return ConversationHandler.END