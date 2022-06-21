from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class TgInlineKeyboards:
    @staticmethod
    def _kbi_wrapper(func):
        def wrapped():
            keyboard = InlineKeyboardMarkup(row_width=2)
            return keyboard.add(*func())

        return wrapped()

    @_kbi_wrapper
    @staticmethod
    def patientStartKbi():
        return [InlineKeyboardButton(text='Следущая страница', callback_data='qwerty'),
                InlineKeyboardButton(text='Предыдущая страница', callback_data='zxc'),
                InlineKeyboardButton(text='Отмена', callback_data='cancel')]

    @_kbi_wrapper
    @staticmethod
    def confirmKbi():
        return [InlineKeyboardButton(text='Да', callback_data='yes'),
                InlineKeyboardButton(text='Нет', callback_data='no'),
                InlineKeyboardButton(text='Отмена', callback_data='cancel')]
