from Database.posgre_sql import StepTable, QuestionsTable, DialogsTable

"""
Command handler algorithm:
    10 000 - change style_id (Example: 10001 - style_id = 001);
    20 000 - delete fields from steps_table to chat_id;
    30 000 - insert style_id=0, step_id=0 in step_table;
    40 000 - change step in step_table;
"""

class CommandHandler():
    def __init__(self, commands, chat_id):
        self.chat_id = chat_id
        self.commands = commands.split(',')
        # self.cod = self.commands // 1000
        # self.value = self.commands % 1000

        self.steps = StepTable()
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()

    def command_parser(self):
        print(self.commands)
        for command in self.commands:
            if command:
                int_cmd = int(command)
                cod = int_cmd // 1000
                value = int_cmd % 1000
                if cod == 10:
                    self.change_style_id(value, self.chat_id)
                if cod == 20:
                    self.delete_data_from_step_id(self.chat_id)
                if cod == 30:
                    self.insert_zero_step_and_style(self.chat_id)
                if cod == 40:
                    self.change_step_id(value, self.chat_id)

    def change_style_id(self, value, chat_id):
        field_value = f'{self.steps.split_fields[2]}={value}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name,
                                 field_value,
                                 conditions
                                 )

    def delete_data_from_step_id(self, chat_id):
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.delete_data_from_table(self.steps.table_name,
                                          conditions
                                          )

    def insert_zero_step_and_style(self, chat_id):
        self.steps.insert_data_in_table(self.steps.table_name,
                                        self.steps.fields,
                                        f'({chat_id},0,0)')

    def change_step_id(self, value, chat_id):
        field_value = f'{self.steps.split_fields[1]}={value}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name,
                                 field_value,
                                 conditions
                                 )

if __name__ == '__main__':
    a = CommandHandler(10001, 12)

