import textwrap, utils
from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


dp = Dispatcher()

@dp.message(CommandStart())
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
        /show_currency show the best choice of pointed currency(may take a while, please wait) 
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
    """Receive and show all currencies"""
    answer_html = ""
    
    all_sources_currencies = await utils.get_currencies_list()

    for source_currencies in all_sources_currencies:
        answer_html += utils.render_template_for(source_currencies)


    await message.answer(textwrap.dedent(answer_html))
