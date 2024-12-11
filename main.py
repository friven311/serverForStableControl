from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware



# Инициализация FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любого источника
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Подключение к базе данных
def get_db_connection():
    try:
        connection = psycopg2.connect(
            database="railway",  # Название базы данных
            user="postgres",  # Имя пользователя PostgreSQL
            password="HuDbpPJkxjLHnMWquaJTjaEsBXBRbFuU",  # Ваш пароль для подключения
            host="junction.proxy.rlwy.net",  # Хост базы данных
            port=21079  # Порт для подключения
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
class History(BaseModel):
    id: int
    open_name: str
    datetime: str
    open_id: int
    status: str
# Модель пользователя для редактирования
class UserUpdate(BaseModel):
    chat_id: Optional[int]
    name: Optional[str]
    role: Optional[str]
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
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
            return {"message": f"User with id {user_id} successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {e}")
    finally:
        connection.close()
# Эндпоинт для редактирования пользователя по ID
@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            update_fields = []
            update_values = []
            if user_update.chat_id is not None:
                update_fields.append("chat_id = %s")
                update_values.append(user_update.chat_id)
            if user_update.name is not None:
                update_fields.append("name = %s")
                update_values.append(user_update.name)
            if user_update.role is not None:
                update_fields.append("role = %s")
                update_values.append(user_update.role)
            update_values.append(user_id)
            update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
            cursor.execute(update_query, tuple(update_values))
            connection.commit()
            return {"message": f"User with id {user_id} successfully updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {e}")
    finally:
        connection.close()

# Эндпоинт для получения всех записей из History
@app.get("/history1", response_model=List[History])
def get_history():
    connection = get_db_connection()
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM history1")
            items = cursor.fetchall()
            return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching History: {e}")
    finally:
        connection.close()

# Эндпоинт для добавления новой записи в history1
@app.post("/history1")
def add_history(item: History):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO history1 (id, datetime, status, open_name,	open_id) VALUES (%s, %s, %s, %s)",
                (item.id, item.datetime, item.status, item.open_name, item.open_id)
            )
            connection.commit()
            return {"message": "History1 added successfully", "item": item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding History1: {e}")
    finally:
        connection.close()


