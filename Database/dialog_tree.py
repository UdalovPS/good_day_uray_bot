from posgre_sql import QuestionsTable, DialogsTable, EmojiTable

class DialogTree():
    def __init__(self):
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()
        self.emj = EmojiTable()

    def insert_question(self, step_number, style_id, question, pre_question, sticker):
        self.questions.insert_data_in_table(self.questions.table_name,
                                            self.questions.fields,
                                            f'{step_number, style_id, question, pre_question, sticker}')

    def insert_dialog(self, step, style, dialog):
        self.dialogs.insert_data_in_table(self.dialogs.table_name,
                                          f'{self.dialogs.split_fields[0]},'
                                          f'{self.dialogs.split_fields[1]},'
                                          f'{self.dialogs.split_fields[2]},'
                                          f'{self.dialogs.split_fields[3]}',
                                          f"({step}, {style}, '{dialog[0]}', "
                                          f"'{dialog[1]}')")

    def insert_dialogs_with_emoji(self, step, style, dialog):
        self.dialogs.insert_data_in_table(self.dialogs.table_name,
                                      self.dialogs.fields,
                                      f"({step}, {style}, '{dialog[0]}',"
                                      f"'{dialog[1]}', '{dialog[2]}')")

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
        """(step, style, question, previous step, sticker) 
            (dialog, commands, emoji IF EXISTS)"""
        self.style = (0, 0, 'В каком стиле будем вести диалог?', 0, 'sticker',
                      (('В стандартном', '12001,', '\U0001F60E'),
                       ('В шуточном', '12002,', '\U0001F600'))
                      )

        self.step_zero_1 = (0, 1, 'Что хотите заказать?', 0, 'sticker',
                          (('Шаурму', '13001,', '\U0001F32F'),)
                          )
        self.step_zero_2 = (0, 2, 'Что будешь хавать?', 0, 'sticker',
                          (('Шаурму', '13001,', '\U0001F32F'),)
                          )
        self.step_one_1 = (1, 1, 'Какую шаурму желаете?', 0,
                          (('Шаурма №1', '40002, 70001', ':one:'),
                           ('Шаурма №2', '40002, 70002', ':two:'),
                           ('Шаурма №3', '40002, 70003', ':three:'),
                           ('Шаурма №4', '40002, 70004', ':one:'),
                           ('Шаурма №5/1', '40002, 70051', ':two:'),
                           ('Шаурма №5/2', '40002, 70052', ':three:'),
                           ('Шаурма №6 вегетерианская', '40002, 70006', ':three:'),
                           ('Шаурма №7 с говядиной', '40002, 70007', ':one:'),
                           ('Шаурма №8', '40002, 70008', ':two:'),
                           ('Шаурма №9 три мяса', '40002, 70009', ':three:'))
                          )
        self.step_one_2 = (1, 2, 'Харош!!! Вкуснее шаурмы ничего нет на свете. Какую тебе?', 0,
                          (('Шаурма №1', '40002, 70001', ':one:'),
                           ('Шаурма №2', '40002, 70002', ':two:'),
                           ('Шаурма №3', '40002, 70003', ':three:'),
                           ('Шаурма №4', '40002, 70004', ':one:'),
                           ('Шаурма №5/1', '40002, 70051', ':two:'),
                           ('Шаурма №5/2', '40002, 70052', ':three:'),
                           ('Шаурма №6 вегетерианская', '40002, 70006', ':three:'),
                           ('Шаурма №7 с говядиной', '40002, 70007', ':one:'),
                           ('Шаурма №8', '40002, 70008', ':two:'),
                           ('Шаурма №9 три мяса', '40002, 70009', ':three:'))
                          )
        self.step_two_1 = (2, 1, 'Состав: ', 1,
                           (('Далее', '40003,'),)
                           )
        self.step_two_2 = (2, 2, 'Приготовлено из лучших продуктов, состав следующий: ', 1,
                           (('Далее', '40003,'),)
                           )
        self.step_three_1 = (3, 1, 'Какой соус вам добавить?', 2,
                             (('Чесночный', '40004, 71001'),
                              ('Томатный', '40004, 71002'),
                              ('Турецкий(острый)', '40004, 71003'),
                              ('Кетчуп+майонез', '40004, 71004'))
                             )
        self.step_three_2 = (3, 2, 'Хороший выбор, уважаю. Осталось выбрать соус?', 2,
                             (('Чесночный-антивампирный', '40004, 71001'),
                              ('Сеньор-помидор', '40004, 71002'),
                              ('Турецкий(острый)-АЩЩЩ', '40004, 71003'),
                              ('Кечунез!!!', '40004, 71004'))
                             )
        self.step_four_1 = (4, 1, 'Сколько? Введи нужное количество', 3)
        self.step_four_2 = (4, 2, 'Напиши мне сколько тебе нужно', 3)
        self.step_five_1 = (5, 1, 'Вы выбрали: ', 4,
                            (('Выбрать еще', '40000,'),
                             ('Перейти к оформлению заказа', '40006,'))
                            )
        self.step_five_2 = (5, 2, 'Из того, что пожевать выбрано следующее: ', 4,
                            (('Выбрать еще', '40000,'),
                             ('Готовьте давайте уже, есть хочу', '40006,'))
                            )
        self.step_six_1 = (6, 1, 'Напишите как к Вам можно обращаться', 5)
        self.step_six_2 = (6, 2, 'Напиши как тебя зовут, Братуха!', 5)
        self.step_seven_1 = (7, 1, 'Введите номер телефона по которому с вами можно связаться', 6)
        self.step_seven_2 = (7, 2, 'Введи номер по которому до тебя можно будет дозвонится', 6)
        self.step_eight_1 = (8, 1, 'Оформить доставку или заберете сами?', 7,
                             (('Да, оформить', '40009, 61002'),
                              ('Нет, заберу сам', '40010, 61001'))
                             )
        self.step_eight_2 = (8, 2, 'Еду привезти? Или сам заберешь?', 7,
                             (('Привези, братуха', '40009, 61002'),
                              ('Сам заберу', '40010, 61001'))
                             )
        self.step_nine_1 = (9, 1, 'Напишите адрес доставки', 8)
        self.step_nine_2 = (9, 2, 'Куда привезти? Прибуду быстро, как ракета', 8)
        self.step_ten_1 = (10, 1, 'Напишите к какому времени подготовить заказ?', 9)
        self.step_ten_2 = (10, 2, 'Напиши во сколько тебя ждать, братишка?', 9)


class AdminDialogs(DialogTree):
    def __init__(self):
        super(AdminDialogs, self).__init__()
        self.start_admin_step = (900, 0, 'Введите код доступа', 0)
        self.first_admin_msg = (901, 0, 'Доступ подтвержден. Выберите команду', 900,
                                (('Управление заказами', '40910,'),
                                ('Управление черным списком', '40920,'),
                                ('Управление скидками', '40930,'))
                                )
        self.choice_cart_status = (910, 0, 'Введите номер заказа', 901)
        self.update_cart_status = (911, 0, '', 910,
                                   (('Заказ принят', '40912, 93002'),
                                    ('Заказ готов к выдаче', '40912, 93003'),
                                    ('Заказ доставляется', '40912, 93004'),
                                    ('Заказ завершен', '40912, 93005'),
                                    ('Заказ отменен', '40912, 93010'))
                                   )
        self.state_is_changed = (912, 0, 'Статус заказа изменен', 911)

if __name__ == '__main__':
    s0 = Dialogs()
    # s0 = AdminDialogs()
    data = s0.step_zero_2
    # s0.insert_question(data[0], data[1], data[2], data[3], data[4])
    # for dialog in data[5]:
    #     if len(dialog) > 2:
    #         s0.insert_dialogs_with_emoji(data[0], data[1], dialog)
    #     else:
    #         s0.insert_dialog(data[0], data[1], dialog)
    pass
