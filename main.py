from config import TG_KEY, GPT_KEY
from keybrds import kb
from redis_client import redis_client

import openai
from aiogram import Bot, Dispatcher, executor, types



openai.api_key = GPT_KEY

bot = Bot(token=TG_KEY)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start_func(message: types.Message):
    print('Bot has started!')
    await message.reply('Welcome to Chat_bot. This bot uses ChatGPT!\n\nTo clear cache use command /del.',
                        reply_markup=kb)


@dispatcher.message_handler(commands=['del'])
async def clear_cache(message: types.Message):
    user_id = types.User.get_current().id
    redis_client.delete(user_id)
    redis_client.close()
    await message.reply('Chache was cleared!',
                        reply_markup=kb)
    

@dispatcher.message_handler()
async def get_message(message: types.Message)->None:
    user_id = types.User.get_current().id
    print(user_id)

    if redis_client.get(user_id):
        db_message = redis_client.get(user_id).decode()
    else:
        db_message = str(redis_client.set(user_id, ''))
    redis_client.close()

    chat_history = db_message + '\n\nHuman: ' + message.text + '\n\nAI:'

    if len(chat_history) > 2000:        
        chat_history = chat_history[-2000:]
    print('CHAT LENGTH: ', len(chat_history))

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages = [{'role': 'user', 
                     'content': chat_history}],        
        temperature = 1,)
        #prompt=chat_history,
        #temperature=0.9,
        #max_tokens=1000,
        #top_p=1.0,
        #frequency_penalty=0.0,
        #presence_penalty=0.0,
        #stop=[" Human:", " AI:"])

    #answer = response['choices'][0]['text']
    answer = response['choices'][0]['message']['content']
    await message.reply(f'<code>{answer}</code>', 
                        parse_mode='html')

    chat_history = chat_history + answer
    #print('CHAT_HISTORY: ',  chat_history)
    redis_client.set(user_id, chat_history.encode(), ex=480)
    #print('RDB: ', redis_client.get(user_id).decode())

    redis_client.close()


if __name__ == '__main__':
    executor.start_polling(dispatcher, 
                           skip_updates=True)
