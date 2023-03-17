from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_button = KeyboardButton(text='/start')
del_button = KeyboardButton(text='/del')

kb.add(start_button, del_button)