import asyncio, os
from handlers import dp
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


load_dotenv()
    
async def main() -> None:
    bot = Bot(
        token=os.getenv("BOT_TOKEN", "_"),
    	default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

