import re

from telegram.ext import ConversationHandler

from admin_bot.keyboard_utils import go_to_site_set_up_personal_data
from admin_bot.static_text import NEW_CLIENT_HAS_COME
from base.models import User
from base.utils import construct_main_menu, clear_broadcast_messages
from tele_interface.handlers import INSERT_PHONE_NUMBER
from tele_interface.static_text import FIRST_TIME_INSERT_PHONE_NUMBER, WRONG_PHONE_NUMBER_FORMAT, \
    I_WILL_TEXT_AS_SOON_AS_COACH_CONFIRM
from tennis_bot.settings import ADMIN_TELEGRAM_TOKEN


def get_first_last_name(update, context):
    user, _ = User.get_user_and_created(update, context)
    text = update.message.text

    last_name, first_name = text.split(' ')
    user.last_name = last_name
    user.first_name = first_name
    user.save()

    update.message.reply_text(
        text=FIRST_TIME_INSERT_PHONE_NUMBER,
    )
    return INSERT_PHONE_NUMBER


def get_phone_number(update, context):
    user, _ = User.get_user_and_created(update, context)
    text = update.message.text
    phone_number_candidate = re.findall(r'\d+', text)

    if len(phone_number_candidate[0]) != 11:
        update.message.reply_text(
            text=WRONG_PHONE_NUMBER_FORMAT.format(len(phone_number_candidate[0])),
        )
        return INSERT_PHONE_NUMBER
    else:
        user.phone_number = int(phone_number_candidate[0])
        user.save()

        update.message.reply_text(
            text=I_WILL_TEXT_AS_SOON_AS_COACH_CONFIRM,
            reply_markup=construct_main_menu()
        )

        admins = User.objects.filter(is_staff=True)

        clear_broadcast_messages(
            user_ids=list(admins.values_list('id', flat=True)),
            message=NEW_CLIENT_HAS_COME.format(user),
            reply_markup=go_to_site_set_up_personal_data(user.id),
            tg_token=ADMIN_TELEGRAM_TOKEN,
        )

    return ConversationHandler.END