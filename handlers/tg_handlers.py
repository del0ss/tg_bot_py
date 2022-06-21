import os
import re
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from keyboards import TgKeyboards, TgInlineKeyboards
from states import Auth


class TgHandlers:
    TIME_SPAM = 5

    def __init__(self, repository, bot):
        self.repository = repository
        self.bot = bot

    async def start(self, msg: types.Message):
        if self.repository.getUser(msg.from_user.id):
            await self.bot.send_message(
                msg.from_user.id,
                'Добро пожаловать',
                reply_markup=TgKeyboards.after_registration())
        elif not (self.repository.getUser(msg.from_user.id)) \
                and not (self.repository.getSpamList(msg.from_user.id)):
            await self.bot.send_message(
                msg.from_user.id,
                'Здравствуйте, чтобы пользоваться ботом, надо зарегистрироваться. \n Дайте доступ к вашему телефону:',
                reply_markup=TgKeyboards.contact())
            await Auth.first()
        else:
            data = self.repository.getSpamList(msg.from_user.id)
            if (datetime.now().minute - (datetime.strptime(data[0], '%H:%M:%S.%f')).minute) < self.TIME_SPAM:
                await self.bot.send_message(msg.from_user.id, 'Время ещё не прошло! Подождите 5 минут!')

            else:
                self.repository.deleteUserFromSpamList(msg.from_user.id)
                await self.bot.send_message(
                    msg.from_user.id,
                    'Здравствуйте, чтобы пользоваться ботом, надо зарегистрироваться. \n Дайте доступ к вашему телефону:',
                    reply_markup=TgKeyboards.contact())
                await Auth.first()

    async def cancel_registration(self, callback_query: types.CallbackQuery, state: FSMContext):
        if await state.get_state() is None:
            return
        await state.finish()
        await callback_query.message.edit_text('Вы отменили регистрацию')

    async def phone(self, msg: types.Message):
        await Auth.next()
        await self.bot.send_message(msg.from_user.id,
                                    f'Зарегиcтрировать вас под этим номером? {msg.contact.phone_number}',
                                    reply_markup=TgInlineKeyboards.confirmKbi())

    async def yes(self, callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.edit_text('Вы зарегистрированы!')
        await state.finish()

    async def no(self, callback_query: types.CallbackQuery):
        await callback_query.message.edit_text('Напишите ваш номер телефона')
        await Auth.next()

    async def contact(self, msg: types.Message):
        if re.match(r'^(\+7)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', msg.text):
            await self.bot.send_message(msg.from_user.id,
                                        f'Зарегиcтрировать вас под этим номером? {msg.text}',
                                        reply_markup=TgInlineKeyboards.confirmKbi())
            await Auth.confirmation.set()
        else:
            await self.bot.send_message(msg.from_user.id, 'Не верный формат телефона! +7999')
            await Auth.contact.set()