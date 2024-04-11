from abc import ABC, abstractmethod
from io import StringIO
from typing import Dict
import pandas as pd
import json
import csv
import yaml
import random
from typing import List, Tuple

def convert_arabic_to_roman(number: int) -> str:
    if not 0 < number < 4000:
        return "не поддерживается"

    roman_numerals = {
        1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X',
        40: 'XL', 50: 'L', 90: 'XC', 100: 'C',
        400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'
    }
    result = ''
    for value, numeral in sorted(roman_numerals.items(), reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result


def convert_roman_to_arabic(number: str) -> int:
    roman_numerals = {
        'I': 1, 'IV': 4, 'V': 5, 'IX': 9, 'X': 10,
        'XL': 40, 'L': 50, 'XC': 90, 'C': 100,
        'CD': 400, 'D': 500, 'CM': 900, 'M': 1000
    }
    result = 0
    i = 0
    while i < len(number):
        if i + 1 < len(number) and number[i:i + 2] in roman_numerals:
            result += roman_numerals[number[i:i + 2]]
            i += 2
        else:
            result += roman_numerals[number[i]]
            i += 1
    return result


def average_age_by_position(df: pd.DataFrame) -> Dict[str, float]:
    try:
        return df.groupby('Должность')['Возраст'].mean().to_dict()
    except KeyError:
        raise ValueError("Неверный формат файла CSV или отсутствуют необходимые столбцы")


"""
Задание_6.
Дан класс DataGenerator, который имеет два метода: generate(), to_file()
Метод generate генерирует данные формата list[list[int, str, float]] и записывает результат в
переменную класса data
Метод to_file сохраняет значение переменной generated_data по пути path c помощью метода
write, классов JSONWritter, CSVWritter, YAMLWritter.

Допишите реализацию методов и классов.
"""
class BaseWriter(ABC):
    """Абстрактный класс с методом write для генерации файла"""

    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        pass


class JSONWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в json формате"""

    def write(self, data: List[List[Tuple[int, str, float]]]) -> StringIO:
        """
        Записывает данные в формате JSON
        :param data: данные для записи
        :return: объект StringIO с данными в формате JSON
        """
        output = StringIO()
        json.dump(data, output)
        output.seek(0)
        return output


class CSVWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в csv формате"""

    def write(self, data: List[List[Tuple[int, str, float]]]) -> StringIO:
        """
        Записывает данные в формате CSV
        :param data: данные для записи
        :return: объект StringIO с данными в формате CSV
        """
        output = StringIO()
        writer = csv.writer(output)
        for row in data:
            writer.writerow(row)
        output.seek(0)
        return output
class YAMLWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в yaml формате."""

    def write(self, data: List[List[Tuple[int, str, float]]]) -> StringIO:
        """
        Записывает данные в формате YAML
        :param data: данные для записи
        :return: объект StringIO с данными в формате YAML
        """
        output = StringIO()
        yaml.dump(data, output)
        output.seek(0)
        return output


class DataGenerator:
    def __init__(self, data: List[List[Tuple[int, str, float]]] = None):
        self.data: List[List[Tuple[int, str, float]]] = data
        self.file_id = None

    def generate(self, matrix_size: int) -> None:
        """Генерирует матрицу данных заданного размера."""
        if matrix_size < 4 or matrix_size > 15:
            raise ValueError("Размер матрицы должен быть от 4 до 15")

        data = [[(i, str(i), float(i)) for i in range(matrix_size)] for _ in range(matrix_size)]
        self.data = data

    def to_file(self, path: str, writer: BaseWriter) -> None:
        """
        Метод для записи в файл данных полученных после генерации.
        Если данных нет, то вызывается кастомный Exception.
        :param path: Путь куда требуется сохранить файл
        :param writer: Одна из реализаций классов потомков от BaseWriter
        """
        if not self.data:
            raise ValueError("Нет данных для записи в файл")

        file_content = writer.write(self.data)
        with open(path, "w") as f:
            f.write(file_content.getvalue())