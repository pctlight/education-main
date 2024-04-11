from fastapi import APIRouter

router = APIRouter(tags=["Стажировка"])

import asyncio

"""
Задание_1. Удаление дублей
    Реализуйте функцию соответствующую следующему описанию:
    На вход подаётся массив слов зависимых от регистра, для которых необходимо произвести
    фильтрацию на основании дублей слов, если в списке найден дубль по регистру, то все
    подобные слова вне зависимости от регистра исключаются.
    На выходе должны получить уникальный список слов в нижнем регистре.

    Список слов для примера: ['Мама', 'МАМА', 'Мама', 'папа', 'ПАПА', 'Мама', 'ДЯдя', 'брАт', 'Дядя', 'Дядя', 'Дядя']
    ["Мама", "МАМА", "Мама", "папа", "ПАПА", "Мама", "ДЯдя", "брАт", "Дядя", "Дядя", "Дядя"]
    Ожидаемый результат: ['папа','брат']
"""
@router.post("/find_in_different_registers", description="Задание_1. Удаление дублей")
async def find_in_different_registers(words: list[str]) -> list[str]:
    unique_words = set()
    duplicates = filter(lambda x: words.count(x) > 1, words)
    duplicates = list(set(duplicates))
    # Создаем список слов в нижнем регистре
    lowercase_words = [word.lower() for word in words]
    duplicates = [duplicates.lower() for duplicates in duplicates]

    # Удаляем из списка дубликаты, найденные в списке duplicates
    unique_words = []
    for word in lowercase_words:
        if word not in duplicates:
            unique_words.append(word)

    return list(set(unique_words))
