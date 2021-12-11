import re

from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from base.models import Player
from admin_bot.go_to_site.keyboards import go_to_site_set_up_personal_data
from base.common_for_bots.tasks import send_message_to_coaches
from admin_bot.go_to_site.static_text import NEW_PARENT_HAS_COME
from parent_bot.menu_and_commands.keyboards import construct_parent_main_menu
from .static_text import FIRST_TIME_INSERT_PHONE_NUMBER, WRONG_PHONE_NUMBER_FORMAT, \
    I_WILL_TEXT_AS_SOON_AS_COACH_CONFIRM, FIRST_TIME_GREETING, FIRST_TIME_INSERT_FIRST_LAST_MAME
from ..menu_and_commands.static_text import HELLO_PARENT

INSERT_FIO, INSERT_PHONE_NUMBER = range(2)


def start(update: Update, context: CallbackContext):
    parent, created = Player.get_player_and_created(update, context)

    if created:
        update.message.reply_text(
            text=FIRST_TIME_GREETING,
        )
        if parent.last_name and parent.first_name:
            update.message.reply_text(
                text=FIRST_TIME_INSERT_PHONE_NUMBER,
            )
            return INSERT_PHONE_NUMBER
        else:
            update.message.reply_text(
                text=FIRST_TIME_INSERT_FIRST_LAST_MAME,
            )
            return INSERT_FIO
    else:
        update.message.reply_text(
            text=HELLO_PARENT.format(first_name=parent.first_name),
            reply_markup=construct_parent_main_menu()
        )
        return ConversationHandler.END


def get_first_last_name(update: Update, context: CallbackContext):
    parent, _ = Player.get_player_and_created(update, context)
    text = update.message.text

    last_name, first_name = text.split(' ')
    parent.last_name = last_name
    parent.first_name = first_name
    parent.save()

    update.message.reply_text(
        text=FIRST_TIME_INSERT_PHONE_NUMBER,
    )
    return INSERT_PHONE_NUMBER


def get_phone_number(update: Update, context: CallbackContext):
    text = update.message.text
    phone_number_candidate = re.findall(r'\d+', text)

    if len(phone_number_candidate[0]) != 11:
        update.message.reply_text(
            text=WRONG_PHONE_NUMBER_FORMAT.format(len(phone_number_candidate[0])),
        )
        return INSERT_PHONE_NUMBER
    else:
        parent, _ = Player.get_player_and_created(update, context)
        parent.phone_number = int(phone_number_candidate[0])
        parent.save()

        update.message.reply_text(
            text=I_WILL_TEXT_AS_SOON_AS_COACH_CONFIRM,
            reply_markup=construct_parent_main_menu()
        )

        send_message_to_coaches(
            text=NEW_PARENT_HAS_COME.format(parent),
            reply_markup=go_to_site_set_up_personal_data(parent.id)
        )

    return ConversationHandler.END


