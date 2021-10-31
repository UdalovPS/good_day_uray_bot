from Database import *
from new_data_selector import SelectorDataDb
from datetime import date, datetime


class CommandHandler(SelectorDataDb):
    def __init__(self, commands, message) -> None:
        self.message = message
        self.chat_id = message.chat.id
        self.message_text = message.text
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
        10 000 - delete fields from steps_table where chat_id = message.chat.id;
        11 000 - insert zero step and style id;
        12 000 - change style_id;
        13 000 - change step_id;
        14 000 return to previous step;
        """
        for command in self.commands:
            print('COMMANDS: ', command)
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


    def __delete_data_from_step_id(self, chat_id) -> None:
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.delete_data_from_table(self.steps.table_name, conditions)

    def __insert_zero_step_and_style(self, chat_id) -> None:
        self.steps.insert_data_in_table(self.steps.table_name, self.steps.fields,
                                        f'({chat_id},0,0)'
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

    def __return_to_previous_step(self, chat_id):
        sel = SelectorDataDb(self.message)
        step_id = sel.select_step_id_from_db()
        if step_id == 0:
            self.__change_style_id(0, chat_id)
        else:
            pre_question = sel.select_pre_question_id()
            self.__change_step_id(pre_question, chat_id)
