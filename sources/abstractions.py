from abc import ABC, abstractmethod
from asyncio import Task
from httpx import AsyncClient, Response, TimeoutException as HttpxTimeoutError
from pyppeteer.errors import TimeoutError as PyppeteerTimeoutError


class Source(ABC):
    url = ""
    need_js_support = False
    available_currencies = ()

    async def get_response(self) -> Response | None:
        """ Receive page html without js rendering support """
        async with AsyncClient() as client:
            try:
                return await client.get(self.url)
            except HttpxTimeoutError:
                return

    async def get_response_with_js_rendering(self, browser) -> str | None:
        """Receive browser and return page html with js rendering support"""
        page = await browser.newPage()
        await page.setViewport({"width":1920, "height":1080})
        await page.setJavaScriptEnabled(True)

        try:
            await page.goto(self.url, {"timeout": 15000})
        except PyppeteerTimeoutError:
            return

        html = await page.content()
        return html

    @abstractmethod
    async def parse_html(
        self,
        task: Task,
        currency_name: str | None = None
    ) -> dict | None:
        """
        Each source have this html parsing method.
        Will return source currencies os currency(if currency_name) as key: value pairs, like:
            {
                ...
                "USD": {"buy_price":400.0, "sell_price": 400.0}
                ...
            }
        """
        pass
