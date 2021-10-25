from datetime import datetime, date

class DataCartFormer():
    async def form_data_to_products_message(self, data, start_phrase="Выбрано: "):
        product_message = f'{start_phrase}\n'
        money_sum = 0
        for item in data:
            product_message += f'1){item[0]}\n'
            product_message += f'2){item[1]}\n'
            product_message += f'3)Количество: {item[2]}\n'
            product_message += f'4)Сумма: {item[3]} рублей\n'
            product_message += '.........................\n'
            money_sum += item[3]
        product_message += f'Итоговая сумма: {money_sum} рублей\n'
        return product_message

    async def form_data_about_cart(self, data):
        cart_id = data[0]
        user_id = data[1]
        mode = data[2]
        if mode == 1: mode = 'Самовывоз'
        else: mode = 'Доставка по адресу'
        name = data[3]
        phone = data[4]
        address = data[5]
        if not address: address = '-'
        customer_time = data[6]
        if not customer_time: customer_time = '-'
        date = data[8].strftime('%d.%m.%Y')
        cart_message = f'Номер заказа: <strong>{cart_id}</strong>\n' \
                       f'<u><strong>{mode}</strong></u>\n' \
                       f'Дата Заказа: <strong>{date}</strong>\n' \
                       f'Ваш уникальный номер: <strong>{user_id}</strong>\n'\
                       f'Ваше Имя: <strong>{name}</strong>\n' \
                       f'Ваш телефона: <strong>{phone}</strong>\n'\
                       f'Адрес доставки: <strong>{address}</strong>\n' \
                       f'Время готовности: <strong>{customer_time}</strong>\n'
        return cart_message

    async def data_for_customer_about_cart(self, data, start_phrase, status):
        products_data_from_sql = data[1]
        cart_data_from_sql = data[0]
        status = f'Статус заказа: {status}\n'
        products_data = await self.form_data_to_products_message(products_data_from_sql, start_phrase)
        cart_data = await self.form_data_about_cart(cart_data_from_sql)
        return cart_data + status + products_data

    async def form_data_about_cart_for_personal(self, data):
        cart_id = data[0]
        user_id = data[1]
        mode = data[2]
        if mode == 1: mode = 'Самовывоз'
        else: mode = 'Доставка по адресу'
        name = data[3]
        phone = data[4]
        address = data[5]
        if not address: address = '-'
        customer_time = data[6]
        if not customer_time: customer_time = '-'
        cart_date = data[8].strftime('%d.%m.%Y')
        cart_time = data[9].strftime('%H:%M')
        cart_message = f'Номер заказа: <strong>{cart_id}</strong>\n' \
                       f'<u><strong>{mode}</strong></u>\n' \
                       f'Дата Заказа: <strong>{cart_date}</strong>\n' \
                       f'Время заказа: <strong>{cart_time}</strong>\n' \
                       f'Идентификационный номер заказчика: <strong>{user_id}</strong>\n'\
                       f'Имя заказчика: <strong>{name}</strong>\n' \
                       f'Телефон заказчика: <strong>{phone}</strong>\n'\
                       f'Адрес доставки: <strong>{address}</strong>\n' \
                       f'Время готовности: <strong>{customer_time}</strong>\n'
        return cart_message

    async def data_for_customer_about_cart_for_personal(self, data, start_phrase, status):
        products_data_from_sql = data[1]
        cart_data_from_sql = data[0]
        status = f'Статус заказа: {status}\n'
        products_data = await self.form_data_to_products_message(products_data_from_sql, start_phrase)
        cart_data = await self.form_data_about_cart_for_personal(cart_data_from_sql)
        return cart_data + status + products_data





