from functools import wraps
from fastapi import APIRouter, Response

router = APIRouter(tags=["Стажировка"])

# Переменная для хранения количества запросов
total_requests = 0

def count_requests(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global total_requests
        total_requests += 1
        return await func(*args, **kwargs)
    return wrapper


@router.get("/new_request", description="Задание_8. Декоратор - счётчик запросов.")
@count_requests  # Применяем декоратор к этому маршруту
async def new_request():
    """Возвращает кол-во сделанных запросов."""
    return Response(content=f"Total requests: {total_requests}\n")
