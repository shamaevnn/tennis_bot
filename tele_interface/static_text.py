from_eng_to_rus_day_week = {
    'Sunday': 'воскресенье', 'Monday': 'понедельник', 'Tuesday': 'вторник', 'Wednesday': 'среда',
    'Thursday': 'четверг', 'Friday': 'пятница', 'Saturday': 'суббота'
}
from_digit_to_month = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
        7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь',
    }

BACK_BUTTON = '⬅️ назад'
ALERT_TEXTS = [{"Знаю, что лень идти, а надо. Сегодня тренировка:": "https://perfum-online.by/image/data/1news/that-to-do-%D1%87%D1%82%D0%BE%D0%B1-not-to-miss-drills.jpg"},
               {"А кто это у нас уже забыл о тренировке, а? Напоминаю:\n": "https://i.pinimg.com/originals/9f/ce/af/9fceaf6c5518ec0526d0d2d86d8cfb01.jpg"},
               {"Терпение и труд всё перетрут, не забудь о тренировке:\n": "https://ggym.ru/files/170215/art-lebedev.jpg"},
               {"Ой, а кто это уже забыл о тренировке? Напоминаю:\n": "https://i.pinimg.com/474x/80/0e/f0/800ef02d7823ffbb097449feb5825d44.jpg"},
               {"Твой контракт с Lacoste уже близок, главное — не пропустить сегодняшнюю тренировку:\n": "https://s-cdn.sportbox.ru/images/styles/690_388/fp_fotos/b9/05/2cfa2db501437ee9f77b96efa14d6c4e5fa6b7e2ce5c6291318978.jpg"},
               {"Неужели вы похожи с этим человеком? Надеюсь, что нет. Сегодня тренировка:\n": "https://i.pinimg.com/736x/a3/48/34/a34834232790bc0528f460d977e2a296.jpg"},
               {"Какой прекрасный котик:) Не стань таким же, сегодня тренировка:\n": "https://newsomsk.ru/images/uploading/2a6ca712467a5fa4fd45031f85ab87b6.jpg"},
               {"А ты можешь делать все, ведь у тебя есть ракетка! Сегодня тренировка:\n": "https://memepedia.ru/wp-content/uploads/2017/09/%D0%BD%D0%B5-%D0%BC%D0%BE%D0%B3%D1%83-%D0%BD%D0%B8%D1%87%D0%B5%D0%B3%D0%BE-%D0%B4%D0%B5%D0%BB%D0%B0%D1%82%D1%8C-%D1%83-%D0%BC%D0%B5%D0%BD%D1%8F-%D0%BB%D0%B0%D0%BF%D0%BA%D0%B8.jpg"},
               {"Действительно, как это? Не забудь:\n": "https://sun9-47.userapi.com/jnrLYf7VsyWwM8NtbsriLmse5pFI22i_m6Tdlg/j37vKNL6OCs.jpg"},
               {"Сегодня проходим новый удар, приходи.\n": "https://bookmaker-ratings.ru/wp-content/uploads/2016/06/Dzhok.jpg"},
               {"Постепенно превратишься в эту обезьянку, если не будешь ходить. Напоминаю:\n": "https://i.pinimg.com/originals/1f/2c/fa/1f2cfa82c65df4138a4cf781b8f966e0.jpg"},
               {"Еда для тех, кто пропускает тренировки. Не забудь сегодня:\n": "https://doseng.org/uploads/posts/2011-01/1295577046_podborka_83.jpg"},
               {"Сегодня даже кошка тренируется, так что приходи.\n": "http://tennispeople.ru/wp-content/uploads/2019/06/16-iyulya-741x1024.jpeg"},
               {"Сегодня повторяем эту цитату, не забудь.\n": "https://shutniki.club/wp-content/uploads/2020/02/Prikoly_pro_tennis_15_02142004.jpg"},
               {"Узнаешь? Ну ничего, труд из обезьяны сделал теннисиста.\n": "https://s3-eu-west-1.amazonaws.com/uploads.playbaamboozle.com/uploads/images/23164/1589396590_146414"},
               {"Желаю тебе, чтобы ничего сегодня не защемило, приходи.\n": "https://demotivatorium.ru/sstorage/3/2013/08/12210417129067/demotivatorium_ru_to_samoe_chuvstvo_kogda_27757.jpg"},
               {"Говорят, что это фото было сделано на том самом корте на Косой Горе. Приходи сегодня!\n": "https://pbs.twimg.com/media/D9sbAfaWsAE_55P.jpg"},
               {"Приходи сегодня! Специально для тебя Владлен сделает также.\n": "https://i.dailymail.co.uk/i/pix/2012/10/10/article-2215659-156FF0C5000005DC-190_964x500.jpg"},
               {"Сегодня Владлен добавляет 5 отыгрышей тем, кто отобьёт также, так что приходи.\n": "http://fototelegraf.ru/wp-content/uploads/2010/12/luchshye-sportivnye-foto-21-25.jpg"},
               {"Никто не может выиграть у Владлена один раз подряд. Приходи сегодня, попробуй!\n": "https://cdn.fishki.net/upload/post/2016/09/21/2080507/1-f-50224.jpg"},
               {"Если придешь сегодня, то @ta2asho подберёт тебе кроссовки от легендарного теннисиста Stan Smith.\n": "https://golf.com/wp-content/uploads/2019/04/114_May_Travel_GolfTown-1-1.jpg"},
               {"Не обижай мячик сегодня.\n": "https://i.pinimg.com/736x/53/88/20/53882082be0a29f30748db86f53b9398.jpg"},
               {"Сегодня по расписанию у нас средний теннис.\n": "https://shutniki.club/wp-content/uploads/2020/02/Prikoly_pro_tennis_8_02142000.jpg"},
               {"Сегодня Владен не откажет, если ты попросишь повторить его это.\n": "https://kaifolog.ru/uploads/posts/2012-04/1335357965_003.jpg"},
               {"Сегодня на разминке делаем следующее упражнение.\n": "https://www.si.com/.image/t_share/MTY4MjU5MjE5MjI3OTQ0ODMz/andy-murray-blogjpg.jpg"},
               {"Захвати сегодня на тренировку арбузика:)\n": "https://i02.fotocdn.net/s107/051ba57737d5ed57/public_pin_l/2357071112.jpg"},
               {"Сегодня на тренировке без сломанных ракеток, пожалуйста.\n": "https://www.tennismagazin.de/content/uploads/2016/02/gettyimages-112177891.jpg"},
               {"Сегодня на тренировке вся группа становится в ряд и делает дзынь-дзынь.\n": "https://joker.ykt.ru/uploads/posts/1329914517_1367_21.02.2012.jpeg"},
               {"Поработаем сегодня над растяжкой, приходи!\n": "https://tunnel.ru/media/images/2016-09/post_comment/739962/at736833740.jpg"},
               {"Иногда на улице холодно. Как же хорошо, что на корте тепло, приходи сегодня!\n": "http://img0.safereactor.cc/pics/post/full/%D0%B4%D0%B5%D0%B2%D1%83%D1%88%D0%BA%D0%B0-%D0%B2%D0%BE%D0%BB%D0%BE%D1%81%D0%B0%D1%82%D0%B0%D1%8F-%D1%82%D0%B5%D0%BD%D0%BD%D0%B8%D1%81-%D0%BF%D0%B5%D1%81%D0%BE%D1%87%D0%BD%D0%B8%D1%86%D0%B0-750982.jpeg"},
               {"Ноготочки все покрасили? Сегодня проверяем. Кто не покрасил, у того -1 отыгрыш.\n": "http://i1.tiesraides.lv/0x0/galleries/valdis_berzins/4c8b0faa90af5/2010-09-11_11.jpg"},
               {"Сегодня будет больше мужского или женского тенниса?\n": "https://mtdata.ru/u28/photo80D4/20019914451-0/original.jpg"},
               {"Согласен. Напоминаю:\n": "https://301-1.ru/uploads/image/rostov-smog-smozhesh-i-ty_Ti0bxWmuMD.jpg"},
               {"Но а пока мы все ещё котики. Напоминаю:\n": "https://klike.net/uploads/posts/2019-09/1567333956_2.jpg"},
               {"Сегодня Владлен принесет свой ковёр, нужно помочь.\n": "https://www.anekdotovmir.ru/wp-content/uploads/2017/05/%D0%B0%D0%BD%D0%B5%D0%BA%D0%B4%D0%BE%D1%82-%D0%BF%D1%80%D0%BE-%D1%82%D0%B5%D0%BD%D0%BD%D0%B8%D1%81.jpg"},
               {"Сегодня тренируем телепатию.\n": "https://qph.fs.quoracdn.net/main-qimg-d58bd9d0e09aadddf367cd84b1b8c01b.webp"},
               {"Сегодня фотографируем твоё лицо во время удара.\n": "https://i.pinimg.com/236x/e8/c6/96/e8c6967e78de73e2ede88d6552f32baf--tennis-funny-tennis-memes.jpg"},]

TAKE_LESSON_BUTTON = 'Записаться на занятие'
MY_DATA_BUTTON = 'Мои данные'
SKIP_LESSON_BUTTON = 'Пропустить занятие'
HELP_BUTTON = '🤓Поддержка'

NO_PAYMENT_BUTTON = '❌НЕ ОПЛАЧЕНО❌'
SUCCESS_PAYMENT = '✅ОПЛАЧЕНО✅'

NOW_YOU_HAVE_ACCESS_CONGRATS = 'Теперь тебе доступен мой функционал, поздравляю!'

GREEN_BALL = '🍏зелёный мяч🍏'
ORANGE_BALL = '🧡оранжевый мяч🧡'

ERROR_LIMIT_MAX_PLAYERS = 'Количество игроков в группе должно быть не больше {max_players}, вы указали {count}.'
ERROR_MAX_PLAYERS_IN_FUTURE = 'Со следующими днями может возникнуть проблема, что будет больше людей, чем нужно на тренирвоке'

CANCEL_TRAIN_PLUS_BONUS_LESSON = '😱ATTENTION😱\n' \
                       'У тебя есть запись на тренировку на <b> {}.</b>\n' \
                       '<b>Тренер ее отменил.</b> Но не отчаивайся, я добавлю тебе отыгрыш 🎾'

CANCEL_TRAIN_PLUS_BONUS_LESSON_2 = 'Тренировка <b>{} в {}</b> доступна, ура!'
TRAIN_IS_AVAIABLE_CONGRATS = 'Тренировка <b>{} в {}</b> доступна, ура!'

ERROR_CANT_ADD_NEW_TRAIN = 'Нельзя добавить тренировку на это время в этот день, т.к. уже есть запись на {} с продолжительностью {}.'

FIRST_TIME_GREETING = 'Привет! Я бот самого продвинутого тренера в Туле (России). ' \
                      'Для дальнейшей работы нужно указать свои контактные данные.'

FIRST_TIME_INSERT_FIRST_LAST_MAME = 'Введи фамилию и имя через пробел в формате "Фамилия Имя", например: Иванов Иван.'
FIRST_TIME_INSERT_PHONE_NUMBER = 'Введи номер телефона в формате "89991112233" (11 цифр подряд).'
WRONG_PHONE_NUMBER_FORMAT = 'Неправильный формат данных, было введено {} цифр.\nВведи номер ещё раз.'
I_WILL_TEXT_AS_SOON_AS_COACH_CONFIRM = 'Как только тренер подтвердит твою кандидатуру, я напишу.'

HELP_MESSAGE = 'По всем вопросам пиши @ta2asho.\nЖелательно описывать свою проблему со скриншотами.'
COACH_HAVE_NOT_CONFIRMED_YET = 'Тренер еще не одобрил.'
