from bs4 import BeautifulSoup
from . import abstractions


class InecoBank(abstractions.Source):
    url = "https://www.inecobank.am/en/Individual"
    need_js_support = True
    available_currencies = ("USD", "EUR", "RUB")

    async def parse_html(self, task, currency_name = None):
        response = await task
        if response is None: return

        currencies_rate = {}
        parsed_html = BeautifulSoup(response, "html.parser")
        currency_rows = parsed_html.find_all(class_="currencyRatesContent")

        for currency_row in currency_rows:
            # iterate over each currency and it prices,
            # add currency to currencies_rate
            name, buy_price, sell_price = currency_row.stripped_strings
            if currency_name and not currency_name == name:
                continue
            else:
                currencies_rate[name] = {
                    "buy_price": float(buy_price),
                    "sell_price": float(sell_price),
                }
        return currencies_rate
