from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class ACBABank(abstractions.Source):
    url = "https://www.acba.am/"
    available_currencies = (
        "USD", "RUR", "EUR",
        "GBP", "GEL", "CHF",
    )

    async def parse_html(self, task: asyncio.Task):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find_all(class_="simple_price-row")

        for currency_row in currency_rows[1:7]:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price, _ = currency_row.stripped_strings
            currencies_rate[name] = {
                "buy_price": float(buy_price),
                "sell_price": float(sell_price),
            }
        return currencies_rate

