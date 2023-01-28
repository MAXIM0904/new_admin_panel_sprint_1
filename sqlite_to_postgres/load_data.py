import os
from datetime import datetime
from dataclasses import dataclass

import sqlite3
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from psycopg2.extensions import AsIs
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@dataclass
class FilmWork:
    id: str
    title: str
    description: str
    creation_date: datetime.now()
    rating: float
    type: str
    created: datetime.now()
    modified: datetime.now()


@dataclass
class Genre:
    id: str
    name: str
    description: str
    created: datetime.now()
    modified: datetime.now()


@dataclass
class Person:
    id: str
    full_name: str
    created: datetime.now()
    modified: datetime.now()


@dataclass
class GenreFilmWork:
    id: str
    film_work_id: str
    genre_id: str
    created: datetime.now()


@dataclass
class PersonFilmWork:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created: datetime.now()


def save_all_data(extract_data, conn, name_base):
    for i_extract_data in extract_data:
        data = i_extract_data.__dict__
        key_columns = data.keys()
        values = [data[column] for column in key_columns]
        insert_statement = f'INSERT INTO content.{name_base} (%s) values %s'
        with conn.cursor() as cursor_pg:
            cursor_pg.execute(insert_statement, (AsIs(
                ','.join(key_columns)), tuple(values)))
            conn.commit()


def reformat_sqlite_fields(elem: dict) -> dict:
    if 'created_at' in elem.keys():
        elem['created'] = elem['created_at']
        del (elem['created_at'])

    if 'updated_at' in elem.keys():
        elem['modified'] = elem['updated_at']
        del (elem['updated_at'])

    if 'file_path' in elem.keys():
        del (elem['file_path'])

    return elem


def _prepare_data(cursor, row: list):
    data = {}
    for index, column in enumerate(cursor.description):
        data[column[0]] = row[index]
    return data


class SQLiteExtractor:
    def __init__(self, connection, package_limit: int):
        self.connection = connection
        self.package_limit = package_limit

    def load_sqlite(self, table: str):
        try:
            cursor = self.connection.cursor()
            cursor.row_factory = _prepare_data
            try:
                table_records_query = cursor.execute(f'SELECT * FROM {table}')
            except sqlite3.Error as e:
                raise e
            while True:
                rows = table_records_query.fetchmany(size=self.package_limit)
                if not rows:
                    return
                yield from rows
        except Exception as exception:
            print(exception)
        finally:
            cursor.close()

    def format_dataclass_data(self, table, dataclass):
        data = self.load_sqlite(table)
        return [dataclass(**reformat_sqlite_fields(elem)) for elem in data]


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    sqlite_extractor = SQLiteExtractor(connection, 50)
    for base, schema in datatables_list.items():
        print(f"Копирование таблицы {base}")
        data = sqlite_extractor.format_dataclass_data(base, schema)
        save_all_data(data, pg_conn, base)
        print(f"Копирование таблицы {base} завершено")


datatables_list = {
    'film_work': FilmWork,
    'person': Person,
    'genre': Genre,
    'person_film_work': PersonFilmWork,
    'genre_film_work': GenreFilmWork,
}


if __name__ == '__main__':
    try:
        dsl = {'dbname': os.environ.get('DATABASE'), 'user': os.environ.get('USER'),
               'password': os.environ.get('PASSWORD'), 'host': os.environ.get('HOST'), 'port': 5432}
        with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
        print('Задача копирования базы данных завершена.')
    except (Exception, Error) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        sqlite_conn.close()
