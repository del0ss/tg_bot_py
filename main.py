from aiogram.utils import executor
from aiogram import Bot, types

from repositories import PgRepository
from dispatcher import TgDispatcher
from handlers import TgHandlers
from settings import SETTINGS


if __name__ == '__main__':
    repository = PgRepository(SETTINGS['POSTGRES_DB'], SETTINGS['POSTGRES_USER'], SETTINGS['POSTGRES_PASSWORD'],
                              SETTINGS['POSTGRES_HOST'], SETTINGS['POSTGRES_PORT'])

    bot = Bot(token=SETTINGS['TOKEN_BOT'], parse_mode=types.ParseMode.HTML)
    handlers = TgHandlers(repository, bot)

    dp = TgDispatcher(bot, handlers)
    dp.registerHandlers()

    executor.start_polling(dp, skip_updates=True)
