from Database.posgre_sql import StepTable, QuestionsTable, DialogsTable
from Database.posgre_sql import Customer, EmojiTable, Product, CartProduct
from Database.posgre_sql import Cart


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
    pass
