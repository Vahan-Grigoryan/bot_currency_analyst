import textwrap, utils
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


dp = Dispatcher()

@dp.message(Command("start"))
async def command_start_handler(message: Message):
    await message.answer(
        textwrap.dedent(
        f"""
        Hello, <b>{message.from_user.full_name}</b>!\n
        I can provide info about currencies in exchanges
        in many supermarkets/banks(sources) in Armenia  
        Available commands:

        /sources list sources from which data collected
        /currencies list all currencies values in each source(may take a while, please wait)
        /show_currency "currency_name" show the best choice of pointed currency(may take a while, please wait)
            for example "/show_currency USD"
        """
        )
    )


@dp.message(Command("sources"))
async def list_sources(message: Message):
    await message.answer(
        textwrap.dedent(
        f"""
        Sources are:

        SAS
        Zovq
        Unibank
        Araratbank
        Ameriabank
        HSBC bank
        ID bank
        VTB bank
        ACBA bank
        Converse bank
        Fast bank
        Ardshinbank
        Artsaxbank
        Byblos bank
        Evoca bank
        Ineco bank
        """
        )
    )

@dp.message(Command("currencies"))
async def currencies(message: Message):
    """Receive and show all currencies from each source"""

    answer_html = ""
    
    all_sources_currencies = await utils.get_currencies_list()

    for source_currencies in all_sources_currencies:
        answer_html += utils.render_template_for(source_currencies)


    await message.answer(textwrap.dedent(answer_html))

@dp.message(Command("show_currency"))
async def show_currency(message: Message):
    """Show pointed currency from each source, and the best one"""

    try:
        _, currency_name = message.text.split()
    except ValueError:
        await message.answer(
            "Provide currency name, example:\n/show_currency USD"
        )
        return

    all_sources_currencies = await utils.get_currencies_list(currency_name)
    answer_html = utils.get_best_choices(all_sources_currencies, currency_name)

    await message.answer(textwrap.dedent(answer_html))
