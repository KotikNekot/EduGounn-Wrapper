from json import dumps
from logging import getLogger
from datetime import datetime
from typing import Any, overload

from aiohttp import ClientSession

from .models import Day, EduGounnException

logger = getLogger(__name__)


class EduGounn:
    def __init__(self, auth_token: str, developer_key: str, vendor: str) -> None:
        self._auth_token = auth_token
        self._developer_key = developer_key
        self._vendor = vendor

        self._BASE_URL = "https://edu.gounn.ru/apiv3/"
        self._PARAMS = {
            "vendor": self._vendor,
            "devkey": self._developer_key,
            "auth_token": self._auth_token,
        }

        # self._loop = get_event_loop()
        # self._session = self._loop.run_until_complete(self._create_session())
        self._session = ClientSession()

    @property
    def vendor(self) -> str:
        return self._vendor

    @property
    def developer_key(self) -> str:
        return self._developer_key

    @property
    def auth_token(self) -> str:
        return self._auth_token

    @staticmethod
    async def _create_session() -> ClientSession:
        return ClientSession()

    @staticmethod
    def _transform_dict_to_list(data: Any):
        if isinstance(data, list):
            return [EduGounn._transform_dict_to_list(item) for item in data]

        if isinstance(data, dict):
            processed_values = {key: EduGounn._transform_dict_to_list(value) for key, value in data.items()}

            if all(isinstance(key, str) and key.isdigit() for key in data.keys()):
                return list(processed_values.values())

            return processed_values

        return data

    @staticmethod
    def _convert_bool_to_str(data):
        if isinstance(data, bool):
            return "true" if data else "false"
        elif isinstance(data, dict):
            return {key: EduGounn._convert_bool_to_str(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [EduGounn._convert_bool_to_str(element) for element in data]
        else:
            return data

    async def _crate_request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        **other_params,
    ) -> dict:
        params = {
            **self._PARAMS,
            **(params or {}),
        }

        response = await self._session.request(
            method=method,
            url=self._BASE_URL + endpoint,
            params=self._convert_bool_to_str(params),
            **other_params,
        )
        logger.debug(
            f"Отправлен запрос: {self._BASE_URL + endpoint}, Параметры: {params}"
        )
        response_json = await response.json()

        response_data = response_json.get("response")
        error_data: dict = response_data.get("error", None)
        result_data = response_data.get("result")

        if error_data:
            logger.error(error_data)
            raise EduGounnException(error_data)

        return self._transform_dict_to_list(result_data)

    @overload
    async def get_diary(
        self,
        date_from: datetime,
        date_to: datetime,
        student: str,
        rings: bool = True
    ) -> list[Day]:
        ...

    @overload
    async def get_diary(
        self,
        date_from: datetime,
        date_to: datetime,
        student: str | None = None,
        rings: bool = True
    ) -> dict[str, list[Day]]:
        ...

    async def get_diary(
        self,
        date_from: datetime,
        date_to: datetime,
        student_id: str | None = None,
        rings: bool = True
    ) -> list[dict[str, list[Day]]] | list[Day]:
        """
        Получает расписание для заданного диапазона дат и ученика.

        :param date_from: Дата начала диапазона (тип: datetime).
        :param date_to: Дата окончания диапазона (тип: datetime).
        :param student_id: Идентификатор ученика (тип: str или None).
                          Если не указан, возвращаются данные всех учеников.
        :param rings: ?
        :return: Список словарей с данными дневника для каждого ученика,
                 где ключ — айди ученика, а значение - список объектов Day.
                 Если student_id указан, возвращается только список объектов Day для этого студента.
        """
        response = await self._crate_request(
            "GET",
            "getdiary",
            {
                "days": f"{date_from.strftime('%Y%m%d')}-{date_to.strftime('%Y%m%d')}",
                "rings": rings,
            }
        )

        diary = [
            {
                data.get("name"): [Day(**d) for d in data.get("days")]
            } for data in response.get("students")
        ]

        if not student_id:
            return diary

        return next((entry[student_id] for entry in diary if student_id in entry), None)
