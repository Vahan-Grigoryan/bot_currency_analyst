from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class FastBank(abstractions.Source):
    url = "https://www.fastbank.am/en/currency-exchange"
    need_js_support = True
    available_currencies = (
        "USD", "RUB", "EUR",
        "GEL", "GBP", "AED"
    )

    async def parse_html(self, task, currency_name = None):
        response = await task
        if response is None: return

        currencies_rate = {}
        parsed_html = BeautifulSoup(response, "html.parser")
        currency_rows = parsed_html.find(id="rates-table").find_all("tr")

        for currency_row in currency_rows[1:]:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            _, name, buy_price, sell_price = currency_row.stripped_strings
            if currency_name and not currency_name == name:
                continue
            else:
                currencies_rate[name] = {
                    "buy_price": float(buy_price),
                    "sell_price": float(sell_price),
                }
        return currencies_rate
