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

    @staticmethod
    def save_all_data(pg_connect, data):
        data = data.__dict__
        key_columns = data.keys()
        values = [data[column] for column in key_columns]
        insert_statement = 'INSERT INTO content.film_work (%s) values %s'
        with pg_connect.cursor() as cursor_pg:
            cursor_pg.execute(insert_statement, (AsIs(
                ','.join(key_columns)), tuple(values)))
            pg_connect.commit()


@dataclass
class Genre:
    id: str
    name: str
    description: str
    created: datetime.now()
    modified: datetime.now()

    @staticmethod
    def save_all_data(pg_connect, data):
        data = data.__dict__
        key_columns = data.keys()
        values = [data[column] for column in key_columns]
        insert_statement = 'INSERT INTO content.genre (%s) values %s'
        with pg_connect.cursor() as cursor_pg:
            cursor_pg.execute(insert_statement, (AsIs(
                ','.join(key_columns)), tuple(values)))
            pg_connect.commit()


@dataclass
class Person:
    id: str
    full_name: str
    created: datetime.now()
    modified: datetime.now()

    @staticmethod
    def save_all_data(pg_connect, data):
        data = data.__dict__
        key_columns = data.keys()
        values = [data[column] for column in key_columns]
        insert_statement = 'INSERT INTO content.person (%s) values %s'
        with pg_connect.cursor() as cursor_pg:
            cursor_pg.execute(insert_statement, (AsIs(
                ','.join(key_columns)), tuple(values)))
            pg_connect.commit()


@dataclass
class GenreFilmWork:
    id: str
    film_work_id: str
    genre_id: str
    created: datetime.now()

    @staticmethod
    def save_all_data(pg_connect, data):
        data = data.__dict__
        key_columns = data.keys()
        values = [data[column] for column in key_columns]
        insert_statement = 'INSERT INTO content.genre_film_work (%s) values %s'
        with pg_connect.cursor() as cursor_pg:
            cursor_pg.execute(insert_statement, (AsIs(
                ','.join(key_columns)), tuple(values)))
            pg_connect.commit()


@dataclass
class PersonFilmWork:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created: datetime.now()

    @staticmethod
    def save_all_data(pg_connect, data):
        data = data.__dict__
        key_columns = data.keys()
        values = [data[column] for column in key_columns]
        insert_statement = 'INSERT INTO content.person_film_work (%s) values %s'
        with pg_connect.cursor() as cursor_pg:
            cursor_pg.execute(insert_statement, (AsIs(
                ','.join(key_columns)), tuple(values)))
            pg_connect.commit()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    cursor = connection.cursor()
    list_table = ['film_work', 'genre', 'person',
                  'person_film_work', 'genre_film_work']
    for i_table in list_table:
        name_table = ''.join(i_table)
        cursor.execute(f"Select * FROM {name_table} LIMIT 0")
        colnames = ', '.join(
            [desc[0] for desc in cursor.description if desc[0] != 'file_path'])
        cursor_sql = connection.cursor()
        print(f"Копирование базы {name_table}")
        table_records_query = cursor_sql.execute(
            f"SELECT {colnames} FROM {name_table}")
        try:
            table_records = table_records_query.fetchmany(50)
            while len(table_records) != 0:
                for data in table_records:
                    if name_table == 'film_work':
                        postgres_saver = FilmWork(*data)
                    elif name_table == 'genre':
                        postgres_saver = Genre(*data)
                    elif name_table == 'person':
                        postgres_saver = Person(*data)
                    elif name_table == 'genre_film_work':
                        postgres_saver = GenreFilmWork(*data)
                    elif name_table == 'person_film_work':
                        postgres_saver = PersonFilmWork(*data)
                    postgres_saver.save_all_data(
                        pg_connect=pg_conn, data=postgres_saver)
                table_records = table_records_query.fetchmany(50)
            print(f"Копирование базы {name_table} успешно выполнено")
        except (Exception, Error) as err:
            print("Ошибка при работе с базой данных", err)
        finally:
            cursor.close()


if __name__ == '__main__':
    try:
        dsl = {'dbname': os.environ.get('DATABASE'), 'user': os.environ.get('USER'),
               'password': os.environ.get('PASSWORD'), 'host': os.environ.get('HOST'), 'port': 5432}
        print('9090')
        print(dsl)
        with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
        print('Задача копирования базы данных завершена.')
    except (Exception, Error) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        sqlite_conn.close()
