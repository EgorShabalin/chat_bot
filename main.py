import openai
import redis

from config import TG_KEY, GPT_KEY

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



openai.api_key = GPT_KEY

bot = Bot(token=TG_KEY)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_button = KeyboardButton(text='/start')
del_button = KeyboardButton(text='/del')

kb.add(start_button, del_button)

rdb = redis.Redis(host='redis', port=6379, db=0)


@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
    print('Bot has started!')
    await message.reply('Welcome to Chat_bot. This bot uses ChatGPT!\n\nTo clear cache use command /del.',
                        reply_markup=kb)


@dp.message_handler(commands=['del'])
async def clear_cache(message: types.Message):
    user_id = types.User.get_current().id
    rdb.delete(user_id)
    rdb.close()
    await message.reply('Chache was cleared!',
                        reply_markup=kb)
    

@dp.message_handler()
async def get_message(message: types.Message)->None:
    user_id = types.User.get_current().id
    print(user_id)

    if rdb.get(user_id):
        db_message = str(rdb.get(user_id))
    else:
        db_message = str(rdb.set(user_id, ''))

    chat_history = db_message + '\n\nHuman: ' + message.text + '\n\nAI:'

    if len(chat_history) > 2000:        
        chat_history = chat_history[-2000:]
    print('CHAT LENGTH: ', len(chat_history))

    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=chat_history,
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=[" Human:", " AI:"]
    )

    answer = response['choices'][0]['text']
    await message.reply(f'<code>{answer}</code>', parse_mode='html')

    chat_history = chat_history + answer
    print('CHAT_HISTORY: ',  chat_history)
    rdb.set(user_id, str(chat_history))
    print('RDB: ', rdb.get(user_id))

    rdb.close()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)