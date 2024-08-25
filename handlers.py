import textwrap, asyncio, sources
from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        textwrap.dedent(
        f"""
        Hello, <b>{message.from_user.full_name}</b>!\n
        I can provide info about currencies in exchanges
        in many supermarkets/banks(sources) in Armenia  
        Available commands:

        /list_sources list sources from which data collected
        /currencies list all currencies values in each source(and the best choice) 
        /show_currency show pointed currency in each source(and the best choice) 
        """
        )
    )


@dp.message(Command("list_sources"))
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
        Inecobank
        Mellatbank
        """
        )
    )

@dp.message(Command("currencies"))
async def currencies(message: Message):
    async with asyncio.TaskGroup() as tg:
        sas = sources.SAS()
        sas_response = tg.create_task(
            sas.get_response()
        )
        zovq = sources.Zovq()
        zovq_response = tg.create_task(
            zovq.get_response()
        )

        sas_currencies = await sas.parse_html(sas_response)
        zovq_currencies = await zovq.parse_html(zovq_response)

        print("\nSAS:\n", sas_currencies)
        print("\nZovq:\n", zovq_currencies)
