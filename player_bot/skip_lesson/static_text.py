from base.common_for_bots.static_text import ATTENTION

USER_CANCELLED_IND_TRAIN = '{}\n{} {} отменил индивидуальную тренировку\n{}'
USER_SKIPPED_TRAIN_FOR_BONUS = '{} {} пропускает тренировку за <b>отыгрыш</b>\n{}'
USER_SKIPPED_TRAIN_FOR_MONEY = '{} {} пропускает тренировку за <b>оплату</b>\n{}'
USER_SKIPPED_TRAIN_FOR_PAY_BONUS = '{} {} пропускает тренировку за <b>платный отыгрыш</b>\n{}'
USER_SKIPPED_TRAIN_IN_HIS_GROUP = '{} {} пропускает тренировку в <b>своей группе</b>\n{}'
SKIP_LESSON_BUTTON = 'Пропустить занятие'
CANT_CANCEL_LESSON_TOO_LATE = 'Неа, уже нельзя отменить занятие.\nКоличество часов, за которое тебе нужно отменять: {}'
OKAY_TRAIN_CANCELLED = 'Окей, занятие отменено.\n{}'
CANCEL_TRAIN_PLUS_BONUS_LESSON = f'{ATTENTION}\n' \
                       'У тебя есть запись на тренировку на <b> {}.</b>\n' \
                       '<b>Тренер ее отменил.</b> Но не отчаивайся, я добавлю тебе отыгрыш 🎾'