import asyncio
import os
import time
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
import telebot
import random
import logging
from bs4 import BeautifulSoup
import requests
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji
from config_reader import config
from aiogram.types import Message
from aiogram.enums import ParseMode


folder_path = "meme_images"


def download_images(folder_path):
    """Скачивает изображения с указанного URL и сохраняет их в указанную директорию."""
    response = requests.get(url="https://www.memify.ru/highfive/")
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    cards = soup.find_all('div', class_='card')

    for card in cards:
        img_tags = card.find_all('img')
        for img in img_tags:
            img_url = img.get('src')
            if img_url:
                img_name = os.path.basename(img_url)
                img_data = requests.get(img_url).content
                with open(os.path.join(folder_path, img_name), 'wb') as f:
                    f.write(img_data)
                    print(f"Изображение {img_name} сохранено успешно.")


def get_random_image_path(folder_path):
    """Выбирает случайное изображение из указанной директории."""
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if image_files:
        return os.path.join(folder_path, random.choice(image_files))
    else:
        return None


def send_first_image_to_group(group_id, image_path):
    """Отправляет первое изображение из указанного пути в указанную группу."""
    if image_path:
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=group_id, photo=photo)
    else:
        print("В указанной директории нет изображений.")


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command("информация",prefix = "!"))
async def cmd_info(message: types.Message, started_at: str):
    await message.answer(f"Бот запущен {started_at}")


@dp.message(Command("кубик",prefix="!"))
async def cmd_dice(message: types.Message):
    await bot.send_dice(message.chat.id, emoji=DiceEmoji.DICE)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет всем!")


@dp.message(Command("мем",prefix = "!"))
async def upload_photo(message: types.Message):
    try:
        image_path = get_random_image_path(folder_path)

        result = await message.answer_photo(
            types.FSInputFile(image_path)
        )
        os.remove(image_path)
    except:
        await message.answer("Мемы кончились, идет генерация новых...")
        download_images(folder_path)
        time.sleep(4)
        image_path = get_random_image_path(folder_path)
        result = await message.answer_photo(
            types.FSInputFile(image_path))
        os.remove(image_path)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
