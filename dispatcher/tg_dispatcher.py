from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import TgHandlers
from states import Auth


class TgDispatcher(Dispatcher):
    def __init__(self, bot: Bot, handlers: TgHandlers):
        self.handlers = handlers
        super().__init__(bot, storage=MemoryStorage())

    def registerHandlers(self):
        self.register_message_handler(
            self.handlers.start,
            commands='start')

        self.register_message_handler(
            self.handlers.phone,
            state=Auth.phone, content_types=['contact'])

        self.register_message_handler(
            self.handlers.contact,
            state=Auth.contact)

        self.register_callback_query_handler(
            self.handlers.yes, lambda c: c.data == 'yes', state=Auth.confirmation)

        self.register_callback_query_handler(
            self.handlers.no, lambda c: c.data == 'no', state=Auth.confirmation)

        self.register_callback_query_handler(
            self.handlers.cancel_registration, lambda c: c.data == 'cancel', state='*')
