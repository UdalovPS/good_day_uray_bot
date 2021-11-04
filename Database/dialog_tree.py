from posgre_sql import QuestionsTable, DialogsTable, EmojiTable

class DialogTree():
    def __init__(self):
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()
        self.emj = EmojiTable()

    def insert_question_with_sticker(self, step_number, style_id, question, pre_question, sticker):
        self.questions.insert_data_in_table(self.questions.table_name,
                                            self.questions.fields,
                                            f'{step_number, style_id, question, pre_question, sticker}')

    def insert_question(self, step_number, style_id, question, pre_question):
        self.questions.insert_data_in_table(self.questions.table_name,
                                            f"{self.questions.split_fields[0]},"
                                            f"{self.questions.split_fields[1]},"
                                            f"{self.questions.split_fields[2]},"
                                            f"{self.questions.split_fields[3]}",
                                            f'{step_number, style_id, question, pre_question}')

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
        self.style = (0, 0, 'В каком стиле будем вести диалог?', 0, None,
                      (('В стандартном', '12001,', '\U0001F60E'),
                       ('В шуточном', '12002,', '\U0001F600'))
                      )

        self.step_zero_1 = (0, 1, 'Что хотите заказать?', 0,
                            'CAACAgIAAxkBAAEDMehhfrjyA7BGzg0Ozpt7BpKqwSdTiQACsAsAAi8P8Aa7wYsCe5kwfCEE',
                          (('Шаурму', '13001,', '\U0001F32F'),)
                          )
        self.step_zero_2 = (0, 2, 'Чего хочешь отведать, Дорогой?', 0,
                            'CAACAgIAAxkBAAEDMehhfrjyA7BGzg0Ozpt7BpKqwSdTiQACsAsAAi8P8Aa7wYsCe5kwfCEE',
                          (('Шаурму', '13001,', '\U0001F32F'),)
                          )
        self.step_one_1 = (1, 1, 'Какую шаурму желаете?', 0, None,
                          (('Шаурма №1', '13002, 20001', '\U00000031\U000020E3'),
                           ('Шаурма №2', '13002, 20002', '\U00000032\U000020E3'),
                           ('Шаурма №3', '13002, 20003', '\U00000033\U000020E3'),
                           ('Шаурма №4', '13002, 20004', '\U00000034\U000020E3'),
                           ('Шаурма №5/1', '13002, 20051', '\U00000035\U000020E3/\U00000031\U000020E3'),
                           ('Шаурма №5/2', '13002, 20052', '\U00000035\U000020E3/\U00000032\U000020E3'),
                           ('Шаурма №6 вегетерианская', '13002, 20006', '\U00000036\U000020E3'),
                           ('Шаурма №7 с говядиной', '13002, 20007', '\U00000037\U000020E3'),
                           ('Шаурма №8', '13002, 20008', '\U00000038\U000020E3'),
                           ('Шаурма №9 три мяса', '13002, 20009', '\U00000039\U000020E3'))
                          )
        self.step_one_2 = (1, 2, 'Харош!!! Какую именно шавуху ты хочешь?', 0,
                           'CAACAgIAAxkBAAEDMgVhfsPJOWmtndGrEmOiMwhz5z-2HwACBQADvWSZJf4AAYN79D1ZWSEE',
                          (('Шаурма №1', '13002, 20001', '\U00000031\U000020E3'),
                           ('Шаурма №2', '13002, 20002', '\U00000032\U000020E3'),
                           ('Шаурма №3', '13002, 20003', '\U00000033\U000020E3'),
                           ('Шаурма №4', '13002, 20004', '\U00000034\U000020E3'),
                           ('Шаурма №5/1', '13002, 20051', '\U00000035\U000020E3/\U00000031\U000020E3'),
                           ('Шаурма №5/2', '13002, 20052', '\U00000035\U000020E3/\U00000032\U000020E3'),
                           ('Шаурма №6 вегетерианская', '13002, 20006', '\U00000036\U000020E3'),
                           ('Шаурма №7 с говядиной', '13002, 20007', '\U00000037\U000020E3'),
                           ('Шаурма №8', '13002, 20008', '\U00000038\U000020E3'),
                           ('Шаурма №9 три мяса', '13002, 20009', '\U00000039\U000020E3'))
                          )
        self.step_two_1 = (2, 1, 'Состав: ', 1, None,
                           (('Далее', '13003,', '\U000027A1'),)
                           )
        self.step_two_2 = (2, 2, 'Приготовлено из лучших продуктов, состав следующий: ', 1, None,
                           (('Далее', '13003,', '\U000027A1'),)
                           )
        self.step_three_1 = (3, 1, 'Какой соус вам добавить?', 2, None,
                             (('Соус чесночный', '13004, 21001', "\U0001F9C4"),
                              ('Соус томатный', '13004, 21002', "\U0001F345"),
                              ('Соус турецкий(острый)', '13004, 21003', "\U0001F525"),
                              ('Кетчуп+майонез', '13004, 21004', "\U0001F345-\U0001F95A"))
                             )
        self.step_three_2 = (3, 2, 'Отличный выбор. Какой соус добавить?', 2,
                             'CAACAgIAAxkBAAEDM6thgCobIUrcx_D28hXGoFP6E3uqZQACfgIAAladvQpBYnRfUWys5CEE',
                             (('Соус чесночный-антивампирный', '13004, 21001', "\U0001F9C4"),
                              ('Соус Сеньор-помидор', '13004, 21002', "\U0001F345"),
                              ('С турецкий(острый)-АЩЩЩ', '13004, 21003', "\U0001F525"),
                              ('Кечунез!!!', '13004, 21004', "\U0001F345-\U0001F95A"))
                             )
        self.step_four_1 = (4, 1, 'Сколько? Введи нужное количество', 3, None)
        self.step_four_2 = (4, 2, 'Напиши мне сколько тебе нужно, Бери побольшее!', 3,
                            'CAACAgEAAxkBAAEDNJVhgPgwNbxqmb37iaqQpuyomeDS0QACvAgAAr-MkASIew6lsfO_6iEE')
        self.step_five_1 = (5, 1, 'Вы выбрали: ', 4, None,
                            (('Выбрать еще', '13000,', '\U0001F504'),
                             ('Перейти к оформлению заказа', '13006, 35000', '\U0001F4CB'))
                            )
        self.step_five_2 = (5, 2, 'Из того, что пожевать выбрано следующее: ', 4, None,
                            (('Выбрать еще', '13000,', '\U0001F504'),
                             ('Готовьте давайте уже, есть хочу', '13006, 35000', '\U0001F4CB'))
                            )
        self.step_six_1 = (6, 1, 'Напишите как к Вам можно обращаться', 5, None)
        self.step_six_2 = (6, 2, 'Напиши как к тебе обращаться. Только давай что-нибудь оригинальное', 5,
                           'CAACAgIAAxkBAAEDNb5hgZBL6Y55hd4fhIzRSSSK0rYU7wAChgkAAnlc4gmdEYTQ68fNZSEE')
        self.step_seven_1 = (7, 1, 'Введите номер телефона по которому с вами можно связаться \U0001F4DE', 6, None)
        self.step_seven_2 = (7, 2, 'Введи номер по которому до тебя можно будет дозвонится \U0001F4DE', 6,
                             'CAACAgIAAxkBAAEDN8hhg9GAw5Q3WWodVwMhVeoLGY3iPQACTgADR_sJDOfEDC5QwsglIQQ')
        self.step_eight_1 = (8, 1, 'Оформить доставку или заберете сами?', 7, None,
                             (('Да, оформить', '13009, 32002', '\U0001F44C'),
                              ('Нет, заберу сам', '13010, 32001', '\U0001F4AA'))
                             )
        self.step_eight_2 = (8, 2, 'Еду привезти? Или сам заберешь?', 7,
                             'CAACAgIAAxkBAAEDN85hg9MSFkivvfzTOitPOw0-EeHZ9wACLgIAAzigCqUQt82uLEElIQQ',
                             (('Привези, братуха', '13009, 32002', '\U0001F44C'),
                              ('Сам заберу', '13010, 32001', '\U0001F4AA'))
                             )
        self.step_nine_1 = (9, 1, 'Напишите адрес доставки. Стоимость доставки 150 рублей. '
                                  'При заказе от 1000 рублей доставка бесплатно', 8, None)
        self.step_nine_2 = (9, 2, 'Куда привезти? Прибуду быстро, как ракета. Это будет стоить стоить 150 рублей, '
                                  'но если закажешь на 1000 или больше - то привезу бесплатно', 8,
                            'CAACAgIAAxkBAAEDN8phg9L3V3JlHBUmjGprO8y6c_JlFAACDwIAAzigCloKUtCsAvOdIQQ')
        self.step_ten_1 = (10, 1, 'Напишите к какому времени подготовить заказ? \U0001F550', 8, None)
        self.step_ten_2 = (10, 2, 'Напиши во сколько тебя ждать, братишка? \U0001F550', 8,
                           'CAACAgIAAxkBAAEDN9Bhg9OsunJu4SpHYH-rGKO9ICZUDwACkAIAAladvQoy0qlxuNTQtSEE')
        self.step_eleven_1 = (11, 1, 'У вас на счету ', 10, None,
                              (('Да', '13012, 51000', '\U0001F44C'),
                               ('Нет', '13012, 37000', '\U0000270B'))
                              )
        self.step_eleven_2 = (11, 2, 'У тебя на счету ', 10, None,
                              (('Да', '13012, 51000', '\U0001F44C'),
                               ('Нет', '13012, 37000', '\U0000270B'))
                              )
        self.step_twelve_1 = (12, 1, '', 11, None,
                              (('Завершить заказ', 'end', '\U00002705'),)
                              )
        self.step_twelve_2 = (12, 2, '', 11, None,
                              (('Завершить заказ', 'end', '\U00002705'),)
                              )

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
    data = s0.step_ten_2
    # if data[4] == None:
    #     s0.insert_question(data[0], data[1], data[2], data[3])
    # else:
    #     s0.insert_question_with_sticker(data[0], data[1], data[2], data[3], data[4])
    # for dialog in data[5]:
    #     if len(dialog) > 2:
    #         s0.insert_dialogs_with_emoji(data[0], data[1], dialog)
    #     else:
    #         s0.insert_dialog(data[0], data[1], dialog)
    pass
