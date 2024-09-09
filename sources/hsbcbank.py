from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class HSBCBank(abstractions.Source):
    url = "https://www.hsbc.am/en-am/help/rates/"
    available_currencies = (
        "AED", "AUD", "CAD", "CHF", "EUR",
        "GBP", "HKD", "JPY", "RUB", "USD"
    )

    async def parse_html(self, task, currency_name = None):
        response = await task
        if response is None: return

        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find(class_="desktop").find_all("tr")[1:]

        for currency_row in currency_rows:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, _, _, buy_price, sell_price = currency_row.stripped_strings
            try:
                if currency_name and not currency_name == name:
                    continue
                else:
                    currencies_rate[name] = {
                        "buy_price": float(buy_price),
                        "sell_price": float(sell_price),
                    }
            except ValueError:
                pass

        return currencies_rate
