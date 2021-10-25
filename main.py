import logging
from emoji import emojize
from aiogram import Bot, Dispatcher, executor, types

from config import ConfigTelebot
from command_handler import CommandHandler
from Database.data_selector import SelectorDataDb
from former_data_about_cart import DataCartFormer

bot = Bot(token=ConfigTelebot().api_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

class MyBot():
    async def add_standart_dialogs_to_inline_keyboard(self, data, keyboard):
        for dialog in data.dialogs:
            if data.emoji:
                keyboard.add(types.InlineKeyboardButton(text=(dialog[0] + emojize(data.emoji)),
                                                        callback_data=dialog[1]))
            else:
                keyboard.add(types.InlineKeyboardButton(text=dialog[0], callback_data=dialog[1]))

    async def add_number_products(self, message):
        try:
            count = int(message.text)
            if count > 999:
                await message.answer('Слишком большое число')
            else:
                command = 72000 + count
                CommandHandler(f'40005, {str(command)}', message.chat.id)
                data = SelectorDataDb(message.chat.id)
                keyboard = types.InlineKeyboardMarkup()
                await MyBot().add_standart_dialogs_to_inline_keyboard(data, keyboard)
                if not data.style_id == 0:
                    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
                products_message = await DataCartFormer().form_data_to_products_message(data.quest, 'Ваш заказ: ')
                await message.answer(products_message)
                await message.answer('Желаете что-нибудь еще, или перейдем к оформлению заказа?', reply_markup=keyboard)
                await bot.delete_message(message.chat.id, message.message_id)
        except ValueError:
            await message.answer('Неверно введено число')

    async def update_customer_name(self, message):
        CommandHandler('40007, 73000', message.chat.id, message.text)
        data = SelectorDataDb(message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        await MyBot().add_standart_dialogs_to_inline_keyboard(data, keyboard)
        if not data.style_id == 0:
            keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
        await message.answer(data.quest, reply_markup=keyboard)
        await bot.delete_message(message.chat.id, message.message_id)

    async def update_phone_number(self, message):
            CommandHandler('40008, 74000', message.chat.id, message.text)
            data = SelectorDataDb(message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            await MyBot().add_standart_dialogs_to_inline_keyboard(data, keyboard)
            if not data.style_id == 0:
                keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
            await message.answer(data.quest, reply_markup=keyboard)
            await bot.delete_message(message.chat.id, message.message_id)

    async def update_delivery_or_custom_time_address(self, message, command):
        CommandHandler(command, message.chat.id, message.text)                  #'40011, 62000'
        data = SelectorDataDb(message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Завершить заказ', callback_data='end'))
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
        text_msg = await DataCartFormer().data_for_customer_about_cart(data.quest, 'Ваш заказ:', data.status_description)
        await message.answer(text_msg, reply_markup=keyboard)

    async def update_customer_time(self, message):
        CommandHandler('40011, 63000', message.chat.id, message.text)
        data = SelectorDataDb(message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Завершить заказ', callback_data='end'))
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
        text_msg = await DataCartFormer().data_for_customer_about_cart(data.quest, 'Ваш заказ:', data.status_description)
        await message.answer(text_msg, reply_markup=keyboard)

    @dp.callback_query_handler(text='end')
    async def end_cart_with_user(call: types.CallbackQuery):
        CommandHandler('90001, 91000', call.message.chat.id)
        data = SelectorDataDb(call.message.chat.id)
        # money_sum = 0
        # cart_id = data.quest[0][0]
        # mode = data.quest[0][1]
        # if mode == 1: mode = 'Самовывоз'
        # else: mode = 'Доставка'
        # name = data.quest[0][2]
        # phone = data.quest[0][3]
        # address = data.quest[0][4]
        # if not address: address = '-'
        # customer_time = data.quest[0][5]
        # if not customer_time: customer_time = '-'
        # status = data.quest[0][6]
        # if status == 0:
        #     status = 'Оформляется'
        # elif status == 1:
        #     status = 'Оформлен'
        # products = data.quest[1]
        customer_msg = await DataCartFormer().data_for_customer_about_cart(data.quest, 'Ваш заказ:', data.status_description)
        persoanl_msg = await DataCartFormer().data_for_customer_about_cart_for_personal(data.quest, 'Ваш заказ:', data.status_description)
        # await call.message.answer(f'Номер Заказа: {cart_id}\n{mode}\n'
        #                      f'Имя заказчика: {name}\nНомер телефона: {phone}\n'
        #                      f'Адрес доставки: {address}\nВремя: {customer_time}\n'
        #                      f'Статус заказа: {status}')

        # for item in products:
        #     money_sum += item[3]
        #     await call.message.answer(f'1){item[0]}\n2){item[1]}\n3)количество: {item[2]}\n4)сумма: {item[3]} рублей')
        # await call.message.answer(f'Сумма заказа: {money_sum} рублей')
        # await bot.send_message(chat_id='-1001558221765', text=f'Номер Заказа: {cart_id}\n{mode}\n'
        #                      f'Имя заказчика: {name}\nНомер телефона: {phone}\n'
        #                      f'Адрес доставки: {address}\nВремя: {customer_time}\n'
        #                      f'Статус заказа: {status}\n{products}\nСумма заказа: {money_sum} ')
        await call.message.answer(customer_msg)
        await bot.send_message(chat_id='-1001558221765', text=persoanl_msg)

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
        await MyBot().add_standart_dialogs_to_inline_keyboard(data, keyboard)
        await message.answer(data.quest, reply_markup=keyboard)

    @dp.message_handler(content_types='text')
    async def handle_text_message(message: types.Message):
        data = SelectorDataDb(message.chat.id)
        if data.step_id == 4: await MyBot().add_number_products(message)
        if data.step_id == 6: await MyBot().update_customer_name(message)
        if data.step_id == 7: await MyBot().update_phone_number(message)
        if data.step_id == 9: await MyBot().update_delivery_or_custom_time_address(message, '40011, 62000')
        if data.step_id == 10: await MyBot().update_delivery_or_custom_time_address(message, '40011, 63000')

    @dp.callback_query_handler(text='back')
    async def back_command(call: types.CallbackQuery):
        CommandHandler('50000,', call.message.chat.id)
        data = SelectorDataDb(call.message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        await MyBot().add_standart_dialogs_to_inline_keyboard(data, keyboard)
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
        await MyBot().add_standart_dialogs_to_inline_keyboard(data, keyboard)
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))

        await call.message.answer(data.quest, reply_markup=keyboard)
        await bot.edit_message_text(f'<u>{pre_answer}</u>', call.message.chat.id,
                                    call.message.message_id, reply_markup='')


if __name__ == '__main__':
    cl = MyBot()
    executor.start_polling(dp, skip_updates=True)
