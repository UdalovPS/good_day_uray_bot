from Database import *
from new_data_selector import SelectorDataDb
from datetime import date, datetime


class CommandHandler(SelectorDataDb):
    def __init__(self, commands, message) -> None:
        self.message = message
        self.chat_id = message.chat.id
        self.message_text = message.text
        self.message_id = message.message_id
        self.commands = commands.split(',')

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

    def command_parser(self) -> None:
        """
        Command handler algorithm:
        10 - is commands for work with <step_table>;
        10 000 - delete fields from steps_table where chat_id = message.chat.id;
        11 000 - insert zero step and style id;
        12 000 - change style_id;
        13 000 - change step_id;
        14 000 - return to previous step;
        15 000 - update sticker_id in step_table;
        16 000 - delete sticker_id from step_table;

        20 - is commands for work with <cart_product_table>;
        20 000 - insert new row in cart_product_table;

        30 - is commands for work with <cart_table>;
        30 000 - insert new row in cart_table;
        """
        for command in self.commands:
            if command:
                int_cmd = int(command)
                cod = int_cmd // 1000
                value = int_cmd % 1000
                if cod == 10:
                    self.__delete_data_from_step_id(self.chat_id)
                if cod == 11:
                    self.__insert_zero_step_and_style(self.chat_id)
                if cod == 12:
                    self.__change_style_id(value, self.chat_id)
                if cod == 13:
                    self.__change_step_id(value, self.chat_id)
                if cod == 14:
                    self.__return_to_previous_step(self.chat_id)
                if cod == 15:
                    self.__update_sticker_id_in_step_table(self.chat_id)
                if cod == 16:
                    self.__delete_sticker_id_from_step_table(self.chat_id)
                if cod == 20:
                    # self.__delete_sticker_id_from_step_table(self.chat_id)
                    pass
                if cod == 30:
                    self.__insert_start_cart_data(self.chat_id)


    def __delete_data_from_step_id(self, chat_id) -> None:
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.delete_data_from_table(self.steps.table_name, conditions)

    def __insert_zero_step_and_style(self, chat_id) -> None:
        self.steps.insert_data_in_table(self.steps.table_name, self.steps.fields,
                                        f'({chat_id},0,0,0)'
                                        )

    def __change_style_id(self, value, chat_id) -> None:
        field_value = f'{self.steps.split_fields[2]}={value}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    def __change_step_id(self, value, chat_id) -> None:
        field_value = f'{self.steps.split_fields[1]}={value}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    def __return_to_previous_step(self, chat_id) -> None:
        sel = SelectorDataDb(self.message)
        step_id = sel.select_step_id_from_db()
        if step_id == 0:
            self.__change_style_id(0, chat_id)
        else:
            pre_question = sel.select_pre_question_id()
            self.__change_step_id(pre_question, chat_id)

    def __insert_start_cart_data(self, chat_id) -> None:
        self.cart.insert_data_in_table(self.cart.table_name,
                                       f'{self.cart.split_fields[1]},'
                                       f'{self.cart.split_fields[2]}',
                                       f'({chat_id},0)'
                                       )

    def __update_sticker_id_in_step_table(self, chat_id) -> None:
        field_value = f'{self.steps.split_fields[3]}={self.message_id}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    def __delete_sticker_id_from_step_table(self, chat_id) -> None:
        field_value = f'{self.steps.split_fields[3]}={0}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )
