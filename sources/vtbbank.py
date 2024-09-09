from bs4 import BeautifulSoup
from . import abstractions
import asyncio


class VTBBank(abstractions.Source):
    url = "https://www.vtb.am/ru/currency"
    available_currencies = (
        "USD", "EUR", "RUB", "GBP",
        "AUD", "CHF", "GEL", "XAU"
    )

    async def parse_html(self, task, currency_name = None):
        response = await task
        if response is None: return

        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find(class_="exchange-rate-table_no-width").find_all("tr")

        for currency_row in currency_rows[1:]:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            _, name, buy_price, sell_price = currency_row.stripped_strings
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

