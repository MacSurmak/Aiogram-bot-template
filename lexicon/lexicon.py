LEXICON: dict[str, dict[str, str]] = {
    'ru': {
        # Commands messages
        '/start': 'Привет! Это тестовая версия Стиралка-бота! '
                  'Чтобы посмотреть список доступных '
                  'команд - набери /help',
        '/start-admin': 'Получена команда /start от админа',
        '/start-registered': 'Снова привет! Это тестовая версия Стиралка-бота! '
                  'Чтобы посмотреть список доступных '
                  'команд - набери /help',
        '/help': 'Здесь будет текст команды /help',
        '/admin': 'Активировал меню администратора!',

        # Admin messages
        'user-back': 'Активировал меню пользователя!',
        'enter-room': 'Введи номер комнаты владельца ключа:',
        'room-not-digit': 'Я жду цифры, повтори ввод:',
        'wrong-number': 'Эта комната не принадлежит геофаку, повтори ввод',
        'enter-surname': 'Отлично, теперь введи фамилию владельца ключа:',
        'enter-name': 'Введи имя владельца ключа:',

        # Admin markups
        '_keygen': 'Сгенерировать ключ',
        '_exit': 'Выход',
        '_cancel': 'Отмена',

        # User messages
        'reply-other': 'Я тебя не понимаю',

        # User markups
    },
    'en': {
        """
        Переводы на английский напишу позже
        """
    }
}


LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Старт',
    '/help': 'Справка по работе бота'
}


def lexicon(lang: str, key: str) -> str:
    if lang in ['ru', 'en']:
        return LEXICON['ru'][key]
    else:
        return LEXICON['ru'][key]
