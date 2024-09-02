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

async def get_currencies_list_with_chrome():
    """
    Run chrome instance and receive html of pages with js support,
    pass htmls to sources and receive currencies and return them.
    """
    launcher = Launcher({
        "executablePath": rf"{os.getenv('CHROME_PATH')}",
    })
    browser = await launcher.launch()
    currencies = []

    async with asyncio.TaskGroup() as tg:
        ardshinbank, ardshinbank_task = create_task_of_source(sources.ArdshinBank, tg, browser)
        araratbank, araratbank_task = create_task_of_source(sources.AraratBank, tg, browser)
        fastbank, fastbank_task = create_task_of_source(sources.FastBank, tg, browser)
        conversebank, conversebank_task = create_task_of_source(sources.ConverseBank, tg, browser)
        inecobank, inecobank_task = create_task_of_source(sources.InecoBank, tg, browser)

        currencies.append({inecobank: await inecobank.parse_html(inecobank_task)})
        currencies.append({ardshinbank: await ardshinbank.parse_html(ardshinbank_task)})
        currencies.append({araratbank: await araratbank.parse_html(araratbank_task)})
        currencies.append({fastbank: await fastbank.parse_html(fastbank_task)})
        currencies.append({conversebank: await conversebank.parse_html(conversebank_task)})

    await browser.close()
    await launcher.killChrome()
    return currencies

async def get_currencies_list():
    """Get all currencies from all sources"""
    currencies = []

    async with asyncio.TaskGroup() as tg:
        sas, sas_task = create_task_of_source(sources.SAS, tg)
        zovq, zovq_task = create_task_of_source(sources.Zovq, tg)
        unibank, unibank_task = create_task_of_source(sources.UniBank, tg)
        ameriabank, ameriabank_task = create_task_of_source(sources.AmeriaBank, tg)
        hsbcbank, hsbcbank_task = create_task_of_source(sources.HSBCBank, tg)
        idbank, idbank_task = create_task_of_source(sources.IDBank, tg)
        vtbbank, vtbbank_task = create_task_of_source(sources.VTBBank, tg)
        acbabank, acbabank_task = create_task_of_source(sources.ACBABank, tg)
        #artsaxbank, artsaxbank_task = create_task_of_source(sources.ArtsaxBank, tg)
        byblosbank, byblosbank_task = create_task_of_source(sources.ByblosBank, tg)
        evocabank, evocabank_task = create_task_of_source(sources.EvocaBank, tg)

        currencies.append({sas: await sas.parse_html(sas_task)})
        currencies.append({zovq: await zovq.parse_html(zovq_task)})
        currencies.append({unibank: await unibank.parse_html(unibank_task)})
        currencies.append({ameriabank: await ameriabank.parse_html(ameriabank_task)})
        currencies.append({hsbcbank: await hsbcbank.parse_html(hsbcbank_task)})
        currencies.append({idbank: await idbank.parse_html(idbank_task)})
        currencies.append({vtbbank: await vtbbank.parse_html(vtbbank_task)})
        currencies.append({acbabank: await acbabank.parse_html(acbabank_task)})
        #currencies.append({artsaxbank: await artsaxbank.parse_html(artsaxbank_task)})
        currencies.append({byblosbank: await byblosbank.parse_html(byblosbank_task)})
        currencies.append({evocabank: await evocabank.parse_html(evocabank_task)})
    

    currencies.extend(await get_currencies_list_with_chrome())
    return currencies


def render_template_for(source_currencies):
    """Create and return html for source currencies"""
    source_instance, source_currencies = tuple(source_currencies.items())[0]
    html = f"{source_instance.__class__.__name__}:\n<pre>{'':<3}|{'buy':<6}|{'sell':<6}\n"
    
    for currency_name, currency_prices in source_currencies.items():
        html += f"{currency_name}| {currency_prices['buy_price']:<6} | {currency_prices['sell_price']:<6}\n"

    html+="</pre>\n"
    return html


