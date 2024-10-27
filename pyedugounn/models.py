from typing import List, Optional
from pydantic import BaseModel


class Homework(BaseModel):
    value: str
    id: int
    individual: bool


class Assessment(BaseModel):
    value: str
    countas: str
    color_hex: Optional[str]
    count: bool
    convert: int
    lesson_id: str
    date: str
    nm: str
    comment: str


class Item(BaseModel):
    homework: List[Homework] = []
    files: List[str] = []
    resources: List[str] = []
    name: str
    lesson_id: str
    num: str
    room: Optional[str] = ''
    teacher: str
    sort: int
    assessments: Optional[List[Assessment]] = None
    grp_short: Optional[str] = None
    grp: Optional[str] = None


class Day(BaseModel):
    name: str
    title: str
    items: List[Item]


class Student(BaseModel):
    name: str
    title: str
    days: List[Day]
