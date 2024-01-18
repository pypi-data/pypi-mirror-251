# pip install psycopg2
import sqlite3

from .__cls_aide_rst_base__ import __cls_aide_rst_base
from .__cls_aide_sql_sqlite__ import __cls_aide_sql_sqlite


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

    def __execute_SQL_base__(self, sql, sql_type):
        self.rst.set_process(f"{sql_type}.{self.rst.process}")
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
            self.__execute_SQL_base__(sql, sql_type)
        else:
            self.rst.set(False, f'Only {sql_type} SQL can be execute!,Cost:{self.rst.dur}', sql)

    def select(self, sql):
        self.__execute_sql(sql, sql_type='SELECT')

    def pragma(self, sql):
        self.__execute_sql(sql, sql_type='PRAGMA')

    def insert(self, sql):
        self.__execute_sql(sql, sql_type="INSERT")

    def update(self, sql):
        self.__execute_sql(sql, sql_type='UPDATE')

    def delete(self, sql):
        self.__execute_sql(sql, sql_type='DELETE')

    def creat(self, sql):
        self.__execute_sql(sql, sql_type="CREATE")

    def load_activity_count(self):
        self.rst.set_process("load_activity_count")

        sql = self._SQL_list_activity_count

        self.select(sql)

        return self.rst.state

    def load_all_tables(self):
        self.rst.set_process("load_all_tables")

        sql = self._SQL_list_all_tables()

        self.select(sql)

    def load_table_structure(self, table_name: str):
        self.rst.set_process("load_table_structure")

        sql = self._SQL_list_table_structure(table_name=table_name)

        self.pragma(sql)

    def get_table_create_sql(self, table_name: str):
        self.rst.set_process("get_table_create_sql")

        sql = self._SQL_list_create_table(table_name=table_name)

        self.select(sql)

        if self.rst.state is True:
            if len(self.rst.data) >0:
                return self.rst.data[0]["sql"]
            else:
                return None
        else:
            return None
