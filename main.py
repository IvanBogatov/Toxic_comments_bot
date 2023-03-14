import os
import logging

from aiogram import Bot, Dispatcher, executor, types

from config import LOGFILE_PATH
from back import get_estimation


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=LOGFILE_PATH,
                    filemode='a')

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    text = 'Напишите комментарий, чтобы оценить вероятность его токсичности.'
    await bot.send_message(chat_id=user_id, text=text)

@dp.message_handler()
async def comment_handler(message: types.Message):
    user_name = message.from_user.username
    user_id = message.from_user.id
    message_text = message.text
    prob_toxic = get_estimation(message.text)
    answer = f'Комментарий токсичный с вероятностью {prob_toxic:.2%}'
    logging.info(f"{user_name=} {user_id=} have sent comment: {message_text=}.")
    await bot.send_message(chat_id=user_id, text=answer)

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)