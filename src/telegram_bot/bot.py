import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "http://localhost:8000/generate-logo"

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

class LogoStates(StatesGroup):
    waiting_for_prompt = State()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для генерации логотипов.\n"
        "Просто отправь мне текстовое описание логотипа, который ты хочешь создать."
    )

@dp.message()
async def handle_message(message: Message):
    try:
        # Show "typing" status
        await bot.send_chat_action(
            chat_id=message.chat.id,
            action="typing"
        )
        
        # Send request to FastAPI service
        response = requests.post(
            API_URL,
            json={"prompt": message.text}
        )
        
        if response.status_code == 200:
            # Send the generated image
            photo = FSInputFile("generated_logo.png")
            
            await message.answer_photo(
                    photo=photo,
                    caption="Вот ваш логотип! 🎨"
                )
        else:
            await message.answer(
                "Извините, произошла ошибка при генерации логотипа. Попробуйте еще раз."
            )
    except Exception as e:
        await message.answer(
            f"Произошла ошибка: {str(e)}"
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 