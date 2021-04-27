from base.models import TrainingGroup

HEY_I_MOVED_TO = "Привет! я переехал на @TennisTula_bot"
HOW_MANY_TRAINS_TO_SAVE = 'Сколько тренировок сохранить?'
WILL_SAY_THAT_TRAIN_IS_CANCELLED = 'Хорошо, сообщу {} {}, что тренировка  {} \n<b>{}</b> отменена.'
TRAIN_IS_ALREADY_CANCELLED = 'Тренировка уже отменена.'
DATE_INFO = '📅Дата: <b>{} ({})</b>\n' \
            '⏰Время: <b>{}</b>\n\n'
WISH_GOOD_TRAIN = f'Хорошо, приятной тренировки!\n' \
                  f'{DATE_INFO}'
SAVED_ONCE = "Сохранил единожды."
SAVED_2_MONTHS_AHEAD = "Сохранил на 2 месяца вперед."
ADMIN_TIME_SCHEDULE_BUTTON = 'Расписание'
ADMIN_SEND_MESSAGE = 'Отправить сообщение'
TRAIN_DAYS = 'Тренировочные дни'
NO_TRAINS_THIS_DAY = 'Нет тренировок в этот день'
WHOM_TO_SEND_TO = 'Кому отправить?'
CHOOSE_GROUP_AFTER_THAT_CONFIRM = 'Сначала выбери группу, а потом подтверждай.'
TYPE_TEXT_OF_MESSAGE = '\nВведи текст сообщения.'
SENDING_TO_ALL_GROUPS_TYPE_TEXT = f'Отправлю сообщение всем группам.{TYPE_TEXT_OF_MESSAGE}'
WILL_SEND_TO_ALL_TYPE_TEXT = f'Отправлю сообщение вообще всем.{TYPE_TEXT_OF_MESSAGE}'
WILL_SEND_TO_FREE_SCHEDULE = f'Отправлю сообщение тем, кто ходит по свободному графику.{TYPE_TEXT_OF_MESSAGE}'
WILL_SEND_TO_THE_FOLLOWING_GROUPS = f'Отправлю сообщение следующим группам:{TYPE_TEXT_OF_MESSAGE}'

OR_PRESS_CANCEL = ' Или нажми /cancel для отмены.'
CANCEL_COMMAND = '/cancel'
IS_SENT = 'Отправлено.'

NO_TRAIN = '❌нет тренировки❌'
INDIVIDUAL_TRAIN = '🧑🏻‍🦯индивидуальная🧑🏻‍🦯'
GROUP_TRAIN = '🤼‍♂️групповая🤼‍♂'
MY_TRAIN = '🧔🏻моя тренировка🧔🏻'
RENT = '👥аренда👥'
GROUP_LEVEL_DICT = {TrainingGroup.LEVEL_ORANGE: '🟠оранжевый мяч🟠', TrainingGroup.LEVEL_GREEN: '🟢зелёный мяч🟢'}

PLAYERS_FROM_GROUP = 'Игроки группы'
HAVE_COME_FROM_OTHERS = '➕Пришли из других'
HAVE_COME_FOR_MONEY = '💲Пришли за ₽'
HAVE_COME_FOR_PAY_BONUS_LESSON = '💲Пришли за ₽ отыгрыши'
ARE_ABSENT = '➖Отсутствуют'

CHOOSE_YEAR = 'Выбери год'
CHOOSE_MONTH = 'Выбери месяц'
CHOOSE_GROUP = 'Выбери группу'

TOTAL_PAID = 'Итого заплатили'
MUST_PAY = 'Должны заплатить'

HAVE_NOT_PAID = 'Не заплатили'

NUMBER_OF_TRAINS = 'Кол-во занятий'
TARIF = 'Тариф'

MUST_PAY_FOR_TRAINS_AND_BALLS = 'Должны <b>{}</b>₽ + {}₽ за мячи'
FIRST_LAST_NAME_FACT_NUMBER_OF_VISITS = 'Имя Фамилия -- факт₽, кол-во посещений'
FIRST_LAST_NAME_NUMBER_OF_VISITS_GROUP = 'Имя Фамилия -- кол-во посещений (банда)'
NO_SUCH = '<b>НЕТ ТАКИХ</b>'

TO_INSERT_PAYMENT_DATA_HELP_INFO = 'Для того, чтобы внести данные об оплате, введи данные в формате \n\n' \
                                   'id сумма_в_рублях через пробел, например, 18 3600\n\n'

YEAR = 'Год'
MONTH = 'Месяц'

ERROR_INCORRECT_ID_OR_MONEY = 'Ошибка, скорее всего неправильно ввел id или сумму -- не ввел через пробел или есть лишние символы\n/cancel'
NO_SUCH_OBJECT_IN_DATABASE = 'Нет такого объекта в базе данных -- неправильный id\n/cancel'

UP_TO_YOU = 'Ну как хочешь'
CHANGES_ARE_MADE = 'Изменения внесены'

THIS_WAY_YEAH = 'Вот так вот значит, да?'

TO_ALL_GROUPS = 'Всем группам'
TO_ALL = 'Вообще всем'
TO_FREE_SCHEDULE = 'Свободный график'
CONFIRM = 'Подтвердить'
YES = 'Да'
NO = 'Нет'
CANCEL = 'Отмена'
CHANGE_DATA = 'Изменить данные'
SET_UP_DATA = 'Настроить данные'
YEAR_2020 = '2020'
YEAR_2021 = '2021'
TO_GROUPS = 'К группам'
SAVE_ONE_TRAIN = 'Одну'
SAVE_FOR_TWO_MONTHS = 'На 2 месяца'
SITE = 'Сайт'
ADMIN_SITE = 'Перейти на сайт'
ADMIN_PAYMENT = 'Оплата'

NEW_CLIENT_HAS_COME = 'Пришел новый клиент:\n<b>{}</b>'
