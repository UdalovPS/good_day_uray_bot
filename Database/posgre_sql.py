import psycopg2
from config import ConfigDatabase

class DatabasePSQL():
    def __init__(self):
        self.host = ConfigDatabase().host
        self.user = ConfigDatabase().user
        self.password = ConfigDatabase().password
        self.db_name = ConfigDatabase().db_name

    def connect_to_db(self):
        connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )
        connection.autocommit = True
        return connection

    def make_cursor(self, con):
        return con.cursor()

    def decorate_open_commit_close(self, *args):
        def real_decorate(func):
            try:                                        #open database
                con = self.connect_to_db()
                with self.make_cursor(con) as cursor:   #make cursor
                    return func(cursor, *args)          #all func with database
            except Exception as _ex:
                print("[INFO] Error while working with PosgreSQL", _ex)
            finally:
                if con:                                 #close database
                    con.close()
                    print("[INFO] PostgreSQL connection closed")
        return real_decorate

    def show_version(self):
        @self.decorate_open_commit_close
        def func(cursor):
            cursor.execute("SELECT version();")
            data = cursor.fetchone()
            print(f"Server version: {data}")

    def create_table(self, table_name, fields_with_parameters):
        @self.decorate_open_commit_close(table_name, fields_with_parameters)
        def func(cursor, table_name, fields_with_parameters):
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {table_name}(
                    {fields_with_parameters});"""
            )
            print(f"[INFO] Table <{table_name}> created successfully")

    def drop_table(self, table_name):
        @self.decorate_open_commit_close(table_name)
        def func(cursor, table_name):
            cursor.execute(
                f"""DROP TABLE {table_name};"""
            )
            print(f'[INFO] Table <{table_name}> was deleted')

    def insert_data_in_table(self, table_name, fields, data):
        @self.decorate_open_commit_close(table_name, fields, data)
        def func(cursor, table_name, fields, data):
            print(f'INSERT INTO {table_name} ({fields}) VALUES {data};')
            cursor.execute(
                f"""INSERT INTO {table_name} ({fields}) VALUES {data};"""
            )
            print('[INFO] Data was successfully inserted')

    def delete_data_from_table(self, table_name, conditions):
        @self.decorate_open_commit_close(table_name, conditions)
        def func(cursor, table_name, conditions):
            cursor.execute(
                f"""DELETE FROM {table_name} WHERE {conditions};"""
            )
            print(f'[INFO] Data from <{table_name}> was deleted')

    def select_in_table(self, table_name, fields, conditions=None):
        @self.decorate_open_commit_close(table_name, fields, conditions)
        def func(cursor, table_name, fields, conditions):
            if not conditions:                  #if conditions is not exists
                cursor.execute(
                    f"""SELECT {fields} FROM {table_name};"""
                )
            else:                               # if conditions is exist
                cursor.execute(
                    f"""SELECT {fields} FROM {table_name}
                        WHERE {conditions};"""
                )
            data = cursor.fetchall()
            print(f'[INFO] Data <{data}> was selected from <{table_name}>')
            return data
        return func

    def update_fields(self, table_name, fields_value, conditions):
        @self.decorate_open_commit_close(table_name, fields_value, conditions)
        def func(cursor, table_name, fields_value, conditions):
            cursor.execute(
                f"""UPDATE {table_name} SET {fields_value}
                    WHERE {conditions};"""
            )
            print(f'[INFO] Data <{fields_value}> from <{table_name}> where <{conditions}> was updated ')


class StepTable(DatabasePSQL):
    def __init__(self):
        super().__init__()
        self.table_name = 'step_table'
        self.fields_with_parameters = "user_id INTEGER," \
                                      "step_number INTEGER," \
                                      "style_id INTEGER"
        self.fields = 'user_id, step_number, style_id'
        self.split_fields = self.fields.split(', ')


class QuestionsTable(DatabasePSQL):
    def __init__(self):
        super().__init__()
        self.table_name = 'questions_table'
        self.fields_with_parameters = 'step_id INTEGER,' \
                                      'style_id INTEGER,' \
                                      'question varchar(255)'
        self.fields = 'step_id, style_id, question'
        self.split_fields = self.fields.split(', ')


class DialogsTable(DatabasePSQL, ConfigDatabase):
    def __init__(self):
        super().__init__()
        self.table_name = 'dialogs_table'
        self.fields_with_parameters = "step_id INTEGER, " \
                                      "style_id INTEGER, " \
                                      "dialog varchar(255)," \
                                      "next_step INTEGER," \
                                      "next_style INTEGER"
        self.fields = 'step_id, style_id, dialog, next_step, next_style'
        self.split_fields = self.fields.split(', ')

if __name__ == '__main__':
    db = DialogsTable()
    # db.drop_table(db.table_name)
    # db.create_table(db.table_name, db.fields_with_parameters)
    # db.insert_data_in_table(db.table_name, db.fields, (0, 1, 'Стандартный'))
    # data = db.select_in_table(db.table_name, db.fields)
    # print(data)
    # db.update_fields(db.table_name, 'step_number = 1', 'user_id = 131312')
    # db.delete_data_from_table(db.table_name, 'step_id=0')
    start = StepTable()
    start.update_fields(start.table_name,
                        f'{start.split_fields[1]} = 0, {start.split_fields[2]} = 0',
                        f'{start.split_fields[0]}=1953960185')
