import config
import telebot
import logging
from Database import sql_handler
from telebot import types

bot = telebot.TeleBot(config.API_TOKEN)
path_db = "Database/db.db"


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.chat.id)
    # markup = types.InlineKeyboardMarkup(row_width=len(btn))
    # for i in btn:
    #     item = types.InlineKeyboardButton(i[1], callback_data=i[0])
    #     markup.add(item)
    bot.send_message(message.chat.id, 'bot start')

@bot.message_handler(content_types=['text'])
def start_message(message):
    print(message.chat.id)
    step_id = db.check_step_id_db(message.chat.id)
    if not step_id:
        step_id = 0
        db.step_user_table.insert_in_table(db.step_user_table.table_name,
                                           db.step_user_table.fields,
                                           (int(message.chat.id), step_id))
    else:
        step_id = step_id[0]
    bot.send_message(message.chat.id, 'Здарова Игорыч!')

@bot.callback_query_handler(func=lambda call: True)
def next_step(call):
    try:
        if call.message:
            # print(call.data)
            # print(type(call.data))
            bot.send_message(call.message.chat.id, call.data)
    except Exception as e:
        print(repr(e))



class WorkWIthDB():
    def __init__(self):
        self.step_user_table = sql_handler.StepUserTable(path_db)
        self.dialog_table = sql_handler.DialogsTable(path_db)
        self.question_table = sql_handler.QuestionTable(path_db)

    def check_step_id_db(self, chat_id):
        cond = 'user_id = {0}'.format(chat_id)
        data = self.step_user_table.select_in_table(self.step_user_table.table_name, 'step', cond)
        return data

if __name__ == '__main__':
    # db = sql_handler.SQLHandler(path_db).create_sub_tables()
    db = WorkWIthDB()
    bot.polling(none_stop=True)
