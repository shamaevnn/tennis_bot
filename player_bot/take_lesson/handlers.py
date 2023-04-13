from datetime import datetime

from telegram import Update
from telegram.ext import CallbackContext

from base.models import Player
from base.common_for_bots.utils import (
    moscow_datetime,
    bot_edit_message,
    create_calendar,
)
from player_bot.take_lesson.keyboards import choose_type_of_training_keyboard
from player_bot.take_lesson.individual.keyboards import (
    ind_train_choose_duration_keyboard,
)
from player_bot.take_lesson import manage_data
from player_bot.calendar.manage_data import CLNDR_ACTION_TAKE_GROUP
from player_bot.take_lesson.rent.keyboards import rent_choose_duration_keyboard
from player_bot.take_lesson.static_text import (
    CHOOSE_TYPE_OF_TRAIN,
    CHOOSE_DURATION_OF_TRAIN,
)
from player_bot.take_lesson.group.query import get_potential_days_for_group_training
from player_bot.registration.utils import check_status_decor
from player_bot.take_lesson.static_text import NO_GAMES_IN_MOMENT, YOU_SACRIFICE_ONE_GAME
from tennis_bot.settings import TARIF_ARBITRARY



@check_status_decor
def choose_type_of_training(update: Update, context: CallbackContext):
    markup = choose_type_of_training_keyboard()
    text = CHOOSE_TYPE_OF_TRAIN
    if update.callback_query:
        bot_edit_message(context.bot, text, update, markup)
    else:
        update.message.reply_text(text=text, reply_markup=markup)


@check_status_decor
def take_lesson(update: Update, context: CallbackContext):
    """записаться на тренировку"""
    player, _ = Player.get_player_and_created(update, context)
    tr_type = update.callback_query.data[len(manage_data.SELECT_TRAINING_TYPE) :]
    if tr_type == manage_data.TRAINING_GROUP:
        if player.bonus_lesson > 0:
            text = YOU_SACRIFICE_ONE_GAME
        else:
            text = NO_GAMES_IN_MOMENT
        training_days = get_potential_days_for_group_training(player).filter(
            date__gte=moscow_datetime(datetime.now()).date()
        )
        highlight_dates = list(training_days.values_list("date", flat=True))
        markup = create_calendar(
            CLNDR_ACTION_TAKE_GROUP, dates_to_highlight=highlight_dates
        )
    elif tr_type == manage_data.TRAINING_RENT:
        markup = rent_choose_duration_keyboard()
        text = CHOOSE_DURATION_OF_TRAIN
    elif tr_type == manage_data.TRAINING_IND:
        markup = ind_train_choose_duration_keyboard()
        text = CHOOSE_DURATION_OF_TRAIN
    else:
        return
    bot_edit_message(context.bot, text, update, markup)
