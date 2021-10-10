from Database.posgre_sql import StepTable, QuestionsTable, DialogsTable

"""
Command handler algorithm:
    10 000 - change style_id (Example: 10001 - style_id = 001);
    20 000 - delete fields from steps_table to chat_id;
    30 000 - insert style_id=0, step_id=0 in step_table;
    40 000 - change step in step_table;
    50 000 - back to previous step;
"""

class CommandHandler():
    def __init__(self, commands, chat_id):
        self.chat_id = chat_id
        self.commands = commands.split(',')

        self.steps = StepTable()
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()

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
                if cod == 40:
                    self.__change_step_id(value, self.chat_id)
                if cod == 50:
                    self.__back_to_previous_step(self.chat_id)

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
        value = self.__select_pre_step_id(step_style_list[0][0], step_style_list[0][1])
        if value == 0:
            field_value = f'{self.steps.split_fields[2]}={value}'
        else:
            field_value = f'{self.steps.split_fields[1]}={value}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

if __name__ == '__main__':
    a = CommandHandler(10001, 12)
