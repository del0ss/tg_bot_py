from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class TgKeyboards:
    @staticmethod
    def _kb_wrapper(func):
        def wrapped():
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            return keyboard.add(*func())
        return wrapped

    @staticmethod
    @_kb_wrapper
    def confirm():
        return ['Да', 'Нет']

    @staticmethod
    @_kb_wrapper
    def registration():
        return ['Зарегистрироваться']

    @staticmethod
    @_kb_wrapper
    def cancel_registration():
        return ['Отменить регистрацию']

    @staticmethod
    @_kb_wrapper
    def cancel():
        return ['Отмена']

    @staticmethod
    def contact():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            KeyboardButton(
                text='Дать доступ к номеру телефона',
                request_contact=True
            )
        )
        return markup


    @staticmethod
    @_kb_wrapper
    def after_registration():
        return ['Записаться к врачу', 'Посмотреть свои данные', 'Написать жалобу', 'Посмотреть рекомендацию от врача']


if __name__ == '__main__':
    kb = TgKeyboards.confirm()
    print(kb)
