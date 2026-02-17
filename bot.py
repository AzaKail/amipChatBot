import asyncio
import logging
import os
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup


def load_token() -> str:
    token = os.getenv("BOT_TOKEN")
    if token:
        return token

    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            if key.strip() != "BOT_TOKEN":
                continue

            clean_value = value.strip().strip('"').strip("'")
            if clean_value:
                os.environ["BOT_TOKEN"] = clean_value
                return clean_value

    raise RuntimeError(
        "BOT_TOKEN is not set. Add it to environment variables or create .env with BOT_TOKEN=<your_token>."
    )


TOKEN = load_token()
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