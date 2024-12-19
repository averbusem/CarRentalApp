import psycopg2
from psycopg2 import sql
import os


def initialize_db():
    """
    Инициализация базы данных. Проверяет существование БД и создает её при необходимости.
    """
    # Параметры подключения к серверу PostgreSQL
    server_config = {
        "host": "localhost",
        "user": "postgres",
        "password": "postgres",
        "port": 5432
    }

    db_name = "car_rental"
    schema_path = os.path.join(os.path.dirname(__file__), "scheme.sql")

    try:
        # Подключаемся к серверу PostgreSQL без указания базы данных
        conn = psycopg2.connect(**server_config)
        conn.autocommit = True  # Отключаем транзакции для этой операции

        with conn.cursor() as cursor:
            # Проверка существования базы данных
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,)
            )
            db_exists = cursor.fetchone()

            if not db_exists:
                print(f"База данных '{db_name}' не найдена. Создание...")
                # Создание базы данных
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print(f"База данных '{db_name}' успешно создана.")
                # Закрываем соединение с сервером PostgreSQL
                conn.close()

                # Применяем схему после создания базы данных
                with psycopg2.connect(**server_config, dbname=db_name) as db_conn:
                    with db_conn.cursor() as db_cursor:
                        with open(schema_path, "r", encoding="utf-8") as schema_file:
                            db_cursor.execute(schema_file.read())
                        # print(f"Схема базы данных из '{schema_path}' успешно применена.")

            else:
                print(f"База данных '{db_name}' уже существует.")

    except Exception as e:
        print(f"Не получилось подключиться к postgres: {e}")


