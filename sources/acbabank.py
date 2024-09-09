from bs4 import BeautifulSoup
from . import abstractions


class ACBABank(abstractions.Source):
    url = "https://www.acba.am/"
    available_currencies = (
        "USD", "RUR", "EUR",
        "GBP", "GEL", "CHF",
    )

    async def parse_html(self, task, currency_name = None):
        response = await task
        if response is None:
            return

        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find_all(class_="simple_price-row")

        for currency_row in currency_rows[1:7]:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price, _ = currency_row.stripped_strings
            
            if currency_name and not currency_name == name:
                continue
            else:
                currencies_rate[name] = {
                    "buy_price": float(buy_price),
                    "sell_price": float(sell_price),
                }

        return currencies_rate

