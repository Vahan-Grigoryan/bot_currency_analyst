from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class SAS(abstractions.Source):
    url = "https://www.sas.am/"
    available_currencies = (
        "USD", "USD1", "RUR", "EUR",
        "GBP", "GEL", "AED", "CHF",
        "UAH", "AUD", "CAD"
    )

    async def parse_html(self, task, currency_name = None):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        if response is None: return

        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find_all(class_="exchange-table__row")

        for currency_row in currency_rows[1:]:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price = currency_row.stripped_strings
            if currency_name and not currency_name == name:
                continue
            else:
                currencies_rate[name] = {
                    "buy_price": float(buy_price),
                    "sell_price": float(sell_price),
                }

        return currencies_rate
