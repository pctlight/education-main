from typing import Union, List
from pydantic import BaseModel, field_validator
from datetime import datetime


###2task
class ConverterRequest(BaseModel):
    number: Union[int, str]


class ConverterResponse(BaseModel):
    arabic: int
    roman: str


class DataRequest(BaseModel):
    file_type: str
    matrix_size: int


class FileIDResponse(BaseModel):
    id: int


class FileStorage:
    _instance = None
    file_dict = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


###3task
class User(BaseModel):
    name: str
    age: int
    adult: bool
    message: str = None
    # @field_validator('age')
    # @classmethod
    # def age_must_be_between_0_and_100(cls, value: int) -> int:
    #     if not 0 <= value <= 100:
    #         raise ValueError('age must be between 0 and 100')
    #     return value
    #
    #
    # @field_validator('age', 'adult')
    # @classmethod
    # def age_must_be_integer(cls, age: int, adult: bool) -> bool:
    #     if age < 18 and adult is True:
    #         raise ValueError('значение adult указано неверно, adult = False')
    #     elif age >= 18 and adult is False:
    #         raise ValueError('значение adult указано неверно, adult = True')
    #     return adult


class Mapping(BaseModel):
    list_of_ids: List
    tags: List[str]

class Meta(BaseModel):
    last_modification: str
    list_of_skills: List[str] = None
    mapping: Mapping

class BigJson(BaseModel):
    user: User
    meta: Meta

    @field_validator('user')
    @classmethod
    def age_must_be_between_0_and_100(cls, value: User) -> User:
        if not 0 <= value.age <= 100:
            raise ValueError('age must be between 0 and 100')
        return value


    @field_validator('user')
    @classmethod
    def age_must_be_integer(cls, value: User) -> User:
        if value.age < 18 and value.adult is True:
            raise ValueError('значение adult указано неверно, adult = False')
        elif value.age >= 18 and value.adult is False:
            raise ValueError('значение adult указано неверно, adult = True')
        return value

    @field_validator('meta')
    @classmethod
    def validate_meta(cls, value: Meta) -> Meta:
        if len(value.last_modification.split('/')) != 3:
            raise ValueError('Неправильный формат разделения даты, измените на DD/MM/YYYY')
        else:
            try:
                value.last_modification = datetime.strptime(value.last_modification, "%d/%m/%Y")
            except ValueError:
                raise ValueError('Дата указана неверно, корректный формат DD/MM/YYYY')
        return value

