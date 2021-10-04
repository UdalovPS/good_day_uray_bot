import logging
from aiogram import Bot, Dispatcher, executor, types

from config import ConfigTelebot
from Database.posgre_sql import StepTable, QuestionsTable, DialogsTable
from command_handler import CommandHandler

class MyBot():
    def __init__(self):
        self.bot = Bot(token=ConfigTelebot().api_token, parse_mode=types.ParseMode.HTML)
        self.dp = Dispatcher(self.bot)
        logging.basicConfig(level=logging.INFO)

        self.steps = StepTable()
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()

    def status_bot_message(self):
        @self.dp.message_handler(commands='status')
        async def status_message(message: types.Message):
            await message.answer('Bot is working')

    def start_dialog_with_user(self):
        @self.dp.message_handler(commands='start')
        async def start_dialog(message: types.Message):
            CommandHandler('20000,', message.chat.id).command_parser()   #20000 is cod to delete command
            CommandHandler('30000,', message.chat.id).command_parser()
            data = SelectorDataDb(message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            for dialog in data.dialogs:
                keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))

            await message.answer(data.quest, reply_markup=keyboard)

    def btn_handler(self):
        @self.dp.callback_query_handler()
        async def enter_button_command(call: types.CallbackQuery):
            pre_data = SelectorDataDb(call.message.chat.id)
            pre_answer = pre_data.select_pre_step_dialog(pre_data.step_id,
                                                         pre_data.style_id,
                                                         call.data
                                                         )
            CommandHandler(call.data, call.message.chat.id).command_parser()
            data = SelectorDataDb(call.message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            for dialog in data.dialogs:
                keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))

            await call.message.answer(data.quest, reply_markup=keyboard)
            await self.bot.edit_message_text(f'{pre_data.quest}\n<u>{pre_answer}</u>', call.message.chat.id,
                                             call.message.message_id, reply_markup='')


    def start_bot(self):
        executor.start_polling(self.dp, skip_updates=True)


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


class SelectorDataDb():
    def __init__(self, user_id):
        self.user_id = user_id
        self.steps = StepTable()
        self.questions = QuestionsTable()
        self.dia = DialogsTable()

        self.step_id = self.select_step_number_from_db(self.user_id)
        self.style_id = self.select_style_id_from_db(self.user_id)
        self.quest = self.select_question_from_db(self.step_id, self.style_id)
        self.dialogs = self.select_dialog_from_db(self.step_id, self.style_id)

    def select_step_number_from_db(self, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        step_number = self.steps.select_in_table(self.steps.table_name,
                                                 self.steps.split_fields[1],
                                                 conditions
                                                 )
        return step_number[0][0]

    def select_style_id_from_db(self, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        style_id = self.steps.select_in_table(self.steps.table_name,
                                              self.steps.split_fields[2],
                                              conditions)
        return style_id[0][0]

    def select_question_from_db(self, step_number, style_id):
        conditions = f'{self.questions.split_fields[0]}={step_number}' \
                     f'AND {self.questions.split_fields[1]}={style_id}'
        data = self.questions.select_in_table(self.questions.table_name,
                                              self.questions.split_fields[2],
                                              conditions)
        print('question', data[0][0])
        return data[0][0]

    def select_dialog_from_db(self, step_number, style_id):
        conditions = f'{self.dia.split_fields[0]}={step_number}' \
                     f'AND {self.dia.split_fields[1]}={style_id}'
        data = self.dia.select_in_table(self.dia.table_name,
                                        f'{self.dia.split_fields[2]}, '
                                        f'{self.dia.split_fields[3]}',
                                        conditions)
        return data

    def select_pre_step_dialog(self, step_number, style_id, command):
        print(self.dia.split_fields[0], self.dia.split_fields[1], self.dia.split_fields[3])
        conditions = f"{self.dia.split_fields[0]}={step_number} "\
                     f"AND {self.dia.split_fields[1]}={style_id} "\
                     f"AND {self.dia.split_fields[3]}='{command}'"
        data = self.dia.select_in_table(self.dia.table_name,
                                        f'{self.dia.split_fields[2]}',
                                        conditions)
        print('answer', data[0][0])
        return data[0][0]

if __name__ == '__main__':
    bot = MyBot()
    bot.status_bot_message()
    bot.start_dialog_with_user()
    bot.btn_handler()
    bot.start_bot()
