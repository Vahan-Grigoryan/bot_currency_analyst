from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class InecoBank(abstractions.Source):
    url = "https://www.inecobank.am/en/Individual"
    available_currencies = ("USD", "EUR", "RUB")

    async def parse_html(self, task: asyncio.Task):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        currencies_rate = {}
        parsed_html = BeautifulSoup(response, "html.parser")
        currency_rows = parsed_html.find_all(class_="currencyRates__item currencyRatesContent")

        for currency_row in currency_rows:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price = currency_row.stripped_strings
            currencies_rate[name] = {
                "buy_price": float(buy_price),
                "sell_price": float(sell_price),
            }
        return currencies_rate
