from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class VTBBank(abstractions.Source):
    url = "https://www.vtb.am/ru/currency"
    available_currencies = (
        "USD", "EUR", "RUB", "GBP",
        "AUD", "CHF", "GEL", "XAU"
    )

    async def parse_html(self, task: asyncio.Task):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find(class_="exchange-rate-table_no-width").find_all("tr")

        for currency_row in currency_rows[1:]:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            _, name, buy_price, sell_price = currency_row.stripped_strings
            try:
                currencies_rate[name] = {
                    "buy_price": float(buy_price),
                    "sell_price": float(sell_price),
                }
            except ValueError:
                pass

        return currencies_rate

