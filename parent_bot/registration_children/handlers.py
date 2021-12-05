from telegram import Update
from telegram.ext import CallbackContext
from parent_bot.menu_and_commands.keyboards import reg_child_butten
from parent_bot.player_info.static_text import CHILDREN_REG_BUTTON
from parent_bot.registration.static_text import CHILDREN_REG_FIO, NOT_CHILDREN, LIST_CHILDREN
from parent_bot.registration.utils import check_status_decor
from base.models import Player
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from parent_bot.registration_children.manage_data import CHILD_REG

INSERT_CHILD_FIO = range(1)


def get_children_reg(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=CHILDREN_REG_FIO)
    return INSERT_CHILD_FIO


@check_status_decor
def get_children_chek(update: Update, context: CallbackContext):
    player, _ = Player.get_player_and_created(update, context)
    if not player.children.all().exists():
        context.bot.send_message(chat_id=update.effective_chat.id, text=NOT_CHILDREN, reply_markup=reg_child_butten())
    else:
        buttons = []
        row = []
        FIO = []
        children_fio = player.children.all().values('first_name', 'last_name')
        for fio in children_fio:
            first_last_name = str(fio['first_name']) + " " + str(fio['last_name'])
            if not first_last_name in FIO:
                print(first_last_name)
                row.append(
                    InlineKeyboardButton(
                        text=first_last_name,
                        callback_data=f"{first_last_name}"
                    )
                )
                buttons.append(row)
                FIO.append(first_last_name)
        for i in FIO:
            print("----" + i + "----")
        buttons.append([
            InlineKeyboardButton(
                text=CHILDREN_REG_BUTTON,
                callback_data=CHILD_REG
            )
        ])
        context.bot.send_message(chat_id=update.effective_chat.id, text=LIST_CHILDREN,
                                 reply_markup=InlineKeyboardMarkup(buttons))
