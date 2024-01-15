# pip install psycopg2
import sqlite3

import datetime


class __cls_aide_rst_base:
    class _cls_aide_rst_base:
        def __init__(self, module: str):
            self.__dict_rst = {"state": False,
                               "msg": None,
                               "data": None,
                               "dur": None,
                               'process': "INIT",
                               'module': module}

            self.start_time = None

        @staticmethod
        def now():
            return datetime.datetime.now()

        def start(self):
            self.start_time = self.now()

        @property
        def dur(self,
                my_time_earlier: datetime.datetime = None,
                my_time_later: datetime.datetime = None):

            if my_time_later is None:
                my_time_later = datetime.datetime.now()
            else:
                pass

            if my_time_earlier is None:
                if isinstance(self.start_time, datetime.datetime):
                    my_time_earlier = self.start_time
                else:
                    return None
            else:
                pass

            diff = (my_time_later - my_time_earlier).microseconds

            diff_second = diff / 1000000

            return diff_second

        @staticmethod
        def __get_dict_value(my_dict_rst, my_key):
            if my_dict_rst.__contains__(my_key):
                return my_dict_rst[my_key]
            else:
                return None

        @property
        def state(self):
            return self.__get_dict_value(self.__dict_rst, "state")

        def set_state(self, new_state: bool = False):
            self.__dict_rst["state"] = new_state

        @property
        def msg(self):
            return self.__get_dict_value(self.__dict_rst, "msg")

        def set_msg(self, new_msg: object = None):
            self.__dict_rst["msg"] = new_msg

        @property
        def data(self):
            return self.__get_dict_value(self.__dict_rst, "data")

        def set_data(self, new_data: object = None):
            self.__dict_rst["data"] = new_data

        @property
        def process(self):
            return self.__get_dict_value(self.__dict_rst, "process")

        def set_process(self, new_process_name: str = None):
            self.start()
            self.__dict_rst["process"] = new_process_name

        @property
        def all(self):
            return self.__dict_rst

        def print(self):
            print(self.all)

        def set(self, new_state, new_msg, new_data: object = None, new_process: str = None):
            self.set_state(new_state)
            self.set_msg(new_msg)
            self.set_data(new_data)
            if new_process is not None:
                self.set_process(new_process)
            else:
                pass


class __cls_aide_sql_sqlite:
    # noinspection PyMissingConstructor
    def __init__(self):
        pass

    @staticmethod
    def Chk(s: str):
        if s[0] != '"' and s[-1] != '"':
            return f'"{s}"'
        elif s[0] == '"' and s[-1] != '"':
            return f'{s}"'
        elif s[0] != '"' and s[-1] == '"':
            return f'"{s}'
        else:
            return s

    @property
    def _system_tables(self):
        return "'sqlite_sequence'"

    @property
    def _sql_list_activity_count(self):
        return "SELECT count(*) " \
               + "FROM sqlite_master WHERE type='table';"

    def _sql_list_all_tables(self):
        sql = "SELECT * " \
              + "FROM sqlite_master " \
              + f"WHERE type='table' AND name not in ({self._system_tables});"

        return sql

    @staticmethod
    def _sql_list_table_structure(table_name: str):

        sql = f'PRAGMA TABLE_INFO({table_name})'

        return sql


class cls_conn(__cls_aide_rst_base, __cls_aide_sql_sqlite):
    # noinspection PyMissingConstructor
    def __init__(self, db_path: str, password=None):
        self.rst = self._cls_aide_rst_base("pgs")

        self.__dirt_connection_info = {"path": "",
                                       "password": None,
                                       "connected": None,
                                       "connected_time": None,
                                       "SQL": None}

        self.conn = None

        self.set_db_path(db_path)
        self.set_password(password)

        self.connect()

    @property
    def connection_info(self):
        return self.__dirt_connection_info

    @property
    def db_path(self):
        return self.__dirt_connection_info["db_path"]

    def set_db_path(self, new_value):
        self.__dirt_connection_info["db_path"] = new_value

    @property
    def password(self):
        return self.__dirt_connection_info["password"]

    def set_password(self, new_value):
        self.__dirt_connection_info["password"] = new_value

    @property
    def connected(self):
        return self.__dirt_connection_info["connected"]

    def set_connected(self, new_value):
        if new_value is None:
            new_value = False
        else:
            pass

        self.__dirt_connection_info["connected"] = new_value

    @property
    def connected_time(self):
        return self.__dirt_connection_info["connected_time"]

    def set_connected_time(self, new_value):
        self.__dirt_connection_info["connected_time"] = new_value

    @property
    def SQL(self):
        return self.__dirt_connection_info["SQL"]

    def set_SQL(self, new_value):
        self.__dirt_connection_info["SQL"] = new_value

    def connect(self):
        self.rst.set_process("connect")

        try:
            self.set_connected(False)
            self.conn = sqlite3.connect(self.db_path)

            self.set_connected(True)

            self.rst.set(self.connected,
                         f'Connected! Cost:{self.rst.dur}',
                         self.db_path)
        except Exception as e:

            if e:
                self.rst.set(False,
                             f'Exception:Connection failed! Cost:{self.rst.dur}',
                             e.__str__())
            else:
                self.rst.set(False,
                             f'DB ERROR:Connection failed! Cost:{self.rst.dur}',
                             f'DB error_log:######################')

    def disconnect(self):
        if self.connected is True:
            self.conn.close()
            self.set_connected(False)

    def __execute_sql_base__(self, sql, sql_type):
        self.set_SQL(sql)

        if self.connected is True:
            pass
        else:
            self.connect()
            if self.rst.state is False:
                return None

        self.rst.set(False, None, None)

        cur = self.conn.cursor()

        try:
            cur.execute("BEGIN" + ";")

            sql = self.SQL

            if sql[-1:] == ";":
                pass
            else:
                self.set_SQL(f"{sql};")

            cur.execute(self.SQL)

            self.conn.commit()

            if sql_type in ["SELECT", "PRAGMA"]:
                data = cur.fetchall()
                data_desc = cur.description
                data_header = [desc[0] for desc in data_desc]
                data_with_header = {i: dict(zip(data_header, row)) for i, row in enumerate(data)}
                data = data_with_header
            else:
                data = cur.statusmessage

            self.rst.set(True,
                         f'{sql_type} {len(data)} row(s) successful!Cost:{self.rst.dur}',
                         data)
        except Exception as e:
            self.conn.rollback()
            if e:
                self.rst.set(False,
                             'Exception:' + e.__str__().replace("'", "") + f',Cost:{self.rst.dur}',
                             sql)
            else:
                self.rst.set(False,
                             'DB ERROR:' + self.conn.stmt_errormsg() + f',Cost:{self.rst.dur}',
                             sql)
        finally:
            cur.close()

        return self.rst.state

    def __execute_sql(self, sql, sql_type):
        sql = sql.strip()
        if sql[0:6].upper() == sql_type.upper():
            self.__execute_sql_base__(sql, sql_type)
        else:
            self.rst.set(False, f'Only {sql_type} SQL can be execute!,Cost:{self.rst.dur}', sql)

    def select(self, sql):
        self.rst.set_process("select")
        self.__execute_sql(sql, sql_type='SELECT')

    def pragma(self, sql):
        self.rst.set_process("pragma")
        self.__execute_sql(sql, sql_type='PRAGMA')

    def insert(self, sql):
        self.rst.set_process("insert")
        self.__execute_sql(sql, sql_type="INSERT")

    def update(self, sql):
        self.rst.set_process("update")
        self.__execute_sql(sql, sql_type='UPDATE')

    def delete(self, sql):
        self.rst.set_process("delete")
        self.__execute_sql(sql, sql_type='DELETE')

    def creat(self, sql):
        self.rst.set_process("creat")
        self.__execute_sql(sql, sql_type="CREATE")

    def load_activity_count(self):
        self.rst.set_process("load_activity_count")

        sql = self._sql_list_activity_count

        self.select(sql)

        return self.rst.state

    def load_all_tables(self):
        self.rst.set_process("load_all_tables")

        sql = self._sql_list_all_tables()

        self.select(sql)

    def load_table_structure(self, table_name):
        self.rst.set_process("load_table_structure")

        sql = self._sql_list_table_structure(table_name=table_name)

        self.pragma(sql)
