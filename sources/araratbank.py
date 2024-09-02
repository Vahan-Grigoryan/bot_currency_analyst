from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class AraratBank(abstractions.Source):
    url = "https://araratbank.am/hy/"
    available_currencies = (
        "USD", "EUR", "RUB",
        "GBP", "CHF", "GEL",
        "CAD", "AUD", "AED"
    )

    async def parse_html(self, task: asyncio.Task):
        """Receive task, await it, receive html of page, parse it and return currencies"""
        response = await task
        currencies_rate = {}
        parsed_html = BeautifulSoup(response, "html.parser")
        currency_rows = parsed_html.find_all(class_="exchange__table-cell")
        for i in range(4, (len(currency_rows) // 4)+4, 4):
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price = currency_rows[i:i+3]
            currencies_rate[name.string] = {
                "buy_price": float(buy_price.string),
                "sell_price": float(sell_price.string),
            }
        return currencies_rate

