from base.utils import construct_main_menu
from tele_interface.handlers import update_user_info


def start(bot, update, user):
    update_user_info(update, user)
    bot.send_message(user.id, 'Я здесь', reply_markup=construct_main_menu(user, user.status))