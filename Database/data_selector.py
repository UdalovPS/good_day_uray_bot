# from Database.posgre_sql import StepTable, QuestionsTable, DialogsTable
# from Database.posgre_sql import Customer, EmojiTable, Product, CartProduct
# from Database.posgre_sql import Cart
from Database import *


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
        self.status = StatusTable()

        self.step_id = self.select_step_number_from_db(self.user_id)
        self.style_id = self.select_style_id_from_db(self.user_id)
        self.quest = self.select_question_from_db(self.step_id, self.style_id)
        self.dialogs = self.select_dialog_from_db(self.step_id, self.style_id)
        self.emoji = self.select_emoji_for_dialog(self.step_id, self.style_id)
        self.black_list_data = self.check_black_list_about_customer(self.user_id)
        self.status_description = self.select_status_description(self.user_id)

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

        elif step_number == 5:
            sub_data = self.select_intermediate_data_about_cart(self.user_id)
            print(sub_data)
            return sub_data
        elif step_number == 11:
            data = self.select_final_data_about_cart(self.user_id)
            return data
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

    def select_intermediate_data_about_cart(self, chat_id):
        cart_id = self.select_last_cart_id(chat_id)
        conditions = f'{self.cart_prod.split_fields[2]}={self.prod.split_fields[0]} AND' \
                     f' {self.cart_prod.split_fields[1]}={cart_id} AND' \
                     f' {self.cart_prod.split_fields[5]}=1'
        data = self.cart_prod.inner_join_in_table(self.cart_prod.table_name,
                                                  self.prod.table_name,
                                                  f'{self.prod.split_fields[1]},'
                                                  f'{self.cart_prod.split_fields[4]},'
                                                  f'{self.cart_prod.split_fields[3]},'
                                                  f'{self.prod.split_fields[3]}',
                                                  conditions)
        data = list(data)
        i = 0
        for item in data:
            data[i] = list(data[i])
            data[i][3] = data[i][3] * data[i][2]
            i += 1
        return data

    def select_final_data_about_cart(self, chat_id):
        products = self.select_intermediate_data_about_cart(chat_id)
        customer_cart_data = self.select_data_about_customer_and_about_cart(chat_id)
        data_list = [customer_cart_data[0], products]
        return data_list

    def select_data_about_customer_and_about_cart(self, chat_id):
        cart_id = self.select_last_cart_id(chat_id)
        fields = f'cart_table.id, user_id, mode, name, phone, address, customer_time, ' \
                 f'status, date, time'
        main_table = 'cart_table'
        sub_table_1 = 'date_time_place_table'
        sub_table_2 = 'customer_table'
        conditions_1 = f"cart_id = {cart_id} AND cart_table.id = {cart_id}"
        conditions_2 = f"customer_table.id = user_id"
        data = self.cart.three_table_join_in_table(main_table, sub_table_1, sub_table_2,
                                                   fields, conditions_1, conditions_2)
        return data

    def select_status_description(self, chat_id):
        cart_id = self.select_last_cart_id(chat_id)
        cart_status = self.select_status_number_of_cart(cart_id)
        conditions = f'{self.status.split_fields[0]}={cart_status}'
        data = self.status.select_in_table(self.status.table_name,
                                           self.status.split_fields[1],
                                           conditions
                                           )
        return data[0][0]

    def select_status_number_of_cart(self, cart_id):
        conditions = f'{self.cart.split_fields[0]}={cart_id}'
        print(conditions)
        data = self.cart.select_in_table(self.cart.table_name,
                                         self.cart.split_fields[2],
                                         conditions
                                         )
        print(data)
        return data[0][0]


if __name__ == '__main__':
    pass
