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
    def _SQL_list_activity_count(self):
        return "SELECT count(*) " \
               + "FROM sqlite_master WHERE type='table';"

    def _SQL_list_all_tables(self):
        sql = "SELECT * " \
              + "FROM sqlite_master " \
              + f"WHERE type='table' AND name not in ({self._system_tables});"

        return sql

    @staticmethod
    def _SQL_list_table_structure(table_name: str):

        sql = f'PRAGMA TABLE_INFO({table_name})'

        return sql

    @staticmethod
    def _SQL_list_create_table(table_name: str):
        sql = "SELECT sql " \
              + " FROM sqlite_master " \
              + f" WHERE type='table' AND name='{table_name}'"
        return sql

