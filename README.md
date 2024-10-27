# EduGounn

EduGounn — это библиотека для работы с электронным дневником, доступным в Нижегородской области. Она предоставляет возможность получать данные о расписании, домашних заданиях, оценках и других элементах, доступных в электронном дневнике. Библиотека имеет только один метод `get_diary`, который можно использовать как для получения данных по списку учеников, так и для отдельного ученика, указывая его ID.

## Важно!
С недавних пор авторизация по логину и паролю недоступна. Использование авторизации через госуслуги в рамках этой библиотеки признано нецелесообразным. Поэтому предлагаем обходной способ получения данных о сессии.

### Инструкция по авторизации
1. Авторизуйтесь в электронном дневнике через браузер.
2. Установите приложение [HTTP Canary](https://www.httpcanary.com/) для перехвата запросов и установите его SSL-сертификат для работы с зашифрованными данными.
3. Откройте дневник и перехватите любой запрос, связанный с ним, через HTTP Canary.
4. В запросе вы найдете необходимые параметры: `auth_token`, `developer_token`, `vendor`. Эти параметры потребуются для работы библиотеки.

## Установка

Установите библиотеку через `pip`:

```bash
pip install git+https://github.com/KotikNekot/EduGounn-Wrapper.git
```

## Использование

Основной метод `get_diary` перегружен: он работает с данными для списка всех учеников или только для одного ученика при указании его ID в параметрах. Библиотека полностью типизирована, и интерфейс интуитивно понятен.

### Пример использования

```python
from pyedugounn import EduGounn

# Инициализация сессии
eg = EduGounn(
    auth_token="токен_авторизации",
    developer_token="токен_разработчика",
    vendor="вендор_школы"
)

# Получение данных по всем ученикам, если у вас отображаются тайп хинты, то из-за перегрузки будет возвращаться список 
# учеников, что облегчит задачу
students = await eg.get_diary()

for student in students:
    print(student.name)

# Но если указать айди нужного ученика, то из списка всех учеников, библиотека найдет айди указанного, и тайпхинты 
# будут показывать то что у вас именно один объект ученика 
student = await eg.get_diary(student_id="12345")
print(student.name)


```

## Модели данных

Вот описание основных моделей данных, с которыми работает EduGounn:

```python
from pydantic import BaseModel
from typing import List, Optional

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
```


Библиотека написано сугубо на энтузиазме, возможно чуть позже я допишу ее, но пока в этом нет никакой нужды

Вот список задач для доработки библиотеки EduGounn на основе предоставленного снимка запросов:

### TODO

1. **Переделать модели данных**
   
2. **Добавить методы**
     - `get_periods`
     - `get_board_notices`
     - `get_marks`
     - `get_final_assessments`
     - `get_schedule`
     - `get_profile_info`
   
3. **Добавить кэширование запросов**
4. **Добавить обработку ошибок и логирование**
5. **Создать документацию по мере разрастания библиотеки**
6. **Может быть, но прям вот нет, добавить аунтефикацию через гос услуги**