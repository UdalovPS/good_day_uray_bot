import logging
from emoji import emojize
from aiogram import Bot, Dispatcher, executor, types

from config import ConfigTelebot
from test_file import *
from Builder.builder import AnswerFactory

bot = Bot(token=ConfigTelebot().api_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


class MyBot:
    @dp.message_handler(commands='test')
    async def test_message(message: types.Message) -> None:
        emojj = "\U0001F519"
        # ready_emj = emojize(emojj)
        builder = FormDataForMsg()
        data = builder.create_data_for_msg()
        keyboard = types.InlineKeyboardMarkup()
        for dialog in data.dialogs.dialogs:
            keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))
        await bot.send_message(chat_id=data.chat_id.text, text=data.quest.text+emojj, reply_markup=keyboard)
        await message.answer(message.text)

    @dp.message_handler(commands='start')
    async def start_message(message: types.Message) -> None:
        data = AnswerFactory().answer_to_start_command(message)
        keyboard = types.InlineKeyboardMarkup()
        KeyboardExtender(keyboard, data.dialogs_list.dialogs_list)
        await bot.send_message(chat_id=data.chat_id, text=data.question.quest, reply_markup=keyboard)

    @dp.callback_query_handler(text='back')
    async def back_command(call: types.CallbackQuery) -> None:
        data = AnswerFactory().answer_to_back_inline_commands(call)
        keyboard = types.InlineKeyboardMarkup()
        KeyboardExtender(keyboard, data.dialogs_list.dialogs_list)
        await bot.send_message(chat_id=data.chat_id, text=data.question.quest, reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    @dp.callback_query_handler()
    async def inline_button_commands(call: types.CallbackQuery) -> None:
        """answer to not concrete inline commands"""
        pre_question = AnswerFactory().pre_question_in_dialog(call)
        data = AnswerFactory().answer_to_inline_commands(call)
        btn_customer_answer = AnswerFactory().pre_inline_btn_customer_answer(call)
        keyboard = types.InlineKeyboardMarkup()
        KeyboardExtender(keyboard, data.dialogs_list.dialogs_list)
        await bot.send_message(chat_id=data.chat_id, text=data.question.quest, reply_markup=keyboard)
        await bot.edit_message_text(f"{pre_question.question.quest}\n<u>{btn_customer_answer.question.pre_answer}</u>",
                                    call.message.chat.id, call.message.message_id, reply_markup='')


class KeyboardExtender:
    def __init__(self, keyboard, dialog_obj_list: list) -> None:
        self.keyboard = keyboard
        self.dialog_obj_list = dialog_obj_list
        self.extend_keyboard()

    def extend_keyboard(self) -> None:
        if self.dialog_obj_list:
            for dialog in self.dialog_obj_list:
                if dialog.emoji:
                  self.keyboard.add(types.InlineKeyboardButton(text=dialog.dialog + '  ' + dialog.emoji,
                                                                 callback_data=dialog.commands))
                else:
                    self.keyboard.add(types.InlineKeyboardButton(text=dialog.dialog,
                                                                 callback_data=dialog.commands))

if __name__ == '__main__':
    cl = MyBot()
    executor.start_polling(dp, skip_updates=True)
