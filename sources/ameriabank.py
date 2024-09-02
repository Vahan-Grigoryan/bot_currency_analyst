from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class AmeriaBank(abstractions.Source):
    url = "https://ameriabank.am/en/exchange-rates"
    available_currencies = (
        "USD", "JPY", "RUB", "EUR",
        "GBP", "CHF", "AUD", "CAD"
    )

    async def parse_html(self, task: asyncio.Task):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find(class_="exchange_wrapper").find_all(class_="Item")

        for currency_row in currency_rows:
            # iterate over each currency and it prices,
            # add currency into currencies_rate
            name, buy_price, sell_price, *_ = currency_row.stripped_strings
            try:
                currencies_rate[name] = {
                    "buy_price": float(buy_price),
                    "sell_price": float(sell_price),
                }
            except ValueError:
                pass

        return currencies_rate
