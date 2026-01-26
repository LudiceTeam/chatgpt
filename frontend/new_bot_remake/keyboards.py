from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
import os
import sys
from config import PROJECT_ROOT

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = "Chat"),KeyboardButton(text = "Profile")]
])

profile_key_borad = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = "Subscribe"),KeyboardButton(text = "Back")]
])

buy_sub_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = "Buy subscribtion"),KeyboardButton(text = "Back")]
])

back_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = "Back")]
])
