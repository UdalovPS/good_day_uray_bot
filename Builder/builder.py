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
        if style_id == 0:
        # if style_id == 0 or step_id == 5 or step_id == 6 or step_id == 7 or step_id == 9 or step_id == 10:
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
        quest = f"Извините, но вы находитесь в черном списке. За подробностями позвоните по телефону <strong>89088964747</strong>\n" \
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


class UnknowCommands(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        quest = f"Для того чтобы сделать новый заказ отправьте: <strong>/заказ</strong> или <strong>/cart</strong>\n" \
                f"Для того чтобы узнать статус заказа отправьте: <strong>/статус</strong> или <strong>/status</strong>\n" \
                f"Для того чтобы узнать кол-во баллов на вашем счету отправьте: <strong>/баллы</strong> или <strong>/points</strong>\n"
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


class CartNoFoundMessage(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        quest = f"Данные не найдены"
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
            CommandHandler('13012, 37000', self.message)
            list_data_db = db.select_intermediate_data_about_cart()
            customer_cart_data_db = db.select_data_about_customer_and_about_cart()
            cart_status = db.select_status_description(customer_cart_data_db[7])
            final_data = DataCartFormer().data_for_customer_about_cart([customer_cart_data_db, list_data_db],
                                                                       'Выбрано:', status=cart_status)
            price_after_scores = db.select_price_after_scores()
            data = final_data + f'Итоговая сумма: {price_after_scores} рублей\n'
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


class FinalDataAboutCart(DataCreator):
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
        price_after_scores = db.select_price_after_scores()
        data = final_data + f'Итоговая сумма: {price_after_scores} рублей\n'
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


class FinalDataAboutCartAfterEnd(DataCreator):
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
        cart_id = db.select_last_cart_id(self.message.chat.id)
        tmp_scores = db.select_tmp_scores(cart_id)
        price_after_scores = db.select_price_after_scores()
        data = final_data + f'Итоговая сумма: {price_after_scores} рублей\n'
        data += f"После оплаты заказа вам будет начислены баллы: <strong>{tmp_scores}</strong>"
        stiker_id = db.select_sticker_id_from_db()
        return Question(data, sticker_id=stiker_id)

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


class FinalDataAboutCartToPersonal(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self):
        personal_channel = '-1001558221765'
        return personal_channel

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        list_data_db = db.select_intermediate_data_about_cart()
        customer_cart_data_db = db.select_data_about_customer_and_about_cart()
        cart_status = db.select_status_description(customer_cart_data_db[7])
        final_data = DataCartFormer().data_for_customer_about_cart_for_personal([customer_cart_data_db, list_data_db],
                                                                                'Выбрано:', status=cart_status)
        price_after_scores = db.select_price_after_scores()
        data = final_data + f'Итоговая сумма: {price_after_scores} рублей\n'
        stiker_id = db.select_sticker_id_from_db()
        return Question(data, sticker_id=stiker_id)

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


class CartDataForStatus(DataCreator):
    def __init__(self, message, cart_id, chat_id=None):
        self.message = message
        self.cart_id = cart_id
        self.chat_id = chat_id

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        list_data_db = db.select_intermediate_data_about_cart(self.cart_id)
        customer_cart_data_db = db.select_data_about_customer_and_about_cart(self.cart_id)
        cart_status = db.select_status_description(customer_cart_data_db[7])
        self.status_id = customer_cart_data_db[7]
        final_data = DataCartFormer().data_for_customer_about_cart([customer_cart_data_db, list_data_db],
                                                                   'Выбрано:', status=cart_status)
        price_after_scores = db.select_price_after_scores(self.cart_id)
        data = final_data + f'Итоговая сумма: <strong>{price_after_scores}</strong> рублей\n'
        stiker_id = db.select_sticker_id_from_db()
        return Question(data, sticker_id=stiker_id)

    def build_dialog_list(self) -> DialogsList:
        if self.status_id in (5, 10, 11):
            data = ()
            dialogs = DialogsList()
            self.add_objects_in_dialog_list(dialogs, data)
        else:
            data = SelectorDataDb(self.message)
            data_dialogs = data.select_dialog_from_db()
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


class CheckCustomerPoints(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        scores = db.select_personal_scores(self.message.chat.id)
        percent = db.select_scores_percent(self.message.chat.id)
        quest = f"Баллы в наличии: <strong>{scores}</strong>\n" \
                f"Персональная скидка: <strong>{percent}%</strong>"
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


class PasswordNotCorrectMessage(DataCreator):
    def __init__(self, message):
        self.message = message

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        quest = f"Введен неверный пароль"
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


class DataAboutCustomerToPersonal(DataCreator):
    def __init__(self, message, customer_id):
        self.message = message
        self.customer_id = customer_id

    def build_chat_id(self) -> int:
        return self.message.chat.id

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        customer_data = db.select_data_about_customer_to_personal(self.customer_id)
        black_id = customer_data[3]
        if black_id == 1:
            black_status = 'Нет, не находится'
        else:
            black_status = 'Да, находится'
        data = f"Идентификационный номер: <strong>{customer_data[0]}</strong>\n" \
               f"Имя: <strong>{customer_data[1]}</strong>\n" \
               f"Номер телефона: <strong>{customer_data[2]}</strong>\n" \
               f"Находится в черном списке: <strong>{black_status}</strong>\n" \
               f"Кол-во баллов на счету: <strong>{customer_data[4]}</strong>\n" \
               f"Персональная скидка: <strong>{customer_data[5]}%</strong>"
        stiker_id = db.select_sticker_id_from_db()
        return Question(data, sticker_id=stiker_id)

    def build_dialog_list(self) -> DialogsList:
        data = SelectorDataDb(self.message)
        data_dialogs = data.select_dialog_from_db()
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
        step_id = SelectorDataDb(call.message).select_step_id_from_db()
        if step_id == 12:
            data = FinalDataAboutCart(call.message).create_data_for_message()
            return data
        elif step_id == 2:
            data = ProductDescriptionMessage(call.message).create_data_for_message()
        else:
            data = StandartDataForMessage(call.message).create_data_for_message()
        return data

    def answer_to_back_inline_commands(self, call):
        """:return - DataForMessage object"""
        CommandHandler('14000,', call.message)
        step_id = SelectorDataDb(call.message).select_step_id_from_db()
        if step_id == 5:
            data = IntermediateDataCart(call.message).create_data_for_message()
        elif step_id == 2:
            data = ProductDescriptionMessage(call.message).create_data_for_message()
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
        elif step_id == 6:
            return self.answer_to_customer_name_message(message)
        elif step_id == 7:
            return self.answer_to_customer_phone_message(message)
        elif step_id == 9:
            return self.answer_to_delivery_address_message(message)
        elif step_id == 10:
            return self.answer_to_customer_time_message(message)
        elif step_id == 500:
            return self.answer_to_status_number_from_customer(message)
        elif step_id == 900:
            return self.check_password(message)
        elif step_id == 910:
            return self.answer_to_status_number_from_personal(message)
        elif step_id == 940:
            return self.check_customer_to_number(message)
        elif step_id == 943:
            return self.change_personal_discount(message)
        else:
            return UnknowCommands(message).create_data_for_message()

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

    def answer_to_end_command_to_customer(self, message):
        """This is answer to end cart with one customer"""
        CommandHandler('10000, 11000, 38001, 52000, 23000', message)
        data = FinalDataAboutCartAfterEnd(message).create_data_for_message()
        return data

    def answer_to_end_command_to_personal(self, message):
        """This is answer to end cart with one customer to personal of shop"""
        data = FinalDataAboutCartToPersonal(message).create_data_for_message()
        return data

    def update_message_id_in_step_table(self, message):
        CommandHandler('39000,', message)

    def select_message_id_from_step_table(self, message):
        return SelectorDataDb(message).select_message_id_from_step_table()

    def answer_to_status_message(self, message):
        black_list = SelectorDataDb(message).check_black_list_about_customer()
        if black_list == 2:
            data = BlackListData(message).create_data_for_message()
        else:
            CommandHandler('13500, 12000', message)
            data = StandartDataForMessage(message).create_data_for_message()
        return data

    def answer_to_status_number_from_customer(self, message):
        db = SelectorDataDb(message)
        cart_number = db.select_cart_id_to_number(message.text, message.chat.id)
        if cart_number:
            CommandHandler('60000,', message)
            data = CartDataForStatus(message, cart_number).create_data_for_message()
        else:
            data = CartNoFoundMessage(message).create_data_for_message()
        return data

    def cancel_cart_from_customer(self, message):
        db = SelectorDataDb(message)
        cart_number = db.select_tmp_cart_id_for_cancel_command()
        CommandHandler('61010,', message, cart_number)
        data = CartDataForStatus(message, cart_number).create_data_for_message()
        return data

    def check_customer_points(self, message):
        data = CheckCustomerPoints(message).create_data_for_message()
        return data

    def password_message(self, message):
        CommandHandler('10000, 11000, 13900', message)
        data = StandartDataForMessage(message).create_data_for_message()
        return data

    def check_password(self, message):
        try:
            input_password = int(message.text)
        except ValueError:
            data = PasswordNotCorrectMessage(message).create_data_for_message()
            return data
        admin_password = SelectorDataDb(message).select_admin_password()
        if input_password == admin_password:
            CommandHandler('13901,', message)
            data = StandartDataForMessage(message).create_data_for_message()
        else:
            data = PasswordNotCorrectMessage(message).create_data_for_message()
        return data

    def answer_to_status_number_from_personal(self, message):
        db = SelectorDataDb(message)
        cart_number = db.select_cart_id_to_number(message.text)
        if cart_number:
            CommandHandler('90000, 13920', message)
            data = CartDataForStatus(message, cart_number).create_data_for_message()
        else:
            data = CartNoFoundMessage(message).create_data_for_message()
        return data

    def check_customer_to_number(self, message):
        db = SelectorDataDb(message)
        customer_id = db.select_customer_id(message.text)
        if customer_id:
            CommandHandler('13941, 93000', message)
            data = DataAboutCustomerToPersonal(message, customer_id).create_data_for_message()
        else:
            data = CartNoFoundMessage(message).create_data_for_message()
        return data

    def change_personal_discount(self, message):
        try:
            new_dicount = int(message.text)
            if new_dicount > 100:
                raise ValueError
            customer_id = SelectorDataDb(message).select_tmp_customer_id()
            CommandHandler('95000, 13942', message, [customer_id, new_dicount])
            data = StandartDataForMessage(message).create_data_for_message()
            return data
        except ValueError:
            raise ValueError


if __name__ == '__main__':
    pass
