from posgre_sql import QuestionsTable, DialogsTable, EmojiTable

class DialogTree():
    def __init__(self):
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()
        self.emj = EmojiTable()

    def insert_question(self, step_number, style_id, question, pre_question):
        self.questions.insert_data_in_table(self.questions.table_name,
                                            self.questions.fields,
                                            f'{step_number, style_id, question, pre_question}')

    def insert_dialog(self, step, style, dialog):
        self.dialogs.insert_data_in_table(self.dialogs.table_name,
                                          self.dialogs.fields,
                                          f"({step}, {style}, '{dialog[0]}', "
                                          f"'{dialog[1]}')")

    def insert_emoji(self, step, style, emoji):
        self.emj.insert_data_in_table(self.emj.table_name,
                                      self.emj.fields,
                                      f"({step}, {style}, '{emoji}')")

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
        """(step, style, question, previous step) 
            (dialog, commands, emoji IF EXISTS)"""
        self.style = (0, 0, 'В каком стиле будем вести диалог?', 0,
                      (('В стандартном', '10001,'), ('Как БРО!', '10002,')))

        self.step_zero_1 = (0, 1, 'Что хотите заказать?', 0,
                          (('Шаурму', '40001,', ':burrito:'),)
                          )
        self.step_zero_2 = (0, 2, 'Что будешь хавать?', 0,
                          (('Шаурму', '40001,', ':burrito:'),)
                          )
        self.step_one_1 = (1, 1, 'Какую шаурму желаете?', 0,
                          (('Шаурма №1', '40002, 70001', ':one:'),
                           ('Шаурма №2', '40002, 70002', ':two:'),
                           ('Шаурма №3', '40002, 70003', ':three:'))
                          )
        self.step_one_2 = (1, 2, 'Харош!!! Вкуснее шаурмы ничего нет на свете. Какую тебе?', 0,
                          (('Шаурма №1', '40002, 70001', ':one:'),
                           ('Шаурма №2', '40002, 70002', ':two:'),
                           ('Шаурма №3', '40002, 70003', ':three:'))
                          )

if __name__ == '__main__':
    s0 = Dialogs()
    data = s0.step_one_2
    # s0.insert_question(data[0], data[1], data[2], data[3])
    # for dialog in data[4]:
    #     s0.insert_dialog(data[0], data[1], dialog)
    #     if len(dialog) > 2:
    #         s0.insert_emoji(data[0], data[1], dialog[2])

    pass
