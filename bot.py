import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

# Keep the bot token in an environment variable, e.g. BOT_TOKEN,
# and pass it during startup: BOT_TOKEN=<your_token> python bot.py
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Export it before starting the bot.")

dp = Dispatcher()

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Русский")],
        [KeyboardButton(text="Казахский")],
        [KeyboardButton(text="Английский")],
    ],
    resize_keyboard=True,
)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    bot_info = await message.bot.get_me()
    bot_name = bot_info.first_name or bot_info.username or "бот"

    await message.answer(
        f"Здравствуйте Я {bot_name}, выберите язык",
        reply_markup=language_keyboard,
    )


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())