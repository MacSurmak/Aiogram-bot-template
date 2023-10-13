from dataclasses import dataclass
from environs import Env
from sqlalchemy.engine.url import URL


@dataclass
class DatabaseConfig:
    url: URL


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class RedisConfig:
    host: str
    port: int
    password: str


@dataclass
class ImapConfig:
    host: str
    user: str
    password: str


@dataclass
class Config:
    bot: TgBot
    db: DatabaseConfig
    redis: RedisConfig
    imap: ImapConfig


def load_config(path: str | None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(bot=TgBot(token=env('BOT_TOKEN'),
                            admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                  db=DatabaseConfig(url=URL.create(
                                        drivername='postgresql+asyncpg',
                                        host=env('DB_HOST'),
                                        port=env('DB_PORT'),
                                        username=env('DB_USER'),
                                        password=env('DB_PASSWORD'),
                                        database=env('DATABASE')
                                    )),
                  redis=RedisConfig(host=env('REDIS_HOST'),
                                    port=env('REDIS_PORT'),
                                    password=env('REDIS_PASSWORD')),
                  imap=ImapConfig(host=env('IMAP_HOST'),
                                  user=env('IMAP_USER'),
                                  password=env('IMAP_PASSWORD')))

