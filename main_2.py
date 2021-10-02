import logging
from aiogram import Bot, Dispatcher, executor, types

from config import ConfigTelebot
from Database.posgre_sql import StepTable, QuestionsTable, DialogsTable

class MyBot():
    def __init__(self):
        self.bot = Bot(token=ConfigTelebot().api_token)
        self.dp = Dispatcher(self.bot)
        logging.basicConfig(level=logging.INFO)

    def start_bot_message(self):
        @self.dp.message_handler(commands='start')
        async def start_message(message: types.Message):
            await message.answer('Bot is start')

    def start_dialog_with_user(self):
        @self.dp.message_handler(content_types=['text'])
        async def start_dialog_message(message: types.Message):
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Press me', callback_data="1"))
            await message.answer('You start dialog', reply_markup=keyboard)

    def btn_handler(self):
        @self.dp.callback_query_handler()
        async def enter_button_command(call: types.CallbackQuery):
            await call.message.answer(call.data)
            await self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             reply_markup=None, text="a12")

    def start_bot(self):
        executor.start_polling(self.dp, skip_updates=True)

if __name__ == '__main__':
    bot = MyBot()
    bot.start_bot_message()
    bot.start_dialog_with_user()
    bot.btn_handler()
    bot.start_bot()
