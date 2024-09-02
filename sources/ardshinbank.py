from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class ArdshinBank(abstractions.Source):
    url = "https://ardshinbank.am/?lang=en"
    available_currencies = ("USD", "EUR", "RUR", "GBP", "CHF")

    async def parse_html(self, task: asyncio.Task):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        currencies_rate = {}
        parsed_html = BeautifulSoup(response, "html.parser")
        currency_rows = parsed_html.find(class_="currency").find_all("tr")

        for currency_row in currency_rows[1:]:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price = list(currency_row.stripped_strings)[:-1]
            currencies_rate[name] = {
                "buy_price": float(buy_price),
                "sell_price": float(sell_price),
            }
        return currencies_rate
