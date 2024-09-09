import os, asyncio, sources
from pyppeteer.launcher import Browser, Launcher


def create_task_of_source(
    source,
	task_group,
	browser: Browser | None = None
):
    """Create source instance and task for receiving response, return both"""
    source_instance = source()

    if browser:
        source_task = task_group.create_task(
            source_instance.get_response_with_js_rendering(browser)
        )
    else:
        source_task = task_group.create_task(
            source_instance.get_response()
        )

    return source_instance, source_task


async def get_currencies_list(for_currency: str | None = None) -> \
    list[dict[str, dict[str, dict[str, int] | None]]]:
    """Get all currencies or pointed currency from each source"""
    currencies = []

    sources_list = (
        sources.SAS,
        sources.Zovq,
        sources.UniBank,
        sources.AmeriaBank,
        sources.HSBCBank,
        sources.IDBank,
        sources.VTBBank,
        sources.ACBABank,
        sources.ArtsaxBank,
        sources.ByblosBank,
        sources.EvocaBank,
        sources.ArdshinBank,
        sources.AraratBank,
        sources.FastBank,
        sources.ConverseBank,
        sources.InecoBank,
    )
    # source instances and tasks will be stored there
    sources_data = []

    launcher = Launcher({
        "executablePath": os.getenv("CHROME_PATH"),
    })
    browser = await launcher.launch()

    async with asyncio.TaskGroup() as tg:
        for source in sources_list:
            if not source.need_js_support:
                sources_data.append(
                    create_task_of_source(source, tg)
                )
                continue

            sources_data.append(
                create_task_of_source(source, tg, browser)
            )

        for source_instance, source_task in sources_data:
            if for_currency and for_currency not in source_instance.available_currencies:
                continue

            source_name = source_instance.__class__.__name__
            source_currencies = await source_instance.parse_html(source_task, for_currency)

            # change RUR to RUB for valid filtering
            if source_currencies and "RUR" in source_currencies:
                source_currencies["RUB"] = source_currencies.pop("RUR")

            currencies.append({
                source_name: source_currencies
            })
            
    await browser.close()
    await launcher.killChrome()

    return currencies


def render_template_for(source_currencies) -> str:
    """Create and return html for source currencies"""
    source_instance, source_currencies = tuple(source_currencies.items())[0]

    if not source_currencies:
        return f"{source_instance}\nsource temporary unavailable...\n\n"

    html = f"{source_instance}:\n<pre>{'':<3}| {'buy':<6} | {'sell':<6}\n"
    
    for currency_name, currency_prices in source_currencies.items():
        html += f"{currency_name}| {currency_prices['buy_price']:<6} | {currency_prices['sell_price']:<6}\n"

    html+="</pre>\n"
    return html


def get_best_choices(all_sources_currencies, currency_name) -> str:
    """
    Evaluate the best ones for pointed currency for "buy" and "sell".
    """
    answer_html = ""
    first_source = tuple(all_sources_currencies[0].items())[0]

    best_buy_choice = (
        [first_source[0]],
        first_source[1][currency_name]["buy_price"]
    )
    best_sell_choice = (
        [first_source[0]],
        first_source[1][currency_name]["sell_price"]
    )

    for source_currencies in all_sources_currencies[1:]:
        answer_html += render_template_for(source_currencies)
        
        name, currencies = tuple(source_currencies.items())[0]

        if not currencies:
            continue

        if currencies[currency_name]["buy_price"] > best_buy_choice[1]:
            best_buy_choice = ([name], currencies[currency_name]["buy_price"])
        elif currencies[currency_name]["buy_price"] == best_buy_choice[1]:
            best_buy_choice[0].append(name)

        if currencies[currency_name]["sell_price"] < best_sell_choice[1]:
            best_sell_choice = ([name], currencies[currency_name]["sell_price"])
        elif currencies[currency_name]["sell_price"] == best_sell_choice[1]:
            best_sell_choice[0].append(name)


    answer_html += \
    f"""
    The best buy choice: {best_buy_choice[1]}(in {", ".join(best_buy_choice[0])})
    The best sell choice: {best_sell_choice[1]}(in {", ".join(best_sell_choice[0])})
    """
    
    return answer_html
