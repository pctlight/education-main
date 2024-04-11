from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.models import BigJson, User

router = APIRouter(tags=["Стажировка"])

"""
Задание_3. Валидация json

В теле запроса передаётся json. Необходимо проверять его на наличие полей и типов данных.
Поля обязательные, если не написано иное.
Например:
{
    "user": {
        "name": "Ivan",  
        "age": 23,  
        "adult": true,  
        "message": ""  
    },
    "meta": {
        "last_modification": "20/05/2023",  
        "list_of_skills": ["ловкий", "смелый"], 
        "mapping": {
            "list_of_ids": [1, "два"],
            "tags": ["стажировка", "egtreg"]  
        }
    
    }
}
Напишите валидатор в модуле app.models для класса BigJson.
Используйте библиотеку pydantic.

"""

@router.post("/check_json", description="Задание_3. Валидация json")
async def check_json(body: BigJson) -> BigJson:

    return body