from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class EduGounnException(Exception):
    def __init__(self, data: dict):
        self.data = data


class Homework(BaseModel):
    value: str
    id: int
    individual: bool


class Assessment(BaseModel):
    value: int
    lesson_id: int
    date: str
    comment: Optional[str] = None


class File(BaseModel):
    id: int = Field(alias='toid')
    filename: str
    link: str


class Lesson(BaseModel):
    homeworks: List[Homework] = Field(alias='homework')
    files: List[File]
    name: str
    lesson_id: int
    num: int
    teacher: str
    sort: int
    room: Optional[str] = None
    group: Optional[str] = None
    start_time: datetime = Field(alias="starttime")
    end_time: datetime = Field(alias="endtime")

    @field_validator('start_time', "end_time", mode='before')
    def convert_to_time(cls, value):
        return datetime.strptime(value, '%H:%M:%S')


class AdditionalLesson(BaseModel):
    name: str
    sort: int
    group: Optional[str] = None
    teacher: str
    start_time: datetime = Field(alias="starttime")
    end_time: datetime = Field(alias="endtime")

    @field_validator('start_time', "end_time", mode='before')
    def convert_to_time(cls, value):
        return datetime.strptime(value, '%H:%M:%S')


class Day(BaseModel):
    date: datetime = Field(alias="name")
    alert: Optional[str] = None
    lessons: List[Lesson] = Field(alias="items")
    additional_lessons: list[AdditionalLesson] = Field([], alias="items_extday")

    @field_validator('date', mode='before')
    def convert_to_date(cls, value):
        return datetime.strptime(value, '%Y%m%d')
