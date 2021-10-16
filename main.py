import logging
from emoji import emojize
from aiogram import Bot, Dispatcher, executor, types

from config import ConfigTelebot
from Database.posgre_sql import StepTable, QuestionsTable, DialogsTable, EmojiTable
from command_handler import CommandHandler

bot = Bot(token=ConfigTelebot().api_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

class MyBot():
    def __init__(self):
        self.steps = StepTable()
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()

    @dp.message_handler(commands='status')
    async def status_message(message: types.Message):
        await message.answer('Bot is working' + emojize(":pizza:"))

    @dp.message_handler(commands='start')
    async def start_dialog(message: types.Message):
        CommandHandler('20000, 30000, 60000', message.chat.id)           #20000 is cod to delete command
        # CommandHandler('30000,', message.chat.id)           #30000 is cod to insert new row in step_table SQL

        data = SelectorDataDb(message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        for dialog in data.dialogs:
            if data.emoji:
                keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(data.emoji)),
                                                        callback_data=dialog[1]))
            else:
                keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))
        await message.answer(data.quest, reply_markup=keyboard)

    @dp.callback_query_handler(text='back')
    async def back_command(call: types.CallbackQuery):
        CommandHandler('50000,', call.message.chat.id)
        data = SelectorDataDb(call.message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        for dialog in data.dialogs:
            if data.emoji:
                keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(data.emoji)),
                                                        callback_data=dialog[1]))
            else:
                keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))
        if not data.style_id == 0:
            keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))

        await call.message.answer(data.quest, reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    @dp.callback_query_handler()
    async def enter_button_command(call: types.CallbackQuery):
        pre_data = SelectorDataDb(call.message.chat.id)
        pre_answer = pre_data.select_pre_step_dialog(pre_data.step_id, pre_data.style_id,
                                                     call.data
                                                     )
        CommandHandler(call.data, call.message.chat.id)
        data = SelectorDataDb(call.message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        for dialog in data.dialogs:
            if data.emoji:
                keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(data.emoji)),
                                                        callback_data=dialog[1]))
            else:
                keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))

        await call.message.answer(data.quest, reply_markup=keyboard)
        await bot.edit_message_text(f'{pre_data.quest}\n<u>{pre_answer}</u>', call.message.chat.id,
                                    call.message.message_id, reply_markup='')


class SelectorDataDb():
    def __init__(self, user_id):
        self.user_id = user_id
        self.steps = StepTable()
        self.questions = QuestionsTable()
        self.dia = DialogsTable()
        self.emj = EmojiTable()

        self.step_id = self.select_step_number_from_db(self.user_id)
        self.style_id = self.select_style_id_from_db(self.user_id)
        self.quest = self.select_question_from_db(self.step_id, self.style_id)
        self.dialogs = self.select_dialog_from_db(self.step_id, self.style_id)
        self.emoji = self.select_emoji_for_dialog(self.step_id, self.style_id)

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
        conditions = f"{self.dia.split_fields[0]}={step_number} "\
                     f"AND {self.dia.split_fields[1]}={style_id} "\
                     f"AND {self.dia.split_fields[3]}='{command}'"
        data = self.dia.select_in_table(self.dia.table_name,
                                        f'{self.dia.split_fields[2]}',
                                        conditions)
        return data[0][0]

    def select_emoji_for_dialog(self, step_number, style_id):
        conditions = f"{self.emj.split_fields[0]}={step_number}" \
                     f"AND {self.emj.split_fields[1]}={style_id}"
        data = self.emj.select_in_table(self.emj.table_name,
                                        f'{self.emj.split_fields[2]}',
                                        conditions)
        print(data)
        if data:
            return data[0][0]
        else:
            return None

if __name__ == '__main__':
    cl = MyBot()
    executor.start_polling(dp, skip_updates=True)
