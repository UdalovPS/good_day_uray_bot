from abc import ABC, abstractmethod
from new_command_handler import CommandHandler
from new_data_selector import SelectorDataDb

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


class AnswerFactory:
    def answer_to_start_command(self, message):
        """ /start command"""
        black_list = SelectorDataDb(message).check_black_list_about_customer()
        if black_list == 2:
            data = BlackListData(message).create_data_for_message()
        else:
            CommandHandler('10000, 11000, 30000', message)
            data = StandartDataForMessage(message).create_data_for_message()
        return data

    def answer_to_inline_commands(self, call):
        """answer to not concrete inline commands
            :return - DataForMessage object"""
        CommandHandler(call.data, call.message)
        data = StandartDataForMessage(call.message).create_data_for_message()
        return data

    def answer_to_back_inline_commands(self, call):
        """:return - DataForMessage object"""
        CommandHandler('14000,', call.message)
        data = StandartDataForMessage(call.message).create_data_for_message()
        return data

    def pre_question_in_dialog(self, call):
        """:return - previous question in dialog for bot.send_message method"""
        data = PreviousQuestionInlineBtn(call).create_data_for_message()
        return data

    def pre_inline_btn_customer_answer(self, call):
        """:return - text previous press button"""
        data = PreviousInlineButtonAnswer(call).create_data_for_message()
        return data

    def update_sticker_id_in_step_table(self, sticker):
        """This method update now sticker_message_id in step_table"""
        CommandHandler('15000,', sticker)

    def delete_sticker_id_in_step_table(self, call):
        """This method delete previous sticker_message_id from step_table"""
        CommandHandler('16000,', call.message)



if __name__ == '__main__':
    pass
