import re

from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from base.utils.parent_utils import create_child
from base.models import Player
from admin_bot.go_to_site.keyboards import go_to_site_set_up_personal_data
from base.common_for_bots.tasks import send_message_to_coaches
from admin_bot.go_to_site.static_text import NEW_CLIENT_HAS_COME
from parent_bot.menu_and_commands.handlers import INSERT_PHONE_NUMBER
from parent_bot.menu_and_commands.keyboards import construct_parent_main_menu
from parent_bot.registration.static_text import FIRST_TIME_INSERT_PHONE_NUMBER, WRONG_PHONE_NUMBER_FORMAT, \
    I_WILL_TEXT_AS_SOON_AS_COACH_CONFIRM, CHILD_OK


def get_first_last_name(update: Update, context: CallbackContext):
    player, _ = Player.get_player_and_created(update, context)
    text = update.message.text

    last_name, first_name = text.split(' ')
    player.last_name = last_name
    player.first_name = first_name
    player.save()

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
        player, _ = Player.get_player_and_created(update, context)
        player.phone_number = int(phone_number_candidate[0])
        player.save()

        update.message.reply_text(
            text=I_WILL_TEXT_AS_SOON_AS_COACH_CONFIRM,
            reply_markup=construct_parent_main_menu()
        )

        send_message_to_coaches(
            text=NEW_CLIENT_HAS_COME.format(player),
            reply_markup=go_to_site_set_up_personal_data(player.id)
        )

    return ConversationHandler.END


def get_child_first_last_name(update: Update, context: CallbackContext):
    player = create_child(update)
    text = update.message.text
    last_name, first_name = text.split(' ')
    player.last_name = last_name
    player.first_name = first_name
    player.save()

    update.message.reply_text(
        text=CHILD_OK.format(first_name=first_name, last_name=last_name)
    )
    return ConversationHandler.END
