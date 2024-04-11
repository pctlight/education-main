import uuid

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from zipfile import ZipFile
import os

from app.models import FileStorage

router = APIRouter(tags=["API для хранения файлов"])

@router.post("/upload_file", description="Задание_5. API для хранения файлов")
async def upload_file(file: UploadFile = File(...)) -> str:
    """Метод для загрузки файла и архивирования."""
    file_id = str(uuid.uuid4())  # Генерация уникального ID файла

    # Сохраняем загруженный файл в папку проекта с его исходным именем
    file_path = f"uploaded_files/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Добавляем запись в словарь с идентификатором файла и его названием
    FileStorage.file_dict[file_id] = file.filename

    # Создаем архив с исходным именем файла
    with ZipFile(f"uploaded_files/{file.filename}.zip", 'w') as zip_file:
        zip_file.write(file_path, arcname=os.path.basename(file.filename))
    return file_id


@router.get("/download_file/{file_id}", description="Задание_5. API для хранения файлов")
async def download_file(file_id: str):
    """Метод для скачивания архивированного файла."""
    # Проверяем наличие файла в словаре
    if file_id not in FileStorage.file_dict:
        existing_ids = list(FileStorage.file_dict.keys())
        return {"error": f"Файла под таким id не найдено. Существующие id: {existing_ids}"}

    # Получаем имя файла по его идентификатору из словаря
    file_name = FileStorage.file_dict[file_id]
    file_path = f"uploaded_files/{file_name}.zip"

    # Проверяем существование архива
    if not os.path.exists(file_path):
        return {"error": "Архив не найден"}

    # Возвращаем архив пользователю
    return FileResponse(path=file_path, media_type='application/zip', filename=file_name)
