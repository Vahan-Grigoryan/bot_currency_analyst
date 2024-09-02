from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class ArtsaxBank(abstractions.Source):
    url = "https://www.artsakhbank.am/"
    available_currencies = (
        "USD", "EUR", "RUR", "CHF",
        "GEL", "GBP", "CAD"
    )

    async def parse_html(self, task: asyncio.Task):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find(class_="exchange_list").find_all("ul")

        for currency_row in currency_rows:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price, _ = currency_row.stripped_strings
            currencies_rate[name] = {
                "buy_price": float(buy_price),
                "sell_price": float(sell_price),
            }
        return currencies_rate
