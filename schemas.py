from pydantic import BaseModel
from datetime import datetime

# Модель для создания пользователя
class UserCreate(BaseModel):
    chat_id: int
    name: str
    role: str

# Модель для ответа пользователя
class UserResponse(BaseModel):
    id: int
    chat_id: int
    name: str
    role: str

    class Config:
        orm_mode = True

# Модель для создания лога использования
class UsageLogCreate(BaseModel):
    user_id: int
    status: str
    action: str

# Модель для ответа лога использования
class UsageLogResponse(BaseModel):
    id: int
    user_id: int
    timestamp: datetime
    status: str
    action: str

    class Config:
        orm_mode = True

# Модель для создания записи стабильности
class StabilityLogCreate(BaseModel):
    internet_status: str
    power_status: str

# Модель для ответа записи стабильности
class StabilityLogResponse(BaseModel):
    id: int
    timestamp: datetime
    internet_status: str
    power_status: str

    class Config:
        orm_mode = True
