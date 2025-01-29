"""Main module for my own wrote A-Parser lib"""
import asyncio
import json
import logging
from typing import Literal
import httpx

from . import schemas
from .exceptions import AParserReqError, AParserRequestNotSuccess, AParserTimeoutError, AParserError
from .schemas import TaskChangeStatus

__all__ = ("AParser",)

logger = logging.getLogger(__name__)


class AParser:
    """Класс, позволяющий работать с некоторыми методами API A-Parser async/await"""

    def __init__(self, address: str, password: str, port: int = 9091):
        self.address = address
        self.port = port
        self.password = password
        self.endpoint = f"{address}:{port}/API"

    async def send(self, json_data):
        """Метод, отправляющий json по нужному адресу A-Parser"""
        async with httpx.AsyncClient() as client:
            try:
                result = await client.post(self.endpoint, data=json_data, timeout=10)
                result.raise_for_status()
            except httpx.HTTPError as e:
                raise AParserReqError(e) from e

        parsed_response = json.loads(result.text)

        if parsed_response["success"] != 1:
            logger.error(parsed_response)
            raise AParserRequestNotSuccess("Got error success != 1")

        return parsed_response.get("data")

    async def ping(self):
        """Базовый метод проверки работоспособности API и правильной настройки системы - ждем в ответ pong"""
        json_data = schemas.PingRequest(
            password=self.password
        ).model_dump_json()

        logger.info(json_data)
        resp_data = await self.send(json_data)
        return resp_data

    async def add_task(self, data: schemas.Data) -> int:
        """
        Добавить задачу в очередь
        :param data: данные по задачи
        :return: id задачи
        """
        data = schemas.AddTaskRequest(
            password=self.password,
            data=data
        )

        logger.info(data.model_dump_json(indent=1))
        resp_data = await self.send(data.model_dump_json())

        return int(resp_data)

    async def get_task_state(self, task_id: int) -> schemas.TaskStatus:
        """
        Получаем статус задачи
        :param task_id: id задачи
        :return: статус и некоторые прочие параметры
        """
        json_data = schemas.GetTaskState(
            password=self.password,
            data=schemas.TaskUidData(taskUid=task_id)
        ).model_dump_json()

        resp_data = await self.send(json_data)

        status = schemas.TaskStatus(**resp_data)
        logger.info(f"Got {status.status} for {task_id}")
        return status

    async def change_task_state(self, task_id: int, state: TaskChangeStatus) -> None:
        data = schemas.ChangeTaskStatus(
            password=self.password,
            data=schemas.ToStatus(taskUid=task_id, toStatus=state)
        ).model_dump_json()

        await self.send(data)

    async def try_to_delete_task(self, task_id: int) -> None:
        try:
            await self.change_task_state(task_id, TaskChangeStatus.DELETING)
        except AParserError:
            logger.warning(f"Can't delete task {task_id}")

    async def wait_for_task(self, task_id, delay=1, timeout=None):
        """
        Метод, асинхронно ожидающий пока статус задача не завершится,
         выбрасывает AParserError если задача завершилась с ошибкой
        :param task_id: id задачи
        :param delay: интервал проверки
        :param timeout: максимальное время ожидания (None - бесконечно)
        :return: None
        """
        time_passed = 0
        while True:
            task_status = await self.get_task_state(task_id=task_id)
            if task_status.status == "completed":
                break

            if task_status.status not in ["work", "starting", "waitSlot"]:
                logger.warning(f"Task {task_id} finished with status {task_status.status}, trying to delete...")
                await self.try_to_delete_task(task_id)
                raise AParserRequestNotSuccess("Task finished with error")
            if timeout is not None and time_passed > timeout:
                logger.warning(f"Timeout exceeded for task {task_id}, trying to delete...")
                await self.try_to_delete_task(task_id)
                raise AParserTimeoutError("Timeout exceeded")

            await asyncio.sleep(delay)

            if task_status.status in ["work", "starting"]:
                time_passed += delay

    async def get_task_result_file(self, task_id: int) -> str:
        """
        Получить одноразовую ссылку на файл с результатом выполнения задачи
        :param task_id: id задачи
        :return: url файла
        """
        json_data = schemas.GetTaskResultFile(
            password=self.password,
            data=schemas.TaskUidData(taskUid=task_id)
        ).model_dump_json()

        logger.info(json_data)
        resp_data = await self.send(json_data)

        return str(resp_data)

    async def delete_task_result_file(self, task_id: int) -> bool:
        """
        Удалить файл с результатом выполнения задачи
        :param task_id: id задачи
        :return: None
        """
        json_data = schemas.DeleteTaskResultFile(
            password=self.password,
            data=schemas.TaskUidData(taskUid=task_id)
        ).model_dump_json()

        logger.info(json_data)
        await self.send(json_data)

        return True

    @staticmethod
    async def load_file(url: str) -> str:
        """
        Загрузить файл по указанному адресу
        :param url: url файла
        :return: содержимое файла
        """
        async with httpx.AsyncClient() as client:
            try:
                result = await client.get(url, timeout=10)
            except httpx.HTTPError as e:
                raise AParserReqError(e) from e
        if result.status_code not in [200, 201]:
            raise AParserReqError(f"Got error status code from A-Parser, {result.status_code}")

        return result.text

    async def change_proxy_checker_state(self, checker: str, state: Literal[0, 1]):
        """
        Метод, изменяющий состояние проксичекера
        :param checker: имя проксичекера
        :param state: новый статус (0 - выкл./ 1 - вкл.)
        :return: None
        """
        data = schemas.ChangeProxyCheckerState(
            password=self.password,
            data=schemas.ProxyCheckerState(checker=checker, state=state)
        )
        data_json = data.model_dump_json()
        logger.info(data_json)
        await self.send(data_json)
