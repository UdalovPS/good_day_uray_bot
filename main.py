import logging
from emoji import emojize
from aiogram import Bot, Dispatcher, executor, types

from config import ConfigTelebot
from Database.posgre_sql import StepTable, QuestionsTable, DialogsTable
from Database.posgre_sql import Customer, EmojiTable, Product, CartProduct
from Database.posgre_sql import Cart
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
        CommandHandler('20000, 30000', message.chat.id)
        data = SelectorDataDb(message.chat.id)
        if data.black_list_data:
            if data.black_list_data == 2:
                await message.answer("Извините, но вы находитесь в черном списке.\nЗа подробностями обратитесь по телефону")
                return 0
        else:
            CommandHandler('80000,', message.chat.id)
        CommandHandler('60000,', message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        for dialog in data.dialogs:
            if data.emoji:
                keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(data.emoji)),
                                                        callback_data=dialog[1]))
            else:
                keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))
        await message.answer(data.quest, reply_markup=keyboard)

    @dp.message_handler(content_types='text')
    async def count_product_message(message: types.Message):
        data = SelectorDataDb(message.chat.id)
        if data.step_id == 4:
            try:
                count = int(message.text)
                if count > 999:
                    await message.answer('Слишком большое число')
                else:
                    command = 72000 + count
                    CommandHandler(f'40005, {str(command)}')
            except ValueError:
                await message.answer('Неверно введено число')

    @dp.callback_query_handler(text='back')
    async def back_command(call: types.CallbackQuery):
        CommandHandler('50000,', call.message.chat.id)
        data = SelectorDataDb(call.message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        for dialog in data.dialogs:
            if dialog[2]:                                                                           #if emoji is exists
                keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(dialog[2])),
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
        if data.dialogs:
            for dialog in data.dialogs:
                if dialog[2]:                                                                           #if emoji is exists
                    keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(dialog[2])),
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
        self.customer = Customer()
        self.prod = Product()
        self.cart_prod = CartProduct()
        self.cart = Cart()

        self.step_id = self.select_step_number_from_db(self.user_id)
        self.style_id = self.select_style_id_from_db(self.user_id)
        self.quest = self.select_question_from_db(self.step_id, self.style_id)
        self.dialogs = self.select_dialog_from_db(self.step_id, self.style_id)
        self.emoji = self.select_emoji_for_dialog(self.step_id, self.style_id)
        self.black_list_data = self.check_black_list_about_customer(self.user_id)

    def select_step_number_from_db(self, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        step_number = self.steps.select_in_table(self.steps.table_name,
                                                 self.steps.split_fields[1],
                                                 conditions
                                                 )
        if step_number:
            return step_number[0][0]
        else:
            return None

    def select_style_id_from_db(self, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        style_id = self.steps.select_in_table(self.steps.table_name,
                                              self.steps.split_fields[2],
                                              conditions)
        if style_id:
            return style_id[0][0]
        else:
            return None

    def select_question_from_db(self, step_number, style_id):
        conditions = f'{self.questions.split_fields[0]}={step_number}' \
                     f'AND {self.questions.split_fields[1]}={style_id}'
        data = self.questions.select_in_table(self.questions.table_name,
                                              self.questions.split_fields[2],
                                              conditions)
        if step_number == 2:
            sub_data = self.select_description_product(self.user_id)
            return data[0][0] + sub_data
        else:
            return data[0][0]

    def select_dialog_from_db(self, step_number, style_id):
        conditions = f'{self.dia.split_fields[0]}={step_number}' \
                     f'AND {self.dia.split_fields[1]}={style_id}'
        data = self.dia.select_in_table(self.dia.table_name,
                                        f'{self.dia.split_fields[2]}, '
                                        f'{self.dia.split_fields[3]},'
                                        f'{self.dia.split_fields[4]}',
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

    def check_black_list_about_customer(self, chat_id):
        conditions = f"{self.customer.split_fields[0]}={chat_id}"
        data = self.customer.select_in_table(self.customer.table_name,
                                             f'{self.customer.split_fields[3]}',
                                             conditions
                                             )
        if data:
            return data[0][0]
        else:
            return None

    def select_description_product(self, chat_id):
        product_id = self.select_product_id(chat_id)
        conditions = f'{self.prod.split_fields[0]}={product_id}'
        data = self.prod.select_in_table(self.prod.table_name,
                                         self.prod.split_fields[2],
                                         conditions)
        return data[0][0]

    def select_product_id(self, chat_id):
        cart_prod_id = self.select_last_cart_product_id(chat_id)
        conditions = f'{self.cart_prod.split_fields[0]}={cart_prod_id}'
        data = self.cart_prod.select_in_table(self.cart_prod.table_name,
                                              self.cart_prod.split_fields[2],
                                              conditions)
        return data[0][0]

    def select_last_cart_product_id(self, chat_id):
        cart_id = self.select_last_cart_id(chat_id)
        conditions = f'{self.cart_prod.split_fields[1]}={cart_id}'
        data = self.cart_prod.select_in_table(self.cart_prod.table_name,
                                              f'MAX({self.cart_prod.split_fields[0]})',
                                              conditions)
        return data[0][0]

    def select_last_cart_id(self, chat_id):
        conditions = f'{self.cart.split_fields[1]}={chat_id}'
        print('conditions last cart: ', conditions)
        data = self.cart.select_in_table(self.cart.table_name,
                                         f'MAX({self.cart.split_fields[0]})',
                                         conditions)
        print(data[0][0])
        return data[0][0]

if __name__ == '__main__':
    cl = MyBot()
    executor.start_polling(dp, skip_updates=True)
