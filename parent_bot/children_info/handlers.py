from telegram import Update
from telegram.ext import CallbackContext

from base.models import Player
from parent_bot.child_registration.keyboards import reg_child_button
from .keyboards import list_all_children_with_add_one_more_button
from .static_text import NOT_CHILDREN, LIST_CHILDREN
from parent_bot.menu_and_commands.utils import check_status_decor


@check_status_decor
def list_all_children(update: Update, context: CallbackContext):
    """показывает список всех детей + кнопку добавить еще одного"""
    parent, _ = Player.get_player_and_created(update, context)
    if not parent.children.all().exists():
        update.message.reply_text(
            text=NOT_CHILDREN,
            reply_markup=reg_child_button(),
        )
        return

    update.message.reply_text(
        text=LIST_CHILDREN,
        reply_markup=list_all_children_with_add_one_more_button(parent)
    )
