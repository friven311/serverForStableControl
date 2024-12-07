from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor

# Инициализация FastAPI
app = FastAPI()

# Подключение к базе данных
def get_db_connection():
    try:
        connection = psycopg2.connect(
            database="StableControl",
            user="viktor",
            password="viktor",
            host="localhost",
            port=5432
        )
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

# Модель пользователя
class User(BaseModel):
    id: int
    chat_id: int
    name: str
    role: str

# Эндпоинт для получения списка пользователей
@app.get("/users", response_model=List[User])
def get_users():
    connection = get_db_connection()
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")
    finally:
        connection.close()

# Эндпоинт для добавления нового пользователя
@app.post("/users")
def add_user(user: User):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (id, chat_id, name, role) VALUES (%s, %s, %s, %s)",
                (user.id, user.chat_id, user.name, user.role)
            )
            connection.commit()
            return {"message": "User added successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding user: {e}")
    finally:
        connection.close()
