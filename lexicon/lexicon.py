LEXICON: dict[str, dict[str, str]] = {
    'ru': {
        '/start': 'Привет! Это тестовая версия Стиралка-бота! '
                  'Чтобы посмотреть список доступных '
                  'команд - набери /help',
        '/start-admin': 'Получена команда /start от админа',
        '/start-registered': 'Снова привет!',
        '/help': 'Здесь будет текст команды /help',
        'reply': 'Я тебя не понимаю'
    },
    'en': {
        '/start': "Hello! It's a test version of a Stiralka-bot!"
                  "To see the list of available commands - "
                  "type /help",
        '/start-admin': 'Admin /start command is handled',
        '/start-registered': 'Hello, nice to see you again ;)',
        '/help': 'There will be a text for /help command',
        'reply': "I don't understand you :("
    }
}


LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Старт',
    '/help': 'Справка по работе бота'
}


def lexicon(lang: str, key: str) -> str:
    if lang in ['ru', 'en']:
        return LEXICON[lang][key]
    else:
        return LEXICON['en'][key]
