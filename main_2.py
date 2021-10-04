import logging
from aiogram import Bot, Dispatcher, executor, types

from config import ConfigTelebot
from Database.posgre_sql import StepTable, QuestionsTable, DialogsTable

class MyBot():
    def __init__(self):
        self.bot = Bot(token=ConfigTelebot().api_token)
        self.dp = Dispatcher(self.bot)
        logging.basicConfig(level=logging.INFO)

        self.steps = StepTable()
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()

    def start_bot_message(self):
        @self.dp.message_handler(commands='start')
        async def start_message(message: types.Message):
            await message.answer('Bot is start')

    def start_dialog_with_user(self):
        @self.dp.message_handler(content_types=['text'])
        async def start_dialog_message(message: types.Message):
            keyboard = types.InlineKeyboardMarkup()

            step_number = self.select_step_number_from_db(message.chat.id)
            style_id = self.select_style_id_from_db(message.chat.id)
            question = self.select_question_from_db(step_number, style_id)
            dialogs = self.select_dialog_from_db(step_number, style_id)

            for dialog in dialogs:
                keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=f'{dialog[1]}, {dialog[2]}'))

            await message.answer(question, reply_markup=keyboard)

    def btn_handler(self):
        @self.dp.callback_query_handler()
        async def enter_button_command(call: types.CallbackQuery):
            common_call_data = call.data.split(', ')
            next_step = int(common_call_data[0])
            next_style = int(common_call_data[1])
            if next_step == 1:
                self.update_style_id(next_style, call.message.chat.id)

            self.update_step_number(next_step, call.message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            step_number = self.select_step_number_from_db(call.message.chat.id)
            style_id = self.select_style_id_from_db(call.message.chat.id)
            question = self.select_question_from_db(step_number, style_id)
            dialogs = self.select_dialog_from_db(step_number, style_id)

            for dialog in dialogs:
                keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))
            await call.message.answer(question, reply_markup=keyboard)

            await self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             reply_markup=None)

    def start_bot(self):
        executor.start_polling(self.dp, skip_updates=True)


    def select_step_number_from_db(self, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        step_number = self.steps.select_in_table(self.steps.table_name,
                                                 self.steps.split_fields[1],
                                                 conditions)
        if not step_number:
            step_number = 0
            self.steps.insert_data_in_table(self.steps.table_name,
                                            self.steps.fields,
                                            f'({chat_id}, 0, 0)')
        return step_number[0][0]

    def select_style_id_from_db(self, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        style_id = self.steps.select_in_table(self.steps.table_name,
                                              self.steps.split_fields[2],
                                              conditions)
        if not style_id: style_id = 0
        return style_id[0][0]

    def select_question_from_db(self, step_number, style_id):
        conditions = f'{self.questions.split_fields[0]}={step_number}' \
                     f'AND {self.questions.split_fields[1]}={style_id}'
        data = self.questions.select_in_table(self.questions.table_name,
                                              self.questions.split_fields[2],
                                              conditions)
        return data[0][0]

    def select_dialog_from_db(self, step_number, style_id):
        conditions = f'{self.dialogs.split_fields[0]}={step_number}' \
                     f'AND {self.dialogs.split_fields[1]}={style_id}'
        data = self.dialogs.select_in_table(self.dialogs.table_name,
                                            f'{self.dialogs.split_fields[2]}, '
                                            f'{self.dialogs.split_fields[3]}, '
                                            f'{self.dialogs.split_fields[4]}',
                                            conditions)
        return data

    def update_step_number(self, next_step, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name,
                                 f'{self.steps.split_fields[1]}={next_step}',
                                 conditions)

    def update_style_id(self, next_style, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name,
                                 f'{self.steps.split_fields[2]}={next_style}',
                                 conditions)

if __name__ == '__main__':
    bot = MyBot()
    bot.start_bot_message()
    bot.start_dialog_with_user()
    bot.btn_handler()
    bot.start_bot()
