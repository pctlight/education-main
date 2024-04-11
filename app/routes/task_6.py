import os
import uuid

from fastapi import APIRouter, HTTPException, Body
from app.models import FileIDResponse, DataRequest
from app.core import DataGenerator, YAMLWriter, CSVWriter, JSONWriter

router = APIRouter(tags=["API для хранения файлов"])

if not os.path.exists("generated_files"):
    os.makedirs("generated_files")

"""
Задание_6. 

Изучите следущие классы в модуле app.core: BaseWriter, DataGenerator

API должно принимать json, по типу:
{
    "file_type": "json",  # или "csv", "yaml"
    "matrix_size": int    # число от 4 до 15
}

{
    "file_type": "json",
    "matrix_size": 5
}

В ответ на удачную генерацию файла должен приходить id для скачивания.

Добавьте реализацию методов класса DataGenerator.
Добавьте аннотации типов и (если требуется) модели в модуль app.models.

(Подумать, как переисползовать код из задания 5)
"""

@router.post("/generate_file", description="Задание_6. Конвертер")
async def generate_file(request_data: dict = Body(...)) -> dict:
    """Генерирует файл и возвращает его идентификатор."""
    file_type = request_data.get("file_type")
    matrix_size = request_data.get("matrix_size")

    # Проверяем корректность входных данных
    if not file_type or file_type not in ["json", "csv", "yaml"]:
        return {"error": "Неверный тип файла. Допустимые значения: json, csv, yaml"}
    if not matrix_size or not isinstance(matrix_size, int) or matrix_size < 4 or matrix_size > 15:
        return {"error": "Неверный размер матрицы. Допустимые значения: целые числа от 4 до 15"}

    data = DataGenerator()
    data.generate(matrix_size)

    writer = None
    if file_type == "json":
        writer = JSONWriter()
    elif file_type == "csv":
        writer = CSVWriter()
    elif file_type == "yaml":
        writer = YAMLWriter()

    file_id = str(uuid.uuid4())
    data.to_file(path=f"generated_files/{file_id}.{file_type}", writer=writer)

    return {"file_id": file_id}