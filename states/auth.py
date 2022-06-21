from aiogram.dispatcher.filters.state import State, StatesGroup


class Auth(StatesGroup):
    phone = State()
    confirmation = State()
    contact = State()