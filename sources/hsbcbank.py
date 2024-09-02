from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class HSBCBank(abstractions.Source):
    url = "https://www.hsbc.am/en-am/help/rates/"
    available_currencies = (
        "AED", "AUD", "CAD", "CHF", "EUR",
        "GBP", "HKD", "JPY", "RUB", "USD"
    )

    async def parse_html(self, task: asyncio.Task):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find(class_="desktop").find_all("tr")[1:]

        for currency_row in currency_rows:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, _, _, buy_price, sell_price = currency_row.stripped_strings
            try:
                currencies_rate[name] = {
                    "buy_price": float(buy_price),
                    "sell_price": float(sell_price),
                }
            except ValueError:
                pass

        return currencies_rate
