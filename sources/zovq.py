from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class Zovq(abstractions.Source):
    url = "https://norzovq.am"
    available_currencies = (
        "USD", "EUR", "RUR",
        "GBP", "GEL", "CHF",
        "AED", "CAD", "AUD"
    )

    async def parse_html(self, task: asyncio.Task):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find_all(class_="exchange-table__cell-content")

        for i in range(3, len(currency_rows) // 2, 3):
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price = currency_rows[i:i+3]
            currencies_rate[name.string] = {
                "buy_price": float(buy_price.string),
                "sell_price": float(sell_price.string),
            }
        return currencies_rate
