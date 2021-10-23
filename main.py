import logging
from emoji import emojize
from aiogram import Bot, Dispatcher, executor, types

from config import ConfigTelebot
from command_handler import CommandHandler
from Database.data_selector import SelectorDataDb

bot = Bot(token=ConfigTelebot().api_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

class MyBot():
    @dp.callback_query_handler(text='end')
    async def end_cart_with_user(call: types.CallbackQuery):
        CommandHandler('90001, 91000', call.message.chat.id)
        data = SelectorDataDb(call.message.chat.id)
        money_sum = 0
        cart_id = data.quest[0][0]
        mode = data.quest[0][1]
        if mode == 1: mode = 'Самовывоз'
        else: mode = 'Доставка'
        name = data.quest[0][2]
        phone = data.quest[0][3]
        address = data.quest[0][4]
        if not address: address = '-'
        customer_time = data.quest[0][5]
        if not customer_time: customer_time = '-'
        status = data.quest[0][6]
        if status == 0:
            status = 'Оформляется'
        elif status == 1:
            status = 'Оформлен'
        products = data.quest[1]
        await call.message.answer(f'Номер Заказа: {cart_id}\n{mode}\n'
                             f'Имя заказчика: {name}\nНомер телефона: {phone}\n'
                             f'Адрес доставки: {address}\nВремя: {customer_time}\n'
                             f'Статус заказа: {status}')
        # await call.message.answer(chat_id='-1001558221765', text=f'Номер Заказа: {cart_id}\n{mode}\n'
        #                      f'Имя заказчика: {name}\nНомер телефона: {phone}\n'
        #                      f'Адрес доставки: {address}\nВремя: {customer_time}\n'
        #                      f'Статус заказа: {status}')
        for item in products:
            money_sum += item[3]
            await call.message.answer(f'1){item[0]}\n2){item[1]}\n3)количество: {item[2]}\n4)сумма: {item[3]} рублей')
        await call.message.answer(f'Сумма заказа: {money_sum} рублей')
        await bot.send_message(chat_id='-1001558221765', text=f'Номер Заказа: {cart_id}\n{mode}\n'
                             f'Имя заказчика: {name}\nНомер телефона: {phone}\n'
                             f'Адрес доставки: {address}\nВремя: {customer_time}\n'
                             f'Статус заказа: {status}\n{products}\nСумма заказа: {money_sum} ')

    @dp.message_handler(commands='status')
    async def status_message(message: types.Message):
        await message.answer('Bot is working' + emojize(":pizza:"))

    @dp.message_handler(commands='заказ')
    async def start_dialog(message: types.Message):
        CommandHandler('20000, 30000', message.chat.id)
        data = SelectorDataDb(message.chat.id)
        if data.black_list_data:
            if data.black_list_data == 2:
                await message.answer("Извините, но вы находитесь в черном списке.\nЗа подробностями обратитесь по телефону")
                return 0
        else:
            CommandHandler('80000,', message.chat.id)
        CommandHandler('60000, 31000', message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        for dialog in data.dialogs:
            if data.emoji:
                keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(data.emoji)),
                                                        callback_data=dialog[1]))
            else:
                keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))
        await message.answer(data.quest, reply_markup=keyboard)

    @dp.message_handler(content_types='text')
    async def handle_text_message(message: types.Message):
        data = SelectorDataDb(message.chat.id)
        async def count_product_msg(message):
            try:
                count = int(message.text)
                if count > 999:
                    await message.answer('Слишком большое число')
                else:
                    command = 72000 + count
                    CommandHandler(f'40005, {str(command)}', message.chat.id)
                    data = SelectorDataDb(message.chat.id)
                    keyboard = types.InlineKeyboardMarkup()
                    for dialog in data.dialogs:
                        if dialog[2]:
                            keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(dialog[2])),
                                                        callback_data=dialog[1]))
                        else:
                            keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))
                    if not data.style_id == 0:
                        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))

                    await message.answer('Ваш заказ: ')
                    for item in data.quest:
                        await message.answer(f'1){item[0]}\n2){item[1]}\n3)количество: {item[2]}\n4)сумма: {item[3]} рублей')
                    await message.answer('Желаете что-нибудь еще, или перейдем к оформлению заказа?', reply_markup=keyboard)
                    await bot.delete_message(message.chat.id, message.message_id)
            except ValueError:
                await message.answer('Неверно введено число')

        async def update_customer_name(message):
            CommandHandler('40007, 73000', message.chat.id, message.text)
            data = SelectorDataDb(message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            for dialog in data.dialogs:
                if dialog[2]:                                                                           #if emoji is exists
                    keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(dialog[2])),
                                                            callback_data=dialog[1]))
                else:
                    keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))
            if not data.style_id == 0:
                keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
            await message.answer(data.quest, reply_markup=keyboard)
            await bot.delete_message(message.chat.id, message.message_id)

        async def update_phone_number(message):
            CommandHandler('40008, 74000', message.chat.id, message.text)
            data = SelectorDataDb(message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            for dialog in data.dialogs:
                if dialog[2]:                                                                           #if emoji is exists
                    keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(dialog[2])),
                                                            callback_data=dialog[1]))
                else:
                    keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))
            if not data.style_id == 0:
                keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
            await message.answer(data.quest, reply_markup=keyboard)
            await bot.delete_message(message.chat.id, message.message_id)

        async def update_delivery_address(message):
            CommandHandler('40011, 62000', message.chat.id, message.text)
            data = SelectorDataDb(message.chat.id)
            money_sum = 0
            cart_id = data.quest[0][0]
            mode = data.quest[0][1]
            if mode == 1: mode = 'Самовывоз'
            else: mode = 'Доставка'
            name = data.quest[0][2]
            phone = data.quest[0][3]
            address = data.quest[0][4]
            if not address: address = '-'
            customer_time = data.quest[0][5]
            if not customer_time: customer_time = '-'
            status = data.quest[0][6]
            if status == 0: status = 'Оформляется'
            products = data.quest[1]
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Завершить заказ', callback_data='end'))
            keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
            await message.answer(f'Номер Заказа: {cart_id}\n{mode}\n'
                                 f'Имя заказчика: {name}\nНомер телефона: {phone}\n'
                                 f'Адрес доставки: {address}\nВремя: {customer_time}\n'
                                 f'Статус заказа: {status}')
            for item in products:
                money_sum += item[3]
                await message.answer(f'1){item[0]}\n2){item[1]}\n3)количество: {item[2]}\n4)сумма: {item[3]} рублей')
            await message.answer(f'Сумма заказа: {money_sum} рублей', reply_markup=keyboard)

        async def update_customer_time(message):
            CommandHandler('40011, 63000', message.chat.id, message.text)
            data = SelectorDataDb(message.chat.id)
            money_sum = 0
            cart_id = data.quest[0][0]
            mode = data.quest[0][1]
            if mode == 1: mode = 'Самовывоз'
            else: mode = 'Доставка'
            name = data.quest[0][2]
            phone = data.quest[0][3]
            address = data.quest[0][4]
            if not address: address = '-'
            customer_time = data.quest[0][5]
            if not customer_time: customer_time = '-'
            status = data.quest[0][6]
            if status == 0: status = 'Оформляется'
            products = data.quest[1]
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Завершить заказ', callback_data='end'))
            keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
            await message.answer(f'Номер Заказа: {cart_id}\n{mode}\n'
                                 f'Имя заказчика: {name}\nНомер телефона: {phone}\n'
                                 f'Адрес доставки: {address}\nВремя: {customer_time}\n'
                                 f'Статус заказа: {status}')
            for item in products:
                money_sum += item[3]
                await message.answer(f'1){item[0]}\n2){item[1]}\n3)количество: {item[2]}\n4)сумма: {item[3]} рублей')
            await message.answer(f'Сумма заказа: {money_sum}', reply_markup=keyboard)


        if data.step_id == 4: await count_product_msg(message)
        if data.step_id == 6: await update_customer_name(message)
        if data.step_id == 7: await update_phone_number(message)
        if data.step_id == 9: await  update_delivery_address(message)
        if data.step_id == 10: await update_customer_time(message)

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
        await bot.edit_message_text(f'<u>{pre_answer}</u>', call.message.chat.id,
                                    call.message.message_id, reply_markup='')
        # await bot.edit_message_text(f'{pre_data.quest}\n<u>{pre_answer}</u>', call.message.chat.id,
        #                             call.message.message_id, reply_markup='')


# class SelectorDataDb():
#     def __init__(self, user_id):
#         self.user_id = user_id
#         self.steps = StepTable()
#         self.questions = QuestionsTable()
#         self.dia = DialogsTable()
#         self.emj = EmojiTable()
#         self.customer = Customer()
#         self.prod = Product()
#         self.cart_prod = CartProduct()
#         self.cart = Cart()
#
#         self.step_id = self.select_step_number_from_db(self.user_id)
#         self.style_id = self.select_style_id_from_db(self.user_id)
#         self.quest = self.select_question_from_db(self.step_id, self.style_id)
#         self.dialogs = self.select_dialog_from_db(self.step_id, self.style_id)
#         self.emoji = self.select_emoji_for_dialog(self.step_id, self.style_id)
#         self.black_list_data = self.check_black_list_about_customer(self.user_id)
#
#     def select_step_number_from_db(self, chat_id):
#         conditions = f'{self.steps.split_fields[0]}={chat_id}'
#         step_number = self.steps.select_in_table(self.steps.table_name,
#                                                  self.steps.split_fields[1],
#                                                  conditions
#                                                  )
#         if step_number:
#             return step_number[0][0]
#         else:
#             return None
#
#     def select_style_id_from_db(self, chat_id):
#         conditions = f'{self.steps.split_fields[0]}={chat_id}'
#         style_id = self.steps.select_in_table(self.steps.table_name,
#                                               self.steps.split_fields[2],
#                                               conditions)
#         if style_id:
#             return style_id[0][0]
#         else:
#             return None
#
#     def select_question_from_db(self, step_number, style_id):
#         conditions = f'{self.questions.split_fields[0]}={step_number}' \
#                      f'AND {self.questions.split_fields[1]}={style_id}'
#         data = self.questions.select_in_table(self.questions.table_name,
#                                               self.questions.split_fields[2],
#                                               conditions)
#         if step_number == 2:
#             sub_data = self.select_description_product(self.user_id)
#             return data[0][0] + sub_data
#         else:
#             return data[0][0]
#
#     def select_dialog_from_db(self, step_number, style_id):
#         conditions = f'{self.dia.split_fields[0]}={step_number}' \
#                      f'AND {self.dia.split_fields[1]}={style_id}'
#         data = self.dia.select_in_table(self.dia.table_name,
#                                         f'{self.dia.split_fields[2]}, '
#                                         f'{self.dia.split_fields[3]},'
#                                         f'{self.dia.split_fields[4]}',
#                                         conditions)
#         return data
#
#     def select_pre_step_dialog(self, step_number, style_id, command):
#         conditions = f"{self.dia.split_fields[0]}={step_number} "\
#                      f"AND {self.dia.split_fields[1]}={style_id} "\
#                      f"AND {self.dia.split_fields[3]}='{command}'"
#         data = self.dia.select_in_table(self.dia.table_name,
#                                         f'{self.dia.split_fields[2]}',
#                                         conditions)
#         return data[0][0]
#
#     def select_emoji_for_dialog(self, step_number, style_id):
#         conditions = f"{self.emj.split_fields[0]}={step_number}" \
#                      f"AND {self.emj.split_fields[1]}={style_id}"
#         data = self.emj.select_in_table(self.emj.table_name,
#                                         f'{self.emj.split_fields[2]}',
#                                         conditions)
#         print(data)
#         if data:
#             return data[0][0]
#         else:
#             return None
#
#     def check_black_list_about_customer(self, chat_id):
#         conditions = f"{self.customer.split_fields[0]}={chat_id}"
#         data = self.customer.select_in_table(self.customer.table_name,
#                                              f'{self.customer.split_fields[3]}',
#                                              conditions
#                                              )
#         if data:
#             return data[0][0]
#         else:
#             return None
#
#     def select_description_product(self, chat_id):
#         product_id = self.select_product_id(chat_id)
#         conditions = f'{self.prod.split_fields[0]}={product_id}'
#         data = self.prod.select_in_table(self.prod.table_name,
#                                          self.prod.split_fields[2],
#                                          conditions)
#         return data[0][0]
#
#     def select_product_id(self, chat_id):
#         cart_prod_id = self.select_last_cart_product_id(chat_id)
#         conditions = f'{self.cart_prod.split_fields[0]}={cart_prod_id}'
#         data = self.cart_prod.select_in_table(self.cart_prod.table_name,
#                                               self.cart_prod.split_fields[2],
#                                               conditions)
#         return data[0][0]
#
#     def select_last_cart_product_id(self, chat_id):
#         cart_id = self.select_last_cart_id(chat_id)
#         conditions = f'{self.cart_prod.split_fields[1]}={cart_id}'
#         data = self.cart_prod.select_in_table(self.cart_prod.table_name,
#                                               f'MAX({self.cart_prod.split_fields[0]})',
#                                               conditions)
#         return data[0][0]
#
#     def select_last_cart_id(self, chat_id):
#         conditions = f'{self.cart.split_fields[1]}={chat_id}'
#         print('conditions last cart: ', conditions)
#         data = self.cart.select_in_table(self.cart.table_name,
#                                          f'MAX({self.cart.split_fields[0]})',
#                                          conditions)
#         print(data[0][0])
#         return data[0][0]

if __name__ == '__main__':
    cl = MyBot()
    executor.start_polling(dp, skip_updates=True)
