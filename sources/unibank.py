from bs4 import BeautifulSoup
from . import abstractions


class UniBank(abstractions.Source):
    url = "https://www.unibank.am/hy/"
    available_currencies = ("USD", "GBP", "RUB", "EUR")

    async def parse_html(self, task, currency_name = None):
        response = await task
        if response is None: return

        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find(class_="pane__body").find_all("li")

        for i in range(1, len(currency_rows), 3):
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price = currency_rows[i:i+3]
            if currency_name and not currency_name == name.string:
                continue
            else:
                currencies_rate[name.string] = {
                    "buy_price": float(buy_price.string),
                    "sell_price": float(sell_price.string),
                }
        return currencies_rate

