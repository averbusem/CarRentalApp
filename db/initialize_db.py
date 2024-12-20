import psycopg2
from psycopg2 import sql
import os


def initialize_db():
    """
    Инициализация базы данных. Проверяет существование БД и создает её при необходимости.
    """
    server_config = {
        "host": "localhost",
        "user": "db_creator",
        "password": "db_creator",
        "port": 5432,
        "dbname": "template1"  # Используем системную БД для подключения
    }

    db_name = "car_rental"
    schema_path = os.path.join(os.path.dirname(__file__), "scheme.sql")

    try:
        # Подключаемся к серверу PostgreSQL
        conn = psycopg2.connect(**server_config)
        conn.autocommit = True

        with conn.cursor() as cursor:
            # Проверка существования базы данных
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,)
            )
            db_exists = cursor.fetchone()

            if not db_exists:
                print(f"База данных '{db_name}' не найдена. Создание...")
                # Создание базы данных
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                )
                print(f"База данных '{db_name}' успешно создана.")

                # Применяем схему после создания базы данных
                schema_config = server_config.copy()
                schema_config["dbname"] = db_name

                with psycopg2.connect(**schema_config) as db_conn:
                    with db_conn.cursor() as db_cursor:
                        with open(schema_path, "r", encoding="utf-8") as schema_file:
                            db_cursor.execute(schema_file.read())
                        print(f"Схема базы данных успешно применена.")
            else:
                print(f"База данных '{db_name}' уже существует.")

    except psycopg2.Error as e:
        print(f"Не получилось полностью создать БД: {e}")
