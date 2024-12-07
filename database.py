import psycopg2
from contextlib import contextmanager

# Строка подключения к базе данных
DATABASE_URL = "postgresql://viktor:viktor@localhost:5432/StableControl"

# Функция для получения соединения с базой данных
@contextmanager
def get_db():
    try:
        # Устанавливаем соединение с базой данных
        connection = psycopg2.connect(
            database="StableControl",  # Название вашей базы данных
            user="viktor",             # Имя пользователя PostgreSQL
            password="viktor",         # Ваш пароль для подключения
            host="localhost",          # Хост базы данных (локальный хост, если база на вашем компьютере)
            port=5432                  # Порт, на котором работает PostgreSQL
        )
        cursor = connection.cursor()
        yield cursor  # Возвращаем курсор для работы с запросами
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.commit()  # Подтверждаем изменения в базе данных
        connection.close()  # Закрываем соединение
