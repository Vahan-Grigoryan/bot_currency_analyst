from bs4 import BeautifulSoup
from . import abstractions


class IDBank(abstractions.Source):
    url = "https://idbank.am/en/rates/"
    available_currencies = ("USD", "GBP", "RUB", "EUR", "GEL")

    async def parse_html(self, task, currency_name = None):
        response = await task
        if response is None: return

        currencies_rate = {}
        parsed_html = BeautifulSoup(await response.aread(), "html.parser")
        currency_rows = parsed_html.find_all(class_="m-exchange__table-row")

        for currency_row in currency_rows[1:]:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price = currency_row.stripped_strings
            if currency_name and not currency_name == name[2:]:
                continue
            else:
                currencies_rate[name[2:]] = {
                    "buy_price": float(buy_price),
                    "sell_price": float(sell_price),
                }
        return currencies_rate
