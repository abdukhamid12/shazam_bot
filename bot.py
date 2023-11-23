import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command

from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils import *
from database import *
from states import *
from btn import *


BOT_TOKEN = "6600379465:AAEf5a5cCTMtJ3HSj1L8Msd94UdK-w1fEoY"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

ADMINS = [1037348868]


async def command_menu(dp: Dispatcher):
  await dp.bot.set_my_commands(
    [
      types.BotCommand('start', 'Ishga tushirish'),
    ]
  )
  await create_tables()


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
  await add_user(message.from_user.id, message.from_user.username)
  await message.answer("Salom birodar", )

@dp.message_handler(commands=['admin'])
async def totals_user(message: types.Message):
  if message.from_user.id in ADMINS:
    score = await total_user()
    await message.answer(f"botni ishlatgan odamlar soni: {score}", reply_markup=menu)
    
@dp.message_handler(commands=['send'])
async def send_handler(message: types.Message):

  if message.from_user.id in ADMINS:
    await message.answer("Xabarni yuboring:")

    await AdminStates.mailing.set()

@dp.message_handler(content_types=['video'])
async def get_user_video(message: types.Message):
    user_id = message.from_user.id
    filename = f"video_{user_id}.mp4"
    file_size = round(message.video.file_size / 1024 / 1024)
  
    if file_size <= 20:
        await message.video.download(destination_file=filename)

        result = await media_shazaming(filename)
        if result:
          await message.reply(f"Nomi: {result[0]}\nIjrochi: {result[1]}")
          if len(result) == 3:
            await message.answer_audio(types.InputFile(result[-1]), caption="caption")
          
        await delete_user_media(user_id)
        
    else:
      await message.answer("20mb dan yuqori xajimdagi videoni tortaolmiman!")


if __name__ == "__main__":
  executor.start_polling(dp, on_startup=command_menu)