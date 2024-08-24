import textwrap, asyncio
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

