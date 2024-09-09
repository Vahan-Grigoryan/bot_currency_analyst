from bs4 import BeautifulSoup
from . import abstractions


class AmeriaBank(abstractions.Source):
    url = "https://ameriabank.am/en/exchange-rates"
    available_currencies = (
        "USD", "JPY", "RUB", "EUR",
        "GBP", "CHF", "AUD", "CAD"
    )

    async def parse_html(self, task, currency_name = None):
        response = await task
        if response is None:
            return

        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find(class_="exchange_wrapper").find_all(class_="Item")

        for currency_row in currency_rows:
            # iterate over each currency and it prices,
            # add currency into currencies_rate
            name, buy_price, sell_price, *_ = currency_row.stripped_strings
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
