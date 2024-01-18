from .__cls_aide_dao_db_types__ import __cls_aide_dao_db_types__ as db_type


class __cls_aide_dao_action__:
    def __init__(self, table_name: str, new_db_type, new_dbc):
        self._table = table_name
        self._db_type = new_db_type

        self.dbc = new_dbc

        self._dict_select = {}
        self._dict_create_insert_update = {}

        self._sql_where = ""

        self.sql_type = None

    @staticmethod
    def chk_col(col: str):
        col = col.replace('"', '')
        col = f'"{col}"'
        col = col.replace('.', '"."')
        col = col.replace('"*"', '*')
        return col

    def get_value(self, key):
        return self._dict_create_insert_update[key]

    def where(self, _sql_where):
        self._sql_where = " WHERE " + _sql_where

    def and_where(self, _sql_where):
        self._sql_where = self._sql_where + " AND " + _sql_where

    def or_where(self, _sql_where):
        self._sql_where = self._sql_where + " OR " + _sql_where

    # Select
    def select(self, data: str, new_value: str = None):
        self.sql_type = "SELECT"

        column = data

        if isinstance(new_value, int):
            pass
        elif new_value is None:
            new_value = None
        else:
            new_value = new_value.replace("'", "''")
            new_value = f"'{new_value}'"

        value = new_value

        self._dict_select[column] = value

    @property
    def SQL_select(self):
        sql_select_item = None

        for key in self._dict_select:

            value = self._dict_select[key]

            column = self.chk_col(key)

            if value in [None, '', ]:
                pass
            else:
                column = f'{column} AS "{value}"'

            if sql_select_item is None:
                sql_select_item = column
            else:
                sql_select_item = f'{sql_select_item},{column}'

        sql = f"SELECT {sql_select_item}" \
              + f" FROM {self._table}" \
              + self._sql_where

        self._dict_select = {}

        return sql

    # Insert
    def add(self, data: str, new_value: str = None):
        self.sql_type = "INSERT"

        if data.find("=") > 0:
            split_index = data.find("=")
            column = data[:split_index]
            value = data[split_index + 1:]
        else:
            column = data
            if isinstance(new_value, int):
                pass
            elif new_value is None:
                new_value = 'NULL'
            else:
                new_value = new_value.replace("'", "''")
                new_value = f"'{new_value}'"

            value = new_value

        self._dict_create_insert_update[column] = value

    @property
    def SQL_add(self):

        sql_columns = None

        sql_values = None

        for key in self._dict_create_insert_update:

            value = self._dict_create_insert_update[key]

            column = self.chk_col(key)

            if sql_columns is None:
                sql_columns = column
                sql_values = value
            else:
                sql_columns = f'{sql_columns},{column}'
                sql_values = f"{sql_values},{value}"

        sql = f"INSERT " \
              + f" INTO {self._table}" \
              + f" ({sql_columns}) VALUES ({sql_values})"

        self._dict_create_insert_update = {}

        return sql

    # Update
    def update(self, data: str, new_value: str = None):
        self.sql_type = "UPDATE"
        self.add(data=data, new_value=new_value)

    @property
    def SQL_update(self):
        sql_update_item = None

        for key in self._dict_create_insert_update:

            value = self._dict_create_insert_update[key]

            column = self.chk_col(key)

            if sql_update_item is None:
                sql_update_item = f"{column}={value}"
            else:
                sql_update_item = f'{sql_update_item},f"{column}={value}"'

        sql = f"UPDATE " \
              + f" {self._table} SET {sql_update_item}" \
              + self._sql_where

        self._dict_create_insert_update = {}

        return sql

    def create(self, new_col_name: str,
               col_type: [db_type.dict_col_type.keys()],
               not_null: bool = False,
               primary_key: bool = False,
               auto_increase: bool = False):

        col_name = self.chk_col(new_col_name)

        col_type = db_type.dict_col_type[col_type][self._db_type]

        if not_null or primary_key:
            col_type += " NOT NULL "
        else:
            pass

        if primary_key and auto_increase:
            col_type += db_type.dict_TYPE_primary_and_auto[self._db_type]
        elif primary_key and not auto_increase:
            col_type += db_type.dict_TYPE_primary_key[self._db_type]
        elif not primary_key and auto_increase:
            col_type += db_type.dict_TYPE_auto_increase[self._db_type]
        else:
            pass

        self._dict_create_insert_update[col_name] = col_type

    def SQL_creat(self):
        sql_create_item = None

        for key in self._dict_create_insert_update:

            value = self._dict_create_insert_update[key]

            column = self.chk_col(key)

            if sql_create_item is None:
                sql_create_item = f"{column} {value}"
            else:
                sql_create_item += f',{column} {value}'

        sql = f"CREATE TABLE {self._table}" \
              + f" ({sql_create_item})"

        return sql
