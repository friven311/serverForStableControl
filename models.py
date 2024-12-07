from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Модель для таблицы users
class User(BaseModel):
    id: Optional[int]  # ID будет задаваться базой данных
    chat_id: int
    name: str
    role: str


# Модель для таблицы usage_logs
class UsageLog(BaseModel):
    id: Optional[int]  # ID будет задаваться базой данных
    user_id: int       # Связь с пользователем
    timestamp: Optional[datetime] = None  # Значение по умолчанию: текущее время
    status: str
    action: str


# Модель для таблицы stability_logs
class StabilityLog(BaseModel):
    id: Optional[int]  # ID будет задаваться базой данных
    timestamp: Optional[datetime] = None  # Значение по умолчанию: текущее время
    internet_status: str
    power_status: str
