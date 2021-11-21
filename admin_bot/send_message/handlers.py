from telegram.ext import ConversationHandler

from admin_bot.send_message.keyboards import construct_menu_groups_for_send_message
from admin_bot.send_message import static_text
from base.common_for_bots.static_text import UP_TO_YOU
from base.models import TrainingGroup, Player, AlertsLog
from base.common_for_bots.utils import bot_edit_message
from base.common_for_bots.tasks import clear_broadcast_messages
from admin_bot.send_message.manage_data import SEND_MESSAGE

GROUP_IDS, TEXT_TO_SEND = 2, 3


def select_groups_where_should_send(update, context):
    text = static_text.WHOM_TO_SEND_TO

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
            text = static_text.CHOOSE_GROUP_AFTER_THAT_CONFIRM
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
            text = static_text.SENDING_TO_ALL_GROUPS_TYPE_TEXT

            banda_groups = TrainingGroup.objects.filter(status=TrainingGroup.STATUS_GROUP,
                                                        max_players__gt=1).distinct()
            players = Player.objects.filter(traininggroup__in=banda_groups).distinct()

        elif -2 in list_of_group_ids:
            # pressed 'send to all'
            text = static_text.WILL_SEND_TO_ALL_TYPE_TEXT
            players = Player.objects.filter(status__in=[Player.STATUS_TRAINING,
                                                      Player.STATUS_ARBITRARY,
                                                      Player.STATUS_IND_TRAIN])
        elif -3 in list_of_group_ids:
            # pressed 'send to free view_schedule'
            text = static_text.WILL_SEND_TO_FREE_SCHEDULE
            players = Player.objects.filter(status=Player.STATUS_ARBITRARY)

        else:
            text = static_text.WILL_SEND_TO_THE_FOLLOWING_GROUPS

            group_names = "\n".join(list(TrainingGroup.objects.filter(id__in=list_of_group_ids).values_list('name', flat=True)))
            text += group_names
            text += static_text.TYPE_TEXT_OF_MESSAGE

            players = Player.objects.filter(traininggroup__in=list_of_group_ids).distinct()

        objs = [AlertsLog(player=player, alert_type=AlertsLog.CUSTOM_COACH_MESSAGE) for player in players]
        AlertsLog.objects.bulk_create(objs)

        text += static_text.OR_PRESS_CANCEL
        bot_edit_message(context.bot, text, update)

        return TEXT_TO_SEND

    else:
        select_groups_where_should_send(update, context)


def receive_text_and_send(update, context):
    text = update.message.text

    if text == static_text.CANCEL_COMMAND:
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
            chat_ids=player_ids,
            message=text
        )

        alert_instances.update(is_sent=True, info=text)

        update.message.reply_text(
            text=static_text.IS_SENT
        )

        return ConversationHandler.END
