import openai

from config import TG_KEY, GPT_KEY

from aiogram import Bot, Dispatcher, executor, types

openai.api_key = GPT_KEY

bot = Bot(token=TG_KEY)
dp = Dispatcher(bot)


@dp.message_handler()
async def get_message(message: types.Message):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=message.text,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    await message.reply(response['choices'][0]['text'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)