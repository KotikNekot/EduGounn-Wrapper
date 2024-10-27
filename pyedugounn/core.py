from asyncio import get_event_loop
from datetime import datetime
from typing import Any, overload

from aiohttp import ClientSession

from pyedugounn.models import Student


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
        response_json = await response.json()


        response_data = response_json.get("response")
        result_data = response_data.get("result")

        return self._transform_dict_to_list(result_data)

    @overload
    async def get_diary(
        self,
        date_from: datetime,
        date_to: datetime,
        student: str,
        rings: bool = True
    ) -> Student:
        ...

    @overload
    async def get_diary(
        self,
        date_from: datetime,
        date_to: datetime,
        student: str | None = None,
        rings: bool = True
    ) -> list[Student]:
        ...

    async def get_diary(
        self,
        date_from: datetime,
        date_to: datetime,
        student_id: str | None = None,
        rings: bool = True
    ) -> list[Student] | Student | None:
        response = await self._crate_request(
            "GET",
            "getdiary",
            {
                "days": f"{date_from.strftime('%Y%m%d')}-{date_to.strftime('%Y%m%d')}",
                "rings": rings,
            }
        )
        students = [Student(**data) for data in response.get("students")]

        if not student_id:
            return students

        return next((student for student in students if student.name == student_id), None)
