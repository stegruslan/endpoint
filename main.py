from datetime import datetime
from typing import Optional, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Создаем модель данных для работника
class Worker(BaseModel):
    id: int
    fullname: str
    age: int
    bio: str
    signup_at: datetime = datetime.now()  # Дата и время регистрации работника (по умолчанию - текущее время)
    last_login: Optional[datetime] = None  # Дата и время последнего входа работника (может быть None)


# Создаем модель данных для запроса входа в систему
class LoginRequest(BaseModel):
    fullname: str  # Полное имя работника, который пытается войти в систему
    last_login: Optional[str] = None  # Дата и время последнего входа (необязательное поле)


#
workers_db = {}  # Создаем пустой словарь для хранения данных о работниках


# Создаем обработчик POST-запросов для создания нового работника
@app.post("/workers")
async def create_worker(worker: Worker):
    worker_id = len(workers_db) + 1  # Генерируем уникальный ID для нового работника
    worker.id = worker_id  # Присваиваем ID новому работнику
    worker.fullname = worker.fullname  # Присваиваем fullname новому работнику
    worker.age = worker.age  # Присваиваем возраст новому работнику
    worker.bio = worker.bio  # Присваиваем bio (биографию) новому работнику
    worker.signup_at = worker.signup_at or datetime.now()  # Если дата регистрации не указана, используем текущее время
    workers_db[worker_id] = worker  # Добавляем данные работника в базу данных
    return worker  # Возвращаем созданного работника


# Создаем обработчик GET-запросов для получения данных о работнике по его ID
@app.get("/workers/{worker_id}")
async def get_worker(worker_id: int):
    if worker_id not in workers_db:  # Проверяем, существует ли работник с указанным ID
        raise HTTPException(status_code=404, detail="Работник не найден!")  # Если нет, возвращаем ошибку 404
    worker = workers_db[worker_id]  # Получаем данные работника из базы данных
    return worker  # Возвращаем данные о работнике


# Создаем обработчик POST-запросов для входа в систему
@app.post("/login/")
async def login(login_request: LoginRequest):
    for worker in workers_db.values():  # Перебираем всех работников из базы данных
        if worker.fullname == login_request.fullname:  # Если найден работник с указанным именем

            # Возвращаем подтверждение входа и дату последнего входа
            return {"Сообщение": f"Логин подтвержден! {login_request.fullname}",
                    "Дата последнего входа": login_request.last_login}

    # Если работник не найден, возвращаем ошибку 404
    raise HTTPException(status_code=404, detail="Работник не найден!")
