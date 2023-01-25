import sqlite3
from datetime import datetime
from psycopg2 import Error
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dataclasses import dataclass, astuple


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
        with pg_connect.cursor() as cursor_pg:
            postgres_insert_query = """INSERT INTO content.film_work 
            (id, title, description, creation_date, rating, type, created, modified)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
            record_to_insert = astuple(data)
            cursor_pg.execute(postgres_insert_query, record_to_insert)
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
        with pg_connect.cursor() as cursor_pg:
            postgres_insert_query = """INSERT INTO content.genre (id, name, description, created, modified)
            VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = astuple(data)
            cursor_pg.execute(postgres_insert_query, record_to_insert)
            pg_connect.commit()


@dataclass
class Person:
    id: str
    full_name: str
    created: datetime.now()
    modified: datetime.now()

    @staticmethod
    def save_all_data(pg_connect, data):
        with pg_connect.cursor() as cursor_pg:
            postgres_insert_query = """INSERT INTO content.person (id, full_name, created, modified)
            VALUES (%s,%s,%s,%s)"""
            record_to_insert = astuple(data)
            cursor_pg.execute(postgres_insert_query, record_to_insert)
            pg_connect.commit()


@dataclass
class GenreFilmWork:
    id: str
    genre_id: str
    film_work_id: str
    created: datetime.now()

    @staticmethod
    def save_all_data(pg_connect, data):
        with pg_connect.cursor() as cursor_pg:
            postgres_insert_query = """INSERT INTO content.genre_film_work (id, genre_id, film_work_id, created)
            VALUES (%s,%s,%s,%s)"""
            record_to_insert = astuple(data)
            cursor_pg.execute(postgres_insert_query, record_to_insert)
            pg_connect.commit()


@dataclass
class PersonFilmWork:
    id: str
    person_id: str
    film_work_id: str
    role: str
    created: datetime.now()

    @staticmethod
    def save_all_data(pg_connect, data):
        with pg_connect.cursor() as cursor_pg:
            postgres_insert_query = """INSERT INTO content.person_film_work (id, person_id, film_work_id, role, created)
            VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = astuple(data)
            cursor_pg.execute(postgres_insert_query, record_to_insert)
            pg_connect.commit()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    table = (
        ('film_work', 'id, title, description, creation_date, rating, type, created_at, updated_at'),
        ('genre', 'id, name, description, created_at, updated_at'),
        ('person', 'id, full_name, created_at, updated_at'),
        ('genre_film_work', 'id, genre_id, film_work_id, created_at'),
        ('person_film_work', 'id, person_id, film_work_id, role, created_at')
    )

    for i_table in table:
        cursor_sql = connection.cursor()
        print(f"Копирование базы {i_table[0]}")
        table_records_query = cursor_sql.execute(f"SELECT {i_table[1]} FROM {i_table[0]}")
        try:
            table_records = table_records_query.fetchmany(50)
            while len(table_records) != 0:
                for data in table_records:
                    if i_table[0] == 'film_work':
                        postgres_saver = FilmWork(*data)
                    elif i_table[0] == 'genre':
                        postgres_saver = Genre(*data)
                    elif i_table[0] == 'person':
                        postgres_saver = Person(*data)
                    elif i_table[0] == 'genre_film_work':
                        postgres_saver = GenreFilmWork(*data)
                    else:
                        postgres_saver = PersonFilmWork(*data)
                    postgres_saver.save_all_data(pg_connect=pg_conn, data=postgres_saver)
                table_records = table_records_query.fetchmany(50)
            print(f"Копирование базы {i_table[0]} успешно выполнено")
        except (Exception, Error) as error:
            print("Ошибка при работе с базой данных", error)


if __name__ == '__main__':
    try:
        dsl = {'dbname': 'movies_database', 'user': 'postgres', 'password': '12345', 'host': '127.0.0.1', 'port': 5432}
        with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
        print('Задача копирования базы данных завершена.')
    except (Exception, Error) as error:
        print("Ошибка при работе с базой данных", error)
