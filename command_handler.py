# from Database.posgre_sql import StepTable, QuestionsTable, DialogsTable
# from Database.posgre_sql import Cart, CartProduct, Customer, Additional
# from Database.posgre_sql import
from Database import *
from Database.data_selector import SelectorDataDb
from datetime import date, datetime

"""
Command handler algorithm:
    10 000 - change style_id (Example: 10001 - style_id = 001);
    20 000 - delete fields from steps_table to chat_id;
    30 000 - insert style_id=0, step_id=0 in step_table;
    31 000 - insert new row in date_time_place_table;
    40 000 - change step in step_table;
    50 000 - back to previous step;
    60 000 - insert new row in cart table;
    61 000 - update data in date_time_place_table;
    62 000 - update delivery address;
    63 000 - update customer_time;
    70 000 - insert new row in cart product table;
    71 000 - update wishes in cart_product table;
    72 000 - update count in cart_product table;
    73 000 - update status in cart_product table and customer name;
    74 000 - update phone number;
    80 000 - insert new customer;
    90 000 - update cart status;
    91 000 - delete garbage from db;
    92 000 - update tmp_cart_id in admin table;
    
"""

class CommandHandler(SelectorDataDb):
    def __init__(self, commands, chat_id, message_text=None):
        self.chat_id = chat_id
        self.commands = commands.split(',')
        self.message_text = message_text

        self.steps = StepTable()
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()
        self.cart = Cart()
        self.cart_prod = CartProduct()
        self.customer = Customer()
        self.wishes = Additional()
        self.date_place = DateTimePlace()
        self.admin = AdminTable()

        self.command_parser()

    def command_parser(self):
        print(self.commands)
        for command in self.commands:
            if command:
                int_cmd = int(command)
                cod = int_cmd // 1000
                value = int_cmd % 1000
                if cod == 10:
                    self.__change_style_id(value, self.chat_id)
                if cod == 20:
                    self.__delete_data_from_step_id(self.chat_id)
                if cod == 30:
                    self.__insert_zero_step_and_style(self.chat_id)
                if cod == 31:
                    self.__insert_new_date_time_place_row(self.chat_id)
                if cod == 40:
                    self.__change_step_id(value, self.chat_id)
                if cod == 50:
                    self.__back_to_previous_step(self.chat_id)
                if cod == 60:
                    self.__insert_start_cart_data(self.chat_id)
                if cod == 61:
                    self.__update_delivery_mode(self.chat_id, value)
                if cod == 62:
                    self.__update_delivery_address(self.chat_id, self.message_text)
                if cod == 63:
                    self.__update_customer_time(self.chat_id, self.message_text)
                if cod == 70:
                    self.__insert_new_row_in_product_cart_table(self.chat_id, value)
                if cod == 71:
                    self.__update_wishes_in_cart_product_table(self.chat_id, value)
                if cod == 72:
                    self.__update_product_count_in_cart_table(self.chat_id, value)
                if cod == 73:
                    self.__update_customer_name(self.chat_id, self.message_text)
                if cod == 74:
                    self.__update_phone_number(self.chat_id, self.message_text)
                if cod == 80:
                    self.__insert_new_customer(self.chat_id)
                if cod == 90:
                    self.__update_cart_status(self.chat_id, value)
                if cod == 91:
                    self.__delete_garbage_from_db(self.chat_id)
                if cod == 92:
                    self.__update_tmp_cart_id(self.message_text)
                    break
                if cod == 93:
                    self.__update_cart_status(self.chat_id, value,
                                              self.__select_tmp_cart_id())

    def __change_style_id(self, value, chat_id):
        field_value = f'{self.steps.split_fields[2]}={value}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    def __delete_data_from_step_id(self, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.delete_data_from_table(self.steps.table_name, conditions)

    def __insert_zero_step_and_style(self, chat_id):
        self.steps.insert_data_in_table(self.steps.table_name, self.steps.fields,
                                        f'({chat_id},0,0)'
                                        )

    def __change_step_id(self, value, chat_id):
        field_value = f'{self.steps.split_fields[1]}={value}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    def __select_step_style_now_message(self, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        data = self.steps.select_in_table(self.steps.table_name,
                                       f'{self.steps.split_fields[1]},'
                                       f'{self.steps.split_fields[2]}',
                                       conditions)
        print('this is step style now', data)
        return data

    def __select_pre_step_id(self, step_id, style_id):
        conditions = f'{self.questions.split_fields[0]}={step_id} ' \
                     f'AND {self.questions.split_fields[1]}={style_id}'
        data = self.questions.select_in_table(self.questions.table_name,
                                              f'{self.questions.split_fields[3]}',
                                              conditions)
        print('this is pre step_id', data[0][0])
        return data[0][0]

    def __back_to_previous_step(self, chat_id):
        step_style_list = self.__select_step_style_now_message(chat_id)
        print("BACK LIST")
        value = self.__select_pre_step_id(step_style_list[0][0], step_style_list[0][1])
        print("BACK VALUE:", value)
        if step_style_list[0][0] == 0:
            field_value = f'{self.steps.split_fields[2]}={value}'
            print("BACK STYLE: ", field_value)
        else:
            field_value = f'{self.steps.split_fields[1]}={value}'
            print("BACK STEP: ", field_value)
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    def __insert_start_cart_data(self, chat_id):
        self.cart.insert_data_in_table(self.cart.table_name,
                                       f'{self.cart.split_fields[1]},'
                                       f'{self.cart.split_fields[2]}',
                                       f'({chat_id},0)'
                                       )

    def __insert_new_customer(self, chat_id):
        self.customer.insert_data_in_table(self.customer.table_name,
                                           f'{self.cart.split_fields[0]},'
                                           f'{self.customer.split_fields[3]}',
                                           f'({chat_id}, 1)'
                                           )

    def __select_max_cart_id(self, chat_id):
        conditions = f'{self.cart.split_fields[1]}={chat_id}'
        data = self.cart.select_in_table(self.cart.table_name,
                                         f'MAX({self.cart.split_fields[0]})',
                                         conditions)
        return data[0][0]

    def __insert_new_row_in_product_cart_table(self, chat_id, value):
        cart_id = self.__select_max_cart_id(chat_id)
        self.cart_prod.insert_data_in_table(self.cart_prod.table_name,
                                            f'{self.cart_prod.split_fields[1]},'
                                            f'{self.cart_prod.split_fields[2]},'
                                            f'{self.cart_prod.split_fields[5]}',
                                            f'({cart_id}, {value}, 0)')

    def __update_wishes_in_cart_product_table(self, chat_id, value):
        wishes_name = self.__select_wishes_name_from_additional_table(value)
        cart_product_id = self.select_last_cart_product_id(chat_id)
        conditions = f'{self.cart_prod.split_fields[0]}={cart_product_id}'
        field_value = f"{self.cart_prod.split_fields[4]}='{wishes_name}'"
        self.cart_prod.update_fields(self.cart_prod.table_name,
                                     field_value, conditions
                                     )

    def __select_wishes_name_from_additional_table(self, wishes_id):
        conditions = f'{self.wishes.split_fields[0]}={wishes_id}'
        data = self.wishes.select_in_table(self.wishes.table_name,
                                           self.wishes.split_fields[1],
                                           conditions)
        return data[0][0]

    def __update_product_count_in_cart_table(self, chat_id, value):
        cart_product_id = self.select_last_cart_product_id(chat_id)
        conditions = f'{self.cart_prod.split_fields[0]}={cart_product_id}'
        field_value = f"{self.cart_prod.split_fields[3]}={value}," \
                      f"{self.cart_prod.split_fields[5]}=1"
        self.cart_prod.update_fields(self.cart_prod.table_name,
                                     field_value, conditions
                                     )

    def __update_customer_name(self, chat_id, value):
        conditions = f'{self.customer.split_fields[0]}={chat_id}'
        field_value = f"{self.customer.split_fields[1]}='{value}'"
        self.customer.update_fields(self.customer.table_name,
                                    field_value, conditions)

    def __update_phone_number(self, chat_id, value):
        conditions = f'{self.customer.split_fields[0]}={chat_id}'
        field_value = f"{self.customer.split_fields[2]}='{value}'"
        self.customer.update_fields(self.customer.table_name,
                                    field_value, conditions)

    def __insert_new_date_time_place_row(self, chat_id):
        cart_id = self.__select_max_cart_id(chat_id)
        self.cart.insert_data_in_table(self.date_place.table_name,
                                       f'{self.date_place.split_fields[0]}',
                                       f'({cart_id})'
                                       )

    def __update_delivery_mode(self, chat_id, value):
        cart_id = self.__select_max_cart_id(chat_id)
        date_now = date.today()
        time_now = datetime.now().time()
        conditions = f'{self.date_place.split_fields[0]}={cart_id}'
        field_value = f"{self.date_place.split_fields[1]}='{date_now}'," \
                      f"{self.date_place.split_fields[2]}='{time_now}'," \
                      f"{self.date_place.split_fields[3]}={value}"
        self.date_place.update_fields(self.date_place.table_name,
                                      field_value, conditions)

    def __update_delivery_address(self, chat_id, value):
        cart_id = self.__select_max_cart_id(chat_id)
        conditions = f'{self.date_place.split_fields[0]}={cart_id}'
        field_value = f"{self.date_place.split_fields[4]}='{value}'"
        self.date_place.update_fields(self.date_place.table_name,
                                      field_value, conditions)

    def __update_customer_time(self, chat_id, value):
        cart_id = self.__select_max_cart_id(chat_id)
        conditions = f'{self.date_place.split_fields[0]}={cart_id}'
        field_value = f"{self.date_place.split_fields[5]}='{value}'"
        self.date_place.update_fields(self.date_place.table_name,
                                      field_value, conditions)

    def __update_cart_status(self, chat_id, value, cart_number=None):
        if not cart_number:
            cart_id = self.__select_max_cart_id(chat_id)
        else:
            cart_id = cart_number
        conditions = f'{self.cart.split_fields[0]}={cart_id}'
        field_value = f"{self.cart.split_fields[2]}={value}"
        self.cart.update_fields(self.cart.table_name,
                                field_value, conditions)

    def __delete_garbage_from_db(self, chat_id):
        cart_id = self.__select_max_cart_id(chat_id)
        cart_conditions = f'{self.cart.split_fields[2]}=0 AND {self.cart.split_fields[1]}={chat_id}'
        cart_prod_conditions = f'{self.cart_prod.split_fields[1]}={cart_id} AND {self.cart_prod.split_fields[5]}=0'
        self.cart_prod.delete_data_from_table(self.cart_prod.table_name, cart_prod_conditions)
        self.cart.delete_data_from_table(self.cart.table_name, cart_conditions)

    def __update_tmp_cart_id(self, new_cart_id):
        field_value = f"{self.admin.split_fields[1]}={new_cart_id}"
        self.admin.update_fields(self.admin.table_name, field_value)

    def __select_tmp_cart_id(self):
        data = self.admin.select_in_table(self.admin.table_name,
                                          self.admin.split_fields[1])
        return data[0][0]




if __name__ == '__main__':
    # a = CommandHandler(10001, 12)
    pass

