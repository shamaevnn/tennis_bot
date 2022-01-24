import telegram
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from admin_bot.ind_train import static_text
from admin_bot.ind_train.keyboards import how_many_trains_to_save_keyboard
from admin_bot.ind_train.manage_data import (
    PERMISSION_FOR_IND_TRAIN,
    AMOUNT_OF_IND_TRAIN,
    PERMISSION_YES,
    AMOUNT_ONE,
)
from base.common_for_bots.static_text import DATE_INFO, ATTENTION
from base.models import GroupTrainingDay, Player
from base.common_for_bots.utils import bot_edit_message, get_time_info_from_tr_day
from player_bot.menu_and_commands.keyboards import construct_main_menu
from player_bot.take_lesson.individual.static_text import (
    COACH_CONFIRMED_TRAIN,
    COACH_CANCELLED_TRAIN,
)
from tennis_bot.settings import TELEGRAM_TOKEN


def permission_for_ind_train(update: Update, context: CallbackContext):
    permission, tg_id, tr_day_id = update.callback_query.data[
        len(PERMISSION_FOR_IND_TRAIN) :
    ].split("|")

    player = Player.objects.get(tg_id=tg_id)
    tr_day = GroupTrainingDay.objects.filter(id=tr_day_id)

    if tr_day.exists():
        tr_day = tr_day.first()
        time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
        date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)
        markup = None

        if permission == PERMISSION_YES:
            markup = how_many_trains_to_save_keyboard(tr_day_id=tr_day_id)
            admin_text = static_text.HOW_MANY_TRAINS_TO_SAVE
            player_text = COACH_CONFIRMED_TRAIN.format(date_info=date_info)
        else:
            admin_text = static_text.WILL_SAY_THAT_TRAIN_IS_CANCELLED.format(
                player.last_name, player.first_name, date_info
            )
            player_text = COACH_CANCELLED_TRAIN.format(
                attention=ATTENTION, date_info=date_info
            )
            tr_day.delete()

        tennis_bot = telegram.Bot(TELEGRAM_TOKEN)
        tennis_bot.send_message(
            chat_id=player.tg_id,
            text=player_text,
            reply_markup=construct_main_menu(player),
            parse_mode=ParseMode.HTML,
        )
    else:
        admin_text = static_text.TRAIN_IS_ALREADY_CANCELLED
        markup = None

    bot_edit_message(context.bot, admin_text, update, markup=markup)


def save_many_ind_trains(update: Update, context: CallbackContext):
    tr_day_id, num_lessons = update.callback_query.data[
        len(AMOUNT_OF_IND_TRAIN) :
    ].split("|")
    tr_day = GroupTrainingDay.objects.get(id=tr_day_id)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    text = static_text.WISH_GOOD_TRAIN.format(date_tlg, day_of_week, time_tlg)
    if num_lessons == AMOUNT_ONE:
        text += static_text.SAVED_ONCE
    else:
        tr_day.create_tr_days_for_future()
        text += static_text.SAVED_2_MONTHS_AHEAD

    bot_edit_message(context.bot, text, update)
