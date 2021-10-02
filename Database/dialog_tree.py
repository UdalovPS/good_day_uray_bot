from posgre_sql import QuestionsTable, DialogsTable

class DialogTree():
    def __init__(self):
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()

    def insert_question(self, step_number, style_id, question):
        self.questions.insert_data_in_table(self.questions.table_name,
                                            self.questions.fields,
                                            f'{step_number, style_id, question}')

    def insert_dialog(self, dialog):
        self.dialogs.insert_data_in_table(self.dialogs.table_name,
                                          self.dialogs.fields,
                                          f"({dialog[0]}, {dialog[1]}, '{dialog[2]}')")


class ZeroStep(DialogTree):
    def __init__(self):
        super().__init__()
        self.step_number = 0
        self.style_id = 0
        self.question = 'В каком стиле будем вести диалог?'
        self.choice_dialogs = ((self.step_number, 1, 'Стандартный'),
                       (self.step_number, 2, 'Как БРО!'))


if __name__ == '__main__':
    s0 = ZeroStep()
    # s0.insert_question(s0.step_number, s0.style_id, s0.question)
    for dialog in s0.choice_dialogs:
        s0.insert_dialog(dialog)

    pass
