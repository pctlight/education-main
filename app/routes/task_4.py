from fastapi import APIRouter, HTTPException, File, UploadFile
from app.core import average_age_by_position

import pandas as pd

router = APIRouter(tags=["Стажировка"])

"""
Задание_4. Работа с pandas и csv. 

В модуле app.core реализуйте функцию average_age_by_position(), 
которая принимает на вход CSV файл с данными о сотрудниках компании. 

В файле должны быть следующие колонки: "Имя", "Возраст", "Должность". 
Функция должна вернуть словарь, в котором ключами являются уникальные должности, 
а значениями — средний возраст сотрудников на каждой должности. 
Для чтения и работы с csv файлами, нужно использовать библиотеку pandas.

Пример CSV файла (employees.csv): 
Имя,Возраст,Должность
Алексей,25,Разработчик
Мария,30,Менеджер
Иван,28,Разработчик
Анна,35,Менеджер


Роут так же должен принимать на входе csv файл.
Пример ответа:
{
    "Разработчик": 26.5,
    "Менеджер": 32.5
}

Рекомендуется добавить аннотации типов. Также добавьте исключения, если файл приходит не валидный, например, 
неправильный формат файла, названия столбцов отличаются и т.д. 
В таких случаях ожидается строка с ошибкой и status code 400.
"""

@router.post("/get_average_age_by_position", description="Задание_4. Работа с pandas и csv")
async def get_average_age_by_position(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        result = average_age_by_position(df)
        return result
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail="Ошибка чтения файла CSV: {}".format(str(e)))