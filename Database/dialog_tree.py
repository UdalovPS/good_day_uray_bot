from posgre_sql import QuestionsTable, DialogsTable

class DialogTree():
    def __init__(self):
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()

    def insert_question(self, step_number, style_id, question):
        self.questions.insert_data_in_table(self.questions.table_name,
                                            self.questions.fields,
                                            f'{step_number, style_id, question}')

    def insert_dialog(self, step, style, dialog):
        self.dialogs.insert_data_in_table(self.dialogs.table_name,
                                          self.dialogs.fields,
                                          f"({step}, {style}, '{dialog[0]}', "
                                          f"'{dialog[1]}')")


class ZeroStepStyle(DialogTree):
    def __init__(self):
        super().__init__()
        self.step_number = 0
        self.style_id = 0
        self.question = 'В каком стиле будем вести диалог?'
        self.choice_dialogs = ((self.step_number, 0, 'В стандартном', '10001,'),
                       (self.step_number, 0, 'Как БРО!', '10002,'))



class FirstStep(DialogTree):
    def __init__(self):
        super().__init__()
        self.step_number = 1
        self.style_id = 1
        self.question = 'Что хотите заказать?'
        self.choice_dialogs = ((self.step_number, self.style_id, 'Шаурма №1', 11, 1),
                               (self.step_number, self.style_id, 'Шаурма №2', 12, 1),
                               (self.step_number, self.style_id, 'Шаурма №3', 13, 1))

class Dialogs(DialogTree):
    def __init__(self):
        super(Dialogs, self).__init__()
        self.style = (0, 0, 'В каком стиле будем вести диалог?',
                      (('В стандартном', '10001,'), ('Как БРО!', '10002.')))

        self.step_zero_1 = (0, 1, 'Что хотите заказать?',
                          (('Шаурму', '40001,'),)
                          )
        self.step_zero_2 = (0, 2, 'Что будешь хавать?',
                          (('Шаурму', '40001,'),)
                          )

if __name__ == '__main__':
    s0 = Dialogs()
    data = s0.step_zero_2
    s0.insert_question(data[0], data[1], data[2])
    for dialog in data[3]:
        s0.insert_dialog(data[0], data[1], dialog)

    pass
