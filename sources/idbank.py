from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class IDBank(abstractions.Source):
    url = "https://idbank.am/en/rates/"
    available_currencies = ("USD", "GBP", "RUB", "EUR", "GEL")

    async def parse_html(self, task: asyncio.Task):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find_all(class_="m-exchange__table-row")

        for currency_row in currency_rows[1:]:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price = currency_row.stripped_strings
            currencies_rate[name[2:]] = {
                "buy_price": float(buy_price),
                "sell_price": float(sell_price),
            }
        return currencies_rate
