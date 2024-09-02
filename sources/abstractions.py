from abc import ABC, abstractmethod
from asyncio import Task
from httpx import AsyncClient, Response


class Source(ABC):
    url = ""

    async def get_response(self) -> Response:
        """Receive page html without js rendering support"""
        async with AsyncClient() as client:
            return await client.get(self.url)

    async def get_response_with_js_rendering(self, browser) -> str:
        """Receive browser and return page html with js rendering support"""
        page = await browser.newPage()
        await page.setViewport({"width":1920, "height":1080})
        await page.goto(self.url)
        html = await page.content()
        return html

    @abstractmethod
    async def parse_html(self, task: Task) -> dict:
        """
        Each source have html parsing method.
        Will return source currencies as key: value pairs, like:
            {
                ...
                "USD": {"buy_price":400.0, "sell_price": 400.0}
                ...
            }
        """
        pass
