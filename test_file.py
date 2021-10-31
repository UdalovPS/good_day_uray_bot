class Question:
    def __init__(self):
        self.text = 'Question text'
        self.sticker = 'Sticker'


class ChatId:
    def __init__(self):
        self.text = '1953960185'


class Dialogs:
    def __init__(self):
        self.dialogs = (('One', '40000'), ('Two', '5000'))


class FormDataForMsg:
    def build_question(self):
        return Question()

    def build_chat_id(self):
        return ChatId()

    def build_dialogs(self):
        return Dialogs()

    def create_data_for_msg(self):
        quest = self.build_question()
        chat_id = self.build_chat_id()
        dialogs = self.build_dialogs()
        return DataForMsg(quest, chat_id, dialogs)

class DataForMsg:
    def __init__(self, quest, chat_id, dialogs):
        self.quest = quest
        self.chat_id = chat_id
        self.dialogs = dialogs
