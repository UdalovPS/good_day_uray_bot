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
        self.question = '?? ?????????? ?????????? ?????????? ?????????? ?????????????'
        self.choice_dialogs = ((self.step_number, 0, '?? ??????????????????????', '10001,'),
                       (self.step_number, 0, '?????? ??????!', '10002,'))



class FirstStep(DialogTree):
    def __init__(self):
        super().__init__()
        self.step_number = 1
        self.style_id = 1
        self.question = '?????? ???????????? ?????????????????'
        self.choice_dialogs = ((self.step_number, self.style_id, '???????????? ???1', 11, 1),
                               (self.step_number, self.style_id, '???????????? ???2', 12, 1),
                               (self.step_number, self.style_id, '???????????? ???3', 13, 1))

class Dialogs(DialogTree):
    def __init__(self):
        super(Dialogs, self).__init__()
        """(step, style, question, previous step, sticker) 
            (dialog, commands, emoji IF EXISTS)"""
        self.style = (0, 0, '?? ?????????? ?????????? ?????????? ?????????? ?????????????', 0, None,
                      (('?? ??????????????????????', '12001,', '\U0001F60E'),
                       ('?? ????????????????', '12002,', '\U0001F600'))
                      )

        self.step_zero_1 = (0, 1, '?????? ???????????? ?????????????????', 0,
                            'CAACAgIAAxkBAAEDMehhfrjyA7BGzg0Ozpt7BpKqwSdTiQACsAsAAi8P8Aa7wYsCe5kwfCEE',
                          (('????????????', '13001,', '\U0001F32F'),)
                          )
        self.step_zero_2 = (0, 2, '???????? ???????????? ????????????????, ???????????????', 0,
                            'CAACAgIAAxkBAAEDMehhfrjyA7BGzg0Ozpt7BpKqwSdTiQACsAsAAi8P8Aa7wYsCe5kwfCEE',
                          (('????????????', '13001,', '\U0001F32F'),)
                          )
        self.step_one_1 = (1, 1, '?????????? ???????????? ???????????????', 0, None,
                          (('???????????? ???1', '13002, 20001', '\U00000031\U000020E3'),
                           ('???????????? ???2', '13002, 20002', '\U00000032\U000020E3'),
                           ('???????????? ???3', '13002, 20003', '\U00000033\U000020E3'),
                           ('???????????? ???4', '13002, 20004', '\U00000034\U000020E3'),
                           ('???????????? ???5/1', '13002, 20051', '\U00000035\U000020E3/\U00000031\U000020E3'),
                           ('???????????? ???5/2', '13002, 20052', '\U00000035\U000020E3/\U00000032\U000020E3'),
                           ('???????????? ???6 ????????????????????????????', '13002, 20006', '\U00000036\U000020E3'),
                           ('???????????? ???7 ?? ??????????????????', '13002, 20007', '\U00000037\U000020E3'),
                           ('???????????? ???8', '13002, 20008', '\U00000038\U000020E3'),
                           ('???????????? ???9 ?????? ????????', '13002, 20009', '\U00000039\U000020E3'))
                          )
        self.step_one_2 = (1, 2, '??????????!!! ?????????? ???????????? ???????????? ???? ?????????????', 0,
                           'CAACAgIAAxkBAAEDMgVhfsPJOWmtndGrEmOiMwhz5z-2HwACBQADvWSZJf4AAYN79D1ZWSEE',
                          (('???????????? ???1', '13002, 20001', '\U00000031\U000020E3'),
                           ('???????????? ???2', '13002, 20002', '\U00000032\U000020E3'),
                           ('???????????? ???3', '13002, 20003', '\U00000033\U000020E3'),
                           ('???????????? ???4', '13002, 20004', '\U00000034\U000020E3'),
                           ('???????????? ???5/1', '13002, 20051', '\U00000035\U000020E3/\U00000031\U000020E3'),
                           ('???????????? ???5/2', '13002, 20052', '\U00000035\U000020E3/\U00000032\U000020E3'),
                           ('???????????? ???6 ????????????????????????????', '13002, 20006', '\U00000036\U000020E3'),
                           ('???????????? ???7 ?? ??????????????????', '13002, 20007', '\U00000037\U000020E3'),
                           ('???????????? ???8', '13002, 20008', '\U00000038\U000020E3'),
                           ('???????????? ???9 ?????? ????????', '13002, 20009', '\U00000039\U000020E3'))
                          )
        self.step_two_1 = (2, 1, '????????????: ', 1, None,
                           (('??????????', '13003,', '\U000027A1'),)
                           )
        self.step_two_2 = (2, 2, '???????????????????????? ???? ???????????? ??????????????????, ???????????? ??????????????????: ', 1, None,
                           (('??????????', '13003,', '\U000027A1'),)
                           )
        self.step_three_1 = (3, 1, '?????????? ???????? ?????? ?????????????????', 2, None,
                             (('???????? ??????????????????', '13004, 21001', "\U0001F9C4"),
                              ('???????? ????????????????', '13004, 21002', "\U0001F345"),
                              ('???????? ????????????????(????????????)', '13004, 21003', "\U0001F525"),
                              ('????????????+??????????????', '13004, 21004', "\U0001F345-\U0001F95A"))
                             )
        self.step_three_2 = (3, 2, '???????????????? ??????????. ?????????? ???????? ?????????????????', 2,
                             'CAACAgIAAxkBAAEDM6thgCobIUrcx_D28hXGoFP6E3uqZQACfgIAAladvQpBYnRfUWys5CEE',
                             (('???????? ??????????????????-??????????????????????????', '13004, 21001', "\U0001F9C4"),
                              ('???????? ????????????-??????????????', '13004, 21002', "\U0001F345"),
                              ('???????? ????????????????(????????????)-????????', '13004, 21003', "\U0001F525"),
                              ('??????????????!!!', '13004, 21004', "\U0001F345-\U0001F95A"))
                             )
        self.step_four_1 = (4, 1, '??????????????? ?????????? ???????????? ????????????????????', 3, None)
        self.step_four_2 = (4, 2, '???????????? ?????? ?????????????? ???????? ??????????, ???????? ??????????????????!', 3,
                            'CAACAgEAAxkBAAEDNJVhgPgwNbxqmb37iaqQpuyomeDS0QACvAgAAr-MkASIew6lsfO_6iEE')
        self.step_five_1 = (5, 1, '???? ??????????????: ', 4, None,
                            (('?????????????? ??????', '13000,', '\U0001F504'),
                             ('?????????????? ?? ???????????????????? ????????????', '13006, 35000', '\U0001F4CB'))
                            )
        self.step_five_2 = (5, 2, '???? ????????, ?????? ???????????????? ?????????????? ??????????????????: ', 4, None,
                            (('?????????????? ??????', '13000,', '\U0001F504'),
                             ('???????????????? ?????????????? ??????, ???????? ????????', '13006, 35000', '\U0001F4CB'))
                            )
        self.step_six_1 = (6, 1, '???????????????? ?????? ?? ?????? ?????????? ????????????????????', 5, None)
        self.step_six_2 = (6, 2, '???????????? ?????? ?? ???????? ????????????????????. ???????????? ?????????? ??????-???????????? ????????????????????????', 5,
                           'CAACAgIAAxkBAAEDNb5hgZBL6Y55hd4fhIzRSSSK0rYU7wAChgkAAnlc4gmdEYTQ68fNZSEE')
        self.step_seven_1 = (7, 1, '?????????????? ?????????? ???????????????? ???? ???????????????? ?? ???????? ?????????? ?????????????????? \U0001F4DE', 6, None)
        self.step_seven_2 = (7, 2, '?????????? ?????????? ???? ???????????????? ???? ???????? ?????????? ?????????? ???????????????????? \U0001F4DE', 6,
                             'CAACAgIAAxkBAAEDN8hhg9GAw5Q3WWodVwMhVeoLGY3iPQACTgADR_sJDOfEDC5QwsglIQQ')
        self.step_eight_1 = (8, 1, '???????????????? ???????????????? ?????? ???????????????? ?????????', 7, None,
                             (('????, ????????????????', '13009, 32002', '\U0001F44C'),
                              ('??????, ???????????? ??????', '13010, 32001', '\U0001F4AA'))
                             )
        self.step_eight_2 = (8, 2, '?????? ????????????????? ?????? ?????? ?????????????????', 7,
                             'CAACAgIAAxkBAAEDN85hg9MSFkivvfzTOitPOw0-EeHZ9wACLgIAAzigCqUQt82uLEElIQQ',
                             (('??????????????, ??????????????', '13009, 32002', '\U0001F44C'),
                              ('?????? ????????????', '13010, 32001', '\U0001F4AA'))
                             )
        self.step_nine_1 = (9, 1, '???????????????? ?????????? ????????????????. ?????????????????? ???????????????? 150 ????????????. '
                                  '?????? ???????????? ???? 1000 ???????????? ???????????????? ??????????????????', 8, None)
        self.step_nine_2 = (9, 2, '???????? ????????????????? ?????????????? ????????????, ?????? ????????????. ?????? ?????????? ???????????? ???????????? 150 ????????????, '
                                  '???? ???????? ???????????????? ???? 1000 ?????? ???????????? - ???? ?????????????? ??????????????????', 8,
                            'CAACAgIAAxkBAAEDN8phg9L3V3JlHBUmjGprO8y6c_JlFAACDwIAAzigCloKUtCsAvOdIQQ')
        self.step_ten_1 = (10, 1, '???????????????? ?? ???????????? ?????????????? ?????????????????????? ??????????? \U0001F550', 8, None)
        self.step_ten_2 = (10, 2, '???????????? ???? ?????????????? ???????? ??????????, ????????????????? \U0001F550', 8,
                           'CAACAgIAAxkBAAEDN9Bhg9OsunJu4SpHYH-rGKO9ICZUDwACkAIAAladvQoy0qlxuNTQtSEE')
        self.step_eleven_1 = (11, 1, '?? ?????? ???? ?????????? ', 10, None,
                              (('????', '13012, 51000', '\U0001F44C'),
                               ('??????', '13012, 37000', '\U0000270B'))
                              )
        self.step_eleven_2 = (11, 2, '?? ???????? ???? ?????????? ', 10, None,
                              (('????', '13012, 51000', '\U0001F44C'),
                               ('??????', '13012, 37000', '\U0000270B'))
                              )
        self.step_twelve_1 = (12, 1, '', 11, None,
                              (('?????????????????? ??????????', 'end', '\U00002705'),)
                              )
        self.step_twelve_2 = (12, 2, '', 11, None,
                              (('?????????????????? ??????????', 'end', '\U00002705'),)
                              )

        self.step_status = (500, 0, '?????????????? ?????????? ????????????', 0, None,
                            (('????????????????', 'cancel', '\U0000274C'),)
                            )
        self.step_cancel = (600, 0, '?????????????? ?????????? ????????????', 0, None,
                            (('????????????????', 'cancel', '\U0000274C'),)
                            )

class AdminDialogs(DialogTree):
    def __init__(self):
        super(AdminDialogs, self).__init__()
        self.start_admin_step = (900, 0, '?????????????? ?????? ??????????????', 0, None)
        self.first_admin_msg = (901, 0, '???????????? ??????????????????????. ???????????????? ??????????????', 900, None,
                                (('???????????????????? ????????????????', '13910,'),
                                ('???????????????????? ??????????????????', '13940,'))
                                )
        self.choice_cart_status = (910, 0, '?????????????? ?????????? ????????????', 901, None)
        self.update_cart_status = (920, 0, '', 910, None,
                                   (('?????????? ????????????', '13930, 91002'),
                                    ('?????????? ?????????? ?? ????????????', '13930, 91003'),
                                    ('?????????? ????????????????????????', '13930, 91004'),
                                    ('?????????? ????????????????', '13930, 91005, 92000'),
                                    ('?????????? ??????????????', '13930, 91011'))
                                   )
        self.state_is_changed = (930, 0, '???????????? ???????????? ??????????????', 920, None)
        self.choice_customer_cmd = (940, 0, '?????????????? ?????????????????????????????????? ?????????? ??????????????', 901, None)
        self.change_customer_data = (941, 0, '', 940, None,
                                     (('???????????????? ?? ???????????? ????????????', '13942, 94002'),
                                      ('?????????????? ???? ?????????????? ????????????', '13942, 94001'),
                                      ('???????????????? ???????????????????????? ????????????', '13943,'))
                                     )
        self.state_personal_data = (942, 0, '???????????? ???????????????????????? ????????????????', 941, None)
        self.personal_scores_data = (943, 0, '?????????????? ?????????? ???????????????????????? ????????????', 941, None)

if __name__ == '__main__':
    s0 = Dialogs()
    # s0 = AdminDialogs()
    data = s0.step_three_2
    # if data[4] == None:
    #     s0.insert_question(data[0], data[1], data[2], data[3])
    # else:
    #     s0.insert_question_with_sticker(data[0], data[1], data[2], data[3], data[4])
    for dialog in data[5]:
        if len(dialog) > 2:
            s0.insert_dialogs_with_emoji(data[0], data[1], dialog)
        else:
            s0.insert_dialog(data[0], data[1], dialog)
    pass
