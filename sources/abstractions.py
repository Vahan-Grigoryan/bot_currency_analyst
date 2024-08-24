from abc import ABC, abstractmethod
from asyncio import Task
from httpx import Response


class Source(ABC):
    @abstractmethod
    async def get_response(self) -> Response:
        pass

    @abstractmethod
    async def parse_html(self, task: Task) -> dict:
        pass
