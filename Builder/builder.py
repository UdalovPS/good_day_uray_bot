from abc import ABC, abstractmethod
from new_command_handler import CommandHandler
from new_data_selector import SelectorDataDb
from former_data_about_cart import DataCartFormer

class DataForMessage:
    def __init__(self, chat_id, question, dialogs_list) -> None:
        self.chat_id = chat_id
        self.question = question
        self.dialogs_list = dialogs_list


class Question:
    def __init__(self, question=None, sticker=None, pre_answer=None, sticker_id=None) -> None:
        self.quest = question
        self.sticker = sticker
        self.pre_answer = pre_answer
        self.sticker_msg_id = sticker_id


class DialogsList:
    def __init__(self) -> None:
        self.dialogs_list = []

    def add_obj_in_list(self, obj) -> None:
        self.dialogs_list.append(obj)


class Dialogs:
    def __init__(self, dialog: str, commands: str, emoji=None):
        self.dialog = dialog
        self.commands = commands
        self.emoji = emoji


class DataCreator(ABC):
    @abstractmethod
    def build_chat_id(self) -> None:
        pass

    @abstractmethod
    def build_question(self) -> None:
        pass

    @abstractmethod
    def build_dialog_list(self) -> None:
        pass

    @abstractmethod
    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        pass

    @abstractmethod
    def create_data_for_message(self) -> None:
        pass


class StandartDataForMessage(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        data = db.select_question_from_db()[0]
        stiker_id = db.select_sticker_id_from_db()
        return Question(*data, sticker_id=stiker_id)

    def build_dialog_list(self) -> DialogsList:
        data = SelectorDataDb(self.message)
        data_dialogs = data.select_dialog_from_db()
        style_id = data.select_style_id_from_db()
        step_id = data.select_step_id_from_db()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data_dialogs)
        if style_id == 0 or step_id == 4 or step_id == 5 or step_id == 6 or step_id == 7 or step_id == 9 or step_id == 10:
            pass
        else:
            self.add_objects_in_dialog_list(dialogs, [('Назад', 'back', '\U0001F519')])
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class BlackListData(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        quest = f"Извините, но вы находитесь в черном списке. За подробностями позвоните по телефону\n" \
                f"Ваш уникальный номер: <strong>{self.message.chat.id}</strong>"
        return Question(quest)

    def build_dialog_list(self) -> DialogsList:
        data = ()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data)
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class PreviousQuestionInlineBtn(DataCreator):
    def __init__(self, call):
        self.call = call

    def build_chat_id(self) -> int:
        return self.call.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.call.message)
        data = db.select_question_from_db()[0]
        return Question(*data)

    def build_dialog_list(self) -> DialogsList:
        data = ()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data)
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class PreviousQuestionToTextMessage(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        data = db.select_question_from_db()[0]
        return Question(*data)

    def build_dialog_list(self) -> DialogsList:
        data = ()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data)
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class PreviousInlineButtonAnswer(DataCreator):
    def __init__(self, call):
        self.call = call

    def build_chat_id(self) -> int:
        return self.call.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.call.message)
        pre_step_id = db.select_pre_question_id()
        step_id = db.select_step_id_from_db()
        if pre_step_id == 0 and step_id == 0:
            pre_btn_customer_answer = db.select_pre_step_dialog(pre_step_id, self.call.data, 0)
        else:
            pre_btn_customer_answer = db.select_pre_step_dialog(pre_step_id, self.call.data)
        return Question(pre_answer=pre_btn_customer_answer)

    def build_dialog_list(self) -> DialogsList:
        data = ()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data)
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class ProductDescriptionMessage(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        prod_price = db.select_description_and_price_product()
        data = f"<strong>Состав:</strong>\n{prod_price[0]}\n<strong>Цена:</strong> <u>{prod_price[1]} рублей</u>"
        stiker_id = db.select_sticker_id_from_db()
        return Question(data, sticker_id=stiker_id)

    def build_dialog_list(self) -> DialogsList:
        data = SelectorDataDb(self.message)
        data_dialogs = data.select_dialog_from_db()
        style_id = data.select_style_id_from_db()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data_dialogs)
        if style_id != 0:
            self.add_objects_in_dialog_list(dialogs, [('Назад', 'back', '\U0001F519')])
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class ListOfSousesForChoice(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        prod_price = db.select_description_and_price_product()
        data = f"<strong>Состав:</strong>\n{prod_price[0]}\n<strong>Цена:</strong> <u>{prod_price[1]} рублей</u>"
        stiker_id = db.select_sticker_id_from_db()
        return Question(data, sticker_id=stiker_id)

    def build_dialog_list(self) -> DialogsList:
        data = SelectorDataDb(self.message)
        data_dialogs = data.select_dialog_from_db()
        style_id = data.select_style_id_from_db()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data_dialogs)
        if style_id != 0:
            self.add_objects_in_dialog_list(dialogs, [('Назад', 'back', '\U0001F519')])
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class IntermediateDataCart(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        list_data = db.select_intermediate_data_about_cart()
        data = f'Заказ: \n'
        money_sum = 0
        for item in list_data:
            data += f'1){item[0]}\n'
            data += f'2){item[1]}\n'
            data += f'3)Количество: {item[2]}\n'
            data += f'4)Сумма: {item[3]} рублей\n'
            data += '........................................\n'
            money_sum += item[3]
        data += f'Итоговая сумма: {money_sum} рублей\n'
        stiker_id = db.select_sticker_id_from_db()
        return Question(data, sticker_id=stiker_id)

    def build_dialog_list(self) -> DialogsList:
        data = SelectorDataDb(self.message)
        data_dialogs = data.select_dialog_from_db()
        style_id = data.select_style_id_from_db()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data_dialogs)
        if style_id != 0:
            self.add_objects_in_dialog_list(dialogs, [('Назад', 'back', '\U0001F519')])
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class CartDataForCustomer(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        list_data_db = db.select_intermediate_data_about_cart()
        customer_cart_data_db = db.select_data_about_customer_and_about_cart()
        cart_status = db.select_status_description(customer_cart_data_db[7])
        final_data = DataCartFormer().data_for_customer_about_cart([customer_cart_data_db, list_data_db],
                                                                   'Выбрано:', status=cart_status)
        price_before_scores = db.select_price_before_scores()
        data = final_data + f'Итоговая сумма: {price_before_scores} рублей\n'
        stiker_id = db.select_sticker_id_from_db()
        return Question(data, sticker_id=stiker_id)

    def build_dialog_list(self) -> DialogsList:
        data = SelectorDataDb(self.message)
        data_dialogs = data.select_dialog_from_db()
        style_id = data.select_style_id_from_db()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data_dialogs)
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class DataAboutCustomerScores(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        scores = db.select_personal_scores(self.message.chat.id)
        if scores != 0:
            data = db.select_question_from_db()[0]
            quest = data[0] + f"{scores} баллов. Хотите их потратить?"
            stiker_id = db.select_sticker_id_from_db()
            return Question(quest, sticker_id=stiker_id)
        else:
            CommandHandler('13012,', self.message)
            list_data_db = db.select_intermediate_data_about_cart()
            customer_cart_data_db = db.select_data_about_customer_and_about_cart()
            cart_status = db.select_status_description(customer_cart_data_db[7])
            final_data = DataCartFormer().data_for_customer_about_cart([customer_cart_data_db, list_data_db],
                                                                       'Выбрано:', status=cart_status)
            price_before_scores = db.select_price_before_scores()
            data = final_data + f'Итоговая сумма: {price_before_scores} рублей\n'
            stiker_id = db.select_sticker_id_from_db()
            return Question(data, sticker_id=stiker_id)

    def build_dialog_list(self) -> DialogsList:
        data = SelectorDataDb(self.message)
        data_dialogs = data.select_dialog_from_db()
        style_id = data.select_style_id_from_db()
        step_id = data.select_step_id_from_db()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data_dialogs)
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class FinalDataAboutCustomerScores(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        list_data_db = db.select_intermediate_data_about_cart()
        customer_cart_data_db = db.select_data_about_customer_and_about_cart()
        cart_status = db.select_status_description(customer_cart_data_db[7])
        final_data = DataCartFormer().data_for_customer_about_cart([customer_cart_data_db, list_data_db],
                                                                   'Выбрано:', status=cart_status)
        price_before_scores = db.select_price_before_scores()
        data = final_data + f'Итоговая сумма: {price_before_scores} рублей\n'
        stiker_id = db.select_sticker_id_from_db()
        return Question(data, sticker_id=stiker_id)

    def build_dialog_list(self) -> DialogsList:
        data = SelectorDataDb(self.message)
        data_dialogs = data.select_dialog_from_db()
        style_id = data.select_style_id_from_db()
        dialogs = DialogsList()
        self.add_objects_in_dialog_list(dialogs, data_dialogs)
        return dialogs

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)

    def create_data_for_message(self):
        chat_id = self.build_chat_id()
        quest = self.build_question()
        dialogs = self.build_dialog_list()
        return DataForMessage(chat_id, quest, dialogs)


class AnswerFactory:
    def answer_to_start_command(self, message):
        """ /start command"""
        black_list = SelectorDataDb(message).check_black_list_about_customer()
        if black_list:
            if black_list == 2:
                data = BlackListData(message).create_data_for_message()
            else:
                CommandHandler('10000, 11000, 30000, 31000', message)
                data = StandartDataForMessage(message).create_data_for_message()
        else:
            CommandHandler('40000, 10000, 11000, 30000, 31000, 50000', message)
            data = StandartDataForMessage(message).create_data_for_message()
        return data

    def answer_to_inline_commands(self, call):
        """answer to not concrete inline commands
            :return - DataForMessage object"""
        CommandHandler(call.data, call.message)
        cod_list = call.data.split(', ')
        if (int(cod_list[0][0:5])) % 1000 == 12:
            data = CartDataForCustomer(call.message).create_data_for_message()
            return data

        if len(cod_list) > 1:
            if (int(cod_list[1]) // 1000) == 20:
                data = ProductDescriptionMessage(call.message).create_data_for_message()
            else:
                data = StandartDataForMessage(call.message).create_data_for_message()
        else:
            data = StandartDataForMessage(call.message).create_data_for_message()
        return data

    def answer_to_back_inline_commands(self, call):
        """:return - DataForMessage object"""
        CommandHandler('14000,', call.message)
        step_id = SelectorDataDb(call.message).select_step_id_from_db()
        if step_id == 5:
            data = IntermediateDataCart(call.message).create_data_for_message()
        else:
            data = StandartDataForMessage(call.message).create_data_for_message()
        return data

    def pre_question_in_dialog(self, call):
        """:return - previous question in dialog for bot.send_message method"""
        data = PreviousQuestionInlineBtn(call).create_data_for_message()
        return data

    def pre_question_in_text_message(self, message):
        """:return - previous question in dialog for bot.send_message method"""
        data = PreviousQuestionToTextMessage(message).create_data_for_message()
        return data

    def pre_inline_btn_customer_answer(self, call):
        """:return - text previous press button"""
        data = PreviousInlineButtonAnswer(call).create_data_for_message()
        return data

    def update_sticker_id_in_step_table(self, sticker):
        """This method update now sticker_message_id in step_table"""
        CommandHandler('15000,', sticker)

    def delete_sticker_id_in_step_table(self, message):
        """This method delete previous sticker_message_id from step_table"""
        CommandHandler('16000,', message)


    def choice_answer_to_text_message(self, message):
        """:return - answer to text message"""
        step_id = SelectorDataDb(message).select_step_id_from_db()
        if step_id == 4:
            return self.answer_to_count_product_message(message)
        if step_id == 6:
            return self.answer_to_customer_name_message(message)
        if step_id == 7:
            return self.answer_to_customer_phone_message(message)
        if step_id == 9:
            return self.answer_to_delivery_address_message(message)
        if step_id == 10:
            return self.answer_to_customer_time_message(message)


    def answer_to_count_product_message(self, message):
        """This is answer to count product message"""
        try:
            int(message.text)
            CommandHandler('13005, 22000', message)
            data = IntermediateDataCart(message).create_data_for_message()
            return data
        except ValueError:
            raise ValueError

    def answer_to_customer_name_message(self, message):
        """This is answer to customer name message"""
        CommandHandler('13007, 41000', message)
        data = StandartDataForMessage(message).create_data_for_message()
        return data

    def answer_to_customer_phone_message(self, message):
        """This is answer to customer phone message"""
        CommandHandler('13008, 42000', message)
        data = StandartDataForMessage(message).create_data_for_message()
        return data

    def answer_to_delivery_address_message(self, message):
        """This is answer to delivery address message"""
        CommandHandler('13011, 33000', message)
        db = SelectorDataDb(message)
        delivery_price_and_limit = db.select_data_from_delivery_price_table()
        price_before_scores = db.select_price_before_scores()
        if price_before_scores < delivery_price_and_limit[1]:
            CommandHandler('36000,', message, delivery_price_and_limit[0]+price_before_scores)
        data = DataAboutCustomerScores(message).create_data_for_message()
        return data

    def answer_to_customer_time_message(self, message):
        """This is answer to delivery address message"""
        CommandHandler('13011, 34000', message)
        data = DataAboutCustomerScores(message).create_data_for_message()
        return data

    def answer_to_end_command(self, message):
        """This is answer to end cart with one customer"""
        CommandHandler('10000, 11000, 38001', message)



if __name__ == '__main__':
    pass
